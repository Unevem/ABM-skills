Projeto: ABM AI Guidelines
Objetivo
Criar um repositório de guidelines, templates e regras que possa ser utilizado por ferramentas de IA durante a construção de modelos baseados em agentes — ABM — em Python.

O projeto é voltado principalmente para pesquisadores de outras áreas que possuem conhecimento do fenômeno estudado, mas pouca experiência em programação. A IA deve auxiliar na implementação, sem substituir as decisões teóricas nem a revisão humana.

O repositório deve transformar uma descrição conceitual feita pelo pesquisador em um projeto ABM organizado, documentado, incremental e revisável.

Princípio central
A IA não deve inventar livremente um modelo. Ela deve:

Entender o objetivo do pesquisador.

Identificar informações ausentes.

Registrar dúvidas e pressupostos.

Estruturar o modelo antes de programá-lo.

Criar uma lista de tarefas.

Implementar o modelo gradualmente.

Relacionar cada decisão de modelagem ao código correspondente.

Solicitar revisão humana em decisões teóricas importantes.

O projeto não pretende garantir que o modelo esteja cientificamente correto. Ele deve aumentar a clareza, a organização e a rastreabilidade do processo.

Base metodológica
Usar o protocolo ODD — Overview, Design Concepts and Details — como estrutura principal para documentar o modelo. ODD é um protocolo amplamente utilizado para descrever ABMs e também pode funcionar como um roteiro para o design do modelo.

O modelo deve ser organizado, quando aplicável, nos seguintes componentes:

Propósito.

Entidades.

Escala espacial e temporal.

Estado dos agentes.

Regras de comportamento.

Interações.

Ambiente.

Emergência.

Adaptação e aprendizado.

Aleatoriedade.

Inicialização.

Parâmetros.

Entradas externas.

Submodelos.

Métricas e resultados.

Estrutura do repositório
text
abm-ai-guidelines/
├── README.md
├── AGENTS.md
├── TASKS.md
├── LICENSE
├── CITATION.cff
├── skills/
│   ├── abm-design/
│   │   └── SKILL.md
│   ├── odd-documentation/
│   │   └── SKILL.md
│   ├── python-abm/
│   │   └── SKILL.md
│   └── validation/
│       └── SKILL.md
├── rules/
│   ├── human-review.md
│   ├── no-undocumented-assumptions.md
│   ├── reproducibility.md
│   ├── task-management.md
│   └── code-organization.md
├── templates/
│   ├── odd-template.md
│   ├── model-specification.md
│   ├── experiment-config.yaml
│   └── decision-log.md
└── examples/
    └── opinion-dynamics/
        ├── README.md
        ├── odd.md
        ├── model.py
        ├── agents.py
        ├── experiments.py
        └── requirements.txt
Arquivo AGENTS.md
Esse arquivo deve conter as regras gerais para a IA:

Ler o README.md, o TASKS.md e a especificação do modelo antes de alterar o código.

Nunca criar uma regra comportamental sem documentá-la.

Nunca inventar decisões teóricas sem marcar a decisão como hipótese.

Perguntar ao usuário quando uma informação importante estiver ausente.

Registrar decisões pendentes no TASKS.md.

Implementar uma tarefa por vez.

Não modificar partes não relacionadas do projeto.

Separar agentes, ambiente, regras, experimentos e métricas em componentes diferentes.

Utilizar parâmetros configuráveis em vez de valores espalhados pelo código.

Usar sementes aleatórias quando houver estocasticidade.

Criar ou atualizar testes básicos quando modificar o comportamento do modelo.

Explicar ao usuário quais arquivos foram criados ou alterados.

Solicitar revisão humana antes de considerar o modelo concluído.

Arquivo TASKS.md
A IA deve manter uma lista de tarefas com estados:

text
# Tasks

## Pending

- [ ] Definir o propósito do modelo.
- [ ] Definir os tipos de agentes.
- [ ] Definir os atributos dos agentes.
- [ ] Definir as regras de interação.
- [ ] Definir o ambiente.
- [ ] Definir parâmetros iniciais.
- [ ] Definir métricas.
- [ ] Implementar os agentes.
- [ ] Implementar o ambiente.
- [ ] Criar experimentos.
- [ ] Revisar a implementação.

