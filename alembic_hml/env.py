# env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from core.config import settings

# Importa o Base e, MUITO IMPORTANTE, registra todos os modelos no metadata:
from db.base_class import Base
import db.base  # <- garante que todas as tabelas sejam anexadas ao Base.metadata

# Alembic config
config = context.config
# injeta a URL (ou deixe no .ini e remova esta linha)
config.set_main_option(
    'sqlalchemy.url', 'postgresql://sa:Profeta_01@192.168.0.219:5432/arancia_db'
)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata para autogenerate
target_metadata = Base.metadata

# ========= CUSTOM =========
# version table exclusiva deste projeto
VERSION_TABLE = "alembic_version_mural"
PREFIX_LIST = [
    "mural_",
    # "auth_user",
    # "logistica_groupaditionalinformation"
]


# Tabelas específicas que NÃO quero que sejam lidas/controladas
EXCLUDE_TABLES = {
    "auth_user_user_permissions",
    "auth_user_groups",
    "logistica_groupaditionalinformationlegacy"
}


def _is_allowed_by_prefix(table_name: str | None) -> bool:
    if not table_name:
        return False

    return any(
        table_name.startswith(prefix)
        for prefix in PREFIX_LIST
    )


def _is_excluded_table(table_name: str | None) -> bool:
    if not table_name:
        return False

    return table_name in EXCLUDE_TABLES


def _should_include_table(table_name: str | None) -> bool:
    """
    Regra final:
    - precisa começar com algum prefixo permitido
    - não pode estar na lista de exclusão
    - não pode ser a tabela de versionamento do Alembic
    """

    if not table_name:
        return False

    if table_name == VERSION_TABLE:
        return False

    if _is_excluded_table(table_name):
        return False

    return _is_allowed_by_prefix(table_name)


def include_name(name: str | None, type_: str, parent_names: dict) -> bool:
    """
    Filtra objetos vindos do banco durante o autogenerate.
    """

    if type_ == "table":
        return _should_include_table(name)

    table_name = parent_names.get("table_name")

    if table_name:
        return _should_include_table(table_name)

    return True


def include_object(object, name, type_, reflected, compare_to):
    """
    Filtra objetos já carregados, inclusive os vindos do Base.metadata.

    Isso ajuda quando o seu Base.metadata tem models que você não quer
    que esse Alembic controle.
    """

    if type_ == "table":
        return _should_include_table(name)

    table_name = None

    if hasattr(object, "table") and object.table is not None:
        table_name = object.table.name

    if table_name:
        return _should_include_table(table_name)

    return True
# ==========================


def _get_url() -> str:
    url = config.get_main_option("sqlalchemy.url")
    return url or 'postgresql://sa:Profeta_01@192.168.0.219:5432/arancia_db'


def run_migrations_offline() -> None:
    url = _get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_name=include_name,
        include_object=include_object,
        compare_type=True,
        compare_server_default=True,
        version_table=VERSION_TABLE,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    section = config.get_section(config.config_ini_section, {})
    section.setdefault("sqlalchemy.url", _get_url())

    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_name=include_name,
            include_object=include_object,
            compare_type=True,
            compare_server_default=True,
            version_table=VERSION_TABLE,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
