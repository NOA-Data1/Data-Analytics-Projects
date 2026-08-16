# Segmentação e Efetividade de Incentivos

**Da resposta de campanha ao plano de ação: segmentação, teste de hipótese com grupo controle, propensão e monitoramento de KPI.**

Este projeto usa o **iFood Data Business Analyst Test**, dataset publicado pelo próprio time iFood Brain para avaliar candidatos a Analista de Dados (`github.com/ifood/ifood-data-business-analyst-test`). Ele descreve clientes e sua resposta a campanhas promocionais.

> **Nota de transparência.** O dataset original é sobre resposta de clientes a campanhas de marketing, e não é o Programa Super de fidelização de entregadores do iFood. Não existe dado público sobre esse programa específico. Este projeto demonstra a metodologia, com segmentação, desenho de grupo controle, modelo de propensão, monitoramento de KPI e dashboard, aplicada a um problema de incentivo e engajamento estruturalmente equivalente, usando dado real e publicamente rastreável da própria empresa.

## A pergunta central

> O incentivo realmente muda o comportamento do cliente, ou quem aceita já era diferente antes?

Sem responder isso com rigor estatístico, qualquer "resultado de campanha" é coincidência disfarçada de causa. Esse é o fio condutor do projeto.

## Resultado principal

- 2.021 clientes analisados após remoção de duplicatas (8,3% da base original).
- Taxa de resposta geral à campanha: **15,4%**.
- Clientes que aceitam a campanha têm renda, frequência de compra e recência estatisticamente diferentes de quem não aceita, com Mann-Whitney U e p abaixo de 0,001 em todas as variáveis. A taxa de resposta bruta superestima o efeito puro do incentivo.
- Quatro segmentos comportamentais identificados via K-means, com taxas de resposta que vão de 4,6% no segmento de risco de desengajamento a 23,7% no segmento de alto valor ativo.
- Um modelo de propensão simples permite contatar 20% da base e capturar 61,5% de todos os respondentes esperados, um ganho de eficiência real sobre campanha em massa.

## Estrutura do projeto

```text
ifood-incentivos/
├── data/                # Dataset original e versões tratadas
├── notebooks/           # Fluxo analítico em seis partes
├── reports/             # Métricas reproduzíveis (JSON)
├── exports/             # CSVs agregados prontos para Tableau/Looker Studio
└── dashboard/app.py     # Dashboard Streamlit
```

## Roteiro dos notebooks

| Notebook | Objetivo |
|---|---|
| `01_fonte_e_qualidade_dos_dados.ipynb` | Auditoria da fonte, dicionário de dados, limpeza de duplicatas |
| `02_frequencia_ganhos_e_retencao.ipynb` | Construção dos três KPIs centrais do incentivo |
| `03_segmentacao_de_clientes.ipynb` | Clusterização K-means e perfil de cada segmento |
| `04_testes_de_hipotese_e_grupo_controle.ipynb` | Teste estatístico de viés entre grupo que aceita e não aceita o incentivo |
| `05_modelo_de_propensao_a_incentivo.ipynb` | Modelo de propensão e visão de capacidade de contato |
| `06_monitoramento_de_kpi_e_planos_de_acao.ipynb` | Regra de alerta por desvio de meta e plano de ação por time |

## Dashboards

O projeto inclui três formas de visualizar o mesmo resultado, propositalmente, para demonstrar fluência nas três ferramentas citadas na vaga de Analista de BI:

- Streamlit, em `dashboard/app.py`: protótipo interativo completo, com as quatro visões do projeto.
- Tableau Public: construído a partir dos CSVs em `exports/`, ver passo a passo no README de publicação.
- Looker Studio: construído a partir dos mesmos CSVs, ver passo a passo no README de publicação.

## Reproduzir a análise

```bash
python -m pip install pandas numpy scikit-learn scipy matplotlib seaborn plotly streamlit
jupyter notebook notebooks/
```

## Limitações

- O dataset não documenta atribuição aleatória de campanha. O grupo controle é observacional, não experimental.
- A base é pequena (2.021 clientes) para os padrões de um modelo de produção.
- Não há carimbo de data por transação. Os ciclos no notebook 06 são simulados para demonstrar a lógica de alerta, não uma série temporal real.
- O dataset descreve clientes consumidores, não entregadores. A metodologia é transferível, os dados literais não.

## Ferramentas utilizadas

Python · pandas · scikit-learn · scipy · Plotly · Streamlit · Tableau Public · Looker Studio

## Fonte

[iFood Data Business Analyst Test](https://github.com/ifood/ifood-data-business-analyst-test), o case oficial do time iFood Brain.