## In Progress

## Completed

## Decisions Needed

- [ ] O comportamento dos agentes deve ser determinístico ou estocástico?
- [ ] O ambiente deve ser espacial?
- [ ] Os agentes aprendem com interações anteriores?
Skills
abm-design
Deve ensinar a IA a transformar uma ideia informal em uma especificação ABM:

Qual fenômeno está sendo estudado?

Qual é a pergunta do modelo?

Quais entidades existem?

Quais são os agentes?

Quais atributos cada agente possui?

Como os agentes percebem o ambiente?

Como tomam decisões?

Como interagem?

O que muda ao longo do tempo?

Quais resultados serão observados?

odd-documentation
Deve orientar a IA a preencher o template ODD, incluindo:

Overview.

Design Concepts.

Details.

A IA deve marcar campos incompletos e não preencher lacunas teóricas silenciosamente.

python-abm
Deve orientar a organização do código Python:

agents.py: classes e comportamentos dos agentes.

model.py: ambiente, ciclo temporal e execução do modelo.

experiments.py: cenários, parâmetros e execuções.

metrics.py: coleta e análise dos resultados.

tests/: testes de comportamento e invariantes.

Para a implementação em Python, usar o Mesa quando for adequado, pois ele é um framework de ABM com componentes para agentes, ambientes, coleta de dados e análise.

validation
Deve orientar a criação de verificações básicas:

O modelo executa sem erros.

O número de agentes permanece válido.

Os agentes possuem estados permitidos.

Os parâmetros são lidos corretamente.

A mesma semente produz resultados reproduzíveis.

As métricas são coletadas.

A documentação corresponde ao código.

Essas verificações não provam que o modelo representa corretamente a realidade. Elas apenas verificam consistência básica da implementação.

Fluxo de uso
O fluxo principal do repositório deve ser:

O pesquisador descreve sua ideia em linguagem natural.

A IA faz perguntas para esclarecer o fenômeno.

A IA cria ou preenche model-specification.md.

A IA transforma a especificação em um documento ODD.

A IA identifica pressupostos e decisões pendentes.

A IA cria o TASKS.md.

O pesquisador revisa as decisões teóricas.

A IA implementa o projeto por etapas.

A IA executa verificações básicas.

O pesquisador revisa o código e os resultados.

Exemplo mínimo
Criar um exemplo de dinâmica de opiniões:

Cada agente possui uma opinião entre 0 e 1.

Os agentes interagem com outros agentes.

A opinião pode mudar conforme a opinião do interlocutor.

O modelo possui uma quantidade configurável de agentes.

O modelo possui número configurável de passos.

A aleatoriedade deve ser controlada por uma semente.

O resultado deve registrar a distribuição das opiniões ao longo do tempo.

O exemplo serve apenas para demonstrar o fluxo do repositório. Ele não precisa ser uma contribuição original de ciência social.

Escopo do projeto
Este é um protótipo conceitual e funcional de um repositório de instruções para IA.

O projeto não deve afirmar que:

A IA cria modelos cientificamente corretos.

O método substitui especialistas.

O repositório melhora automaticamente todos os modelos.

O uso das guidelines garante validade dos resultados.

O projeto deve afirmar que:

As guidelines estruturam o processo de desenvolvimento.

A documentação torna decisões explícitas.

A lista de tarefas facilita o desenvolvimento incremental.

O ODD ajuda a organizar a especificação.

A revisão humana continua obrigatória.

O repositório pode reduzir a barreira inicial de programação para pesquisadores de outras áreas.

Resultado esperado
Ao final, o repositório deve permitir que um usuário:

Clone o projeto.

Leia as instruções.

Forneça uma descrição informal de um ABM.

Use uma ferramenta de IA compatível com instruções de repositório.

Gere uma especificação organizada.

Acompanhe as tarefas.

Produza uma implementação Python inicial.

Revise o código, as regras e os pressupostos.

O paper futuro apresentará esse repositório como um artefato de software e uma proposta metodológica para apoiar a criação assistida por IA de ABMs em Python.