# Módulo Mural de Comunicados

## Visão Geral

O módulo **Mural de Comunicados** tem como objetivo centralizar, organizar e rastrear avisos, comunicados, scripts operacionais e manuais diretamente na tela inicial do CRM.

A criação deste módulo surgiu da necessidade de substituir comunicações dispersas ou improvisadas por um recurso interno padronizado, controlado e auditável. Clientes como a **Cielo** frequentemente solicitam evidências de treinamentos, comunicações e orientações repassadas às equipes. Dessa forma, o mural passa a atuar como uma ferramenta de comunicação interna com rastreabilidade, permitindo comprovar o alcance das informações publicadas.

Na prática, o mural funciona como um módulo orientado por:

- Conteúdo;
- Público-alvo;
- Vigência;
- Criticidade;
- Prioridade;
- Rastreabilidade de leitura.

Com isso, o sistema passa a oferecer maior controle sobre quais informações são exibidas, para quem são exibidas, por quanto tempo permanecem disponíveis e se foram ou não lidas pelos usuários.

---

## Objetivo do Módulo

O principal objetivo do mural é garantir que informações importantes sejam disponibilizadas em um único ponto do sistema, reduzindo falhas de comunicação e facilitando o acompanhamento das publicações.

O módulo permite publicar diferentes tipos de conteúdo, como:

- Avisos operacionais;
- Comunicados internos;
- Scripts de atendimento;
- Manuais;
- Orientações de processo;
- Informações críticas ou emergenciais.

Além disso, o mural permite que essas publicações sejam direcionadas para públicos específicos, evitando que usuários recebam informações que não fazem parte da sua rotina ou permissão de atuação.

---

## Justificativa

Antes da criação do mural, comunicados e treinamentos poderiam ser realizados por meios externos ou pouco rastreáveis, como e-mails, mensagens, arquivos avulsos ou orientações verbais.

Esse modelo gera alguns problemas:

- Dificuldade para comprovar que determinado usuário recebeu ou visualizou uma comunicação;
- Baixa rastreabilidade sobre treinamentos e orientações;
- Risco de perda de informação;
- Falta de histórico organizado;
- Dificuldade para direcionar conteúdos por grupo, GAI ou usuário;
- Dependência de controles manuais.

Com o mural, o CRM passa a contar com uma camada própria de comunicação interna, permitindo maior governança sobre os conteúdos publicados e seus respectivos públicos.

---

## Funcionalidades Principais

### 1. Publicação de Conteúdos

O módulo permite cadastrar e publicar conteúdos diretamente no CRM, centralizando informações importantes em um único ambiente.

Tipos de conteúdo previstos:

- `notice` — Aviso;
- `announcement` — Comunicado;
- `script` — Script;
- `manual` — Manual.

Essa classificação permite tratar cada publicação de acordo com sua finalidade.

---

### 2. Segmentação por Público-Alvo

Cada item publicado no mural pode ser direcionado para diferentes públicos.

Tipos de público previstos:

- Todos os usuários;
- Usuários específicos;
- GAIs específicas;
- Grupos específicos.

Isso permite que uma comunicação seja exibida apenas para quem realmente precisa recebê-la.

Exemplos:

- Um manual operacional pode ser exibido apenas para um grupo específico;
- Um comunicado de processo pode ser direcionado para uma GAI;
- Um aviso geral pode ser exibido para todos os usuários;
- Um script específico pode ser liberado apenas para determinados operadores.

---

### 3. Controle de Vigência

Cada publicação pode possuir um período de validade, definindo quando deve começar e quando deve deixar de ser exibida.

O módulo deve permitir:

- Definir data e hora de início;
- Definir data e hora de término;
- Criar itens sem prazo final;
- Ocultar automaticamente itens fora do período de vigência.

Dessa forma, comunicados temporários não precisam ser removidos manualmente após perderem validade.

---

### 4. Itens Sem Prazo Final

Alguns conteúdos, como manuais, scripts ou orientações permanentes, podem não possuir uma data final de expiração.

Para esses casos, o mural deve permitir marcar o item como **indefinido**, mantendo-o disponível enquanto estiver ativo.

---

### 5. Ativação e Desativação de Publicações

O módulo deve permitir desabilitar um item sem apagar seu histórico.

Isso é importante para manter a rastreabilidade das publicações antigas, mesmo que elas não estejam mais visíveis para os usuários.

Com isso, o sistema preserva:

- Histórico do conteúdo publicado;
- Data de criação;
- Público-alvo;
- Registros de leitura;
- Responsável pela publicação;
- Informações de auditoria.

---

### 6. Criticidade dos Comunicados

Cada item pode possuir um nível de criticidade, permitindo diferenciar visualmente publicações simples de comunicados mais importantes.

Níveis sugeridos:

- `informational` — Informativo;
- `moderate` — Moderado;
- `important` — Importante;
- `critical` — Crítico.

Itens críticos devem receber maior destaque visual na interface, chamando a atenção do usuário para informações que exigem leitura imediata ou maior prioridade.

---

### 7. Controle de Leitura

O mural deve permitir controlar a leitura dos itens quando necessário.

Alguns comunicados podem exigir que o usuário confirme manualmente a leitura através da ação **“Marcar como lido”**.

Esse controle é essencial para gerar evidências de comunicação e treinamento.

O sistema deve registrar, quando aplicável:

- Usuário que realizou a leitura;
- Data e hora da leitura;
- Item lido;
- Público-alvo da publicação;
- Necessidade ou não de leitura obrigatória.

---

### 8. Rastreabilidade

Um dos principais ganhos do módulo é a rastreabilidade.

O sistema deve permitir acompanhar quais usuários visualizaram ou confirmaram a leitura de determinado conteúdo, apoiando processos internos e demandas de auditoria.

Essa rastreabilidade pode ser utilizada para:

- Evidenciar treinamentos;
- Comprovar ciência de comunicados;
- Apoiar cobranças de clientes;
- Identificar usuários que ainda não visualizaram uma orientação;
- Manter histórico de comunicação interna.

---

## Regras de Negócio

### Exibição dos Itens

Um item deve ser exibido no mural quando:

- Estiver ativo;
- Estiver dentro do período de vigência;
- Não estiver expirado, exceto quando marcado como sem prazo final;
- O usuário logado fizer parte do público-alvo;
- O item respeitar as regras de segmentação configuradas.

---

### Público-Alvo

Quando o item for destinado a todos os usuários, não é necessário informar IDs específicos.

Quando o item for destinado a usuários, GAIs ou grupos, deve ser informada a lista de IDs correspondentes ao tipo de público selecionado.

Exemplo:

```json
{
  "target_type": "groups",
  "ids": [1, 2, 3]
}
