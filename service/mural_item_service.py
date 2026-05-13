from datetime import datetime, timezone

from fastapi import HTTPException, status
from schemas.api_v1.mural_item_schema import MuralItemCreateSC, MuralItemUpdateSC


class MuralItemService():
    def _build_field_name(self,  field_name: str, relation: bool = True):

        if not relation:
            return f"{field_name}"

        return f"mural_item.{field_name}"

    def build_default_filters(self, relation: bool = True):
        now = datetime.now(timezone.utc)
        return [
            {
                "field": self._build_field_name(field_name="is_active", relation=relation),
                "operator": "=",
                "value": True
            },
            {
                "field": self._build_field_name(field_name="starts_at", relation=relation),
                "operator": "<=",
                "value": now
            },
            {
                "logic": "or",
                "conditions": [
                    {
                        "field": self._build_field_name(field_name="ends_at", relation=relation),
                        "operator": ">=",
                        "value": now
                    },
                    {
                        "field": self._build_field_name(field_name="is_indefinite", relation=relation),
                        "operator": "=",
                        "value": True
                    }
                ]
            }
        ]

    def build_visibility_conditions(self, target_type: str, ids: list[int] = []):

        if ids:
            filter_final = {
                "logic": "and",
                "conditions": [
                    {
                        "field": "target_type",
                        "operator": "=",
                        "value": target_type
                    },
                    {
                        "field": "id",
                        "operator": "in",
                        "value": ids
                    }
                ]
            }
        else:
            filter_final = {
                "field": "target_type",
                "operator": "=",
                "value": target_type
            }
        return filter_final

    def build_validation_itens(self, item_data: MuralItemUpdateSC, ids: list[int] | None):
        severity = item_data.severity
        until_read = item_data.until_read
        item_type = item_data.item_type
        ends_at = item_data.ends_at
        is_indefinite = item_data.is_indefinite
        target_type = item_data.target_type

        if severity == 'critical' and not until_read:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Para itens críticos, é necessário confirmação de leitura obrigatória!")

        if item_type in ('announcement', 'notice') and not (ends_at or until_read):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Para itens do tipo 'announcement' ou 'notice', é obrigatório ter confirmação de leitura ('until_read') ou data final ('ends_at').")

        if item_type in ('manual', 'script') and (ends_at or until_read):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Para manuais ou scripts, é necessário que o item tenha prazo indefinido. Não envie ends_at nem until_read.")

        if is_indefinite and ends_at:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Itens marcados como 'definitivos' não podem conter ends_at.")

        if target_type and target_type != 'all' and not ids:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="O campo ids é obrigatório quando o target for != 'all'")

        if target_type and target_type == 'all' and ids:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="O campo ids não deve ser enviado quando o target for 'all'")

        if ends_at and isinstance(ends_at, datetime) and ends_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="A data de expiração (ends_at) deve estar no futuro.")


mural_item_service = MuralItemService()
