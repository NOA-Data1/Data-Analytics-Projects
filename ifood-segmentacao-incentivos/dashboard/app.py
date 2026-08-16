"""Dashboard de portfólio de Segmentação e Efetividade de Incentivos, iFood."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

TEAL = "#0E6268"
CORAL = "#F08FA0"
SLATE = "#728489"
DARK = "#15262B"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXPORTS = PROJECT_ROOT / "exports"

st.set_page_config(page_title="Segmentação e Incentivos", page_icon="◉", layout="wide")


def style_figure(figure, height=440):
    figure.update_layout(
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font={"color": DARK, "family": "Inter, sans-serif"},
        margin={"l": 10, "r": 10, "t": 60, "b": 10},
    )
    return figure


@st.cache_data
def load_data():
    clientes = pd.read_csv(EXPORTS / "clientes_segmentados.csv")
    resumo = pd.read_csv(EXPORTS / "resumo_por_segmento.csv")
    painel = pd.read_csv(EXPORTS / "painel_ciclos.csv")
    return clientes, resumo, painel


clientes, resumo, painel = load_data()

st.markdown('<div style="color:#60767B; font-size:.85rem; letter-spacing:.06em; text-transform:uppercase;">Estudo de caso de portfólio · Segmentação e incentivos</div>', unsafe_allow_html=True)
st.title("Segmentação e Efetividade de Incentivos")
st.markdown('<p style="margin-top:-.6rem; color:#60767B; font-size:1.05rem;">Baseado no iFood Data Business Analyst Test, o dataset oficial do time iFood Brain</p>', unsafe_allow_html=True)

st.info(
    "Este projeto usa o dataset público que o próprio iFood publica para avaliar candidatos a Analista de Dados "
    "(resposta de clientes a campanhas de marketing). Ele é usado aqui para demonstrar metodologia de segmentação, "
    "teste de hipótese e monitoramento de incentivo. Ele não representa o Programa Super de entregadores.",
    icon="ℹ️",
)

overview_tab, segments_tab, hypothesis_tab, monitoring_tab = st.tabs(
    ["Visão geral", "Segmentação", "Efetividade do incentivo", "Monitoramento e alertas"]
)

with overview_tab:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Clientes analisados", f"{len(clientes):,}")
    c2.metric("Taxa de resposta geral", f"{clientes.Response.mean():.1%}")
    c3.metric("Renda média", f"R$ {clientes.Income.mean():,.0f}")
    c4.metric("Ganhos médios por cliente", f"R$ {clientes.ganhos_gerados.mean():,.0f}")

    left, right = st.columns([1.4, 1])
    with left:
        figure = px.bar(
            resumo.sort_values("taxa_de_resposta", ascending=True),
            x="taxa_de_resposta", y="segmento", orientation="h",
            title="Taxa de resposta ao incentivo, por segmento",
            color_discrete_sequence=[CORAL],
        )
        figure.update_xaxes(tickformat=".0%")
        style_figure(figure)
        st.plotly_chart(figure, width="stretch")
    with right:
        figure = px.pie(
            clientes, names="segmento", title="Distribuição de clientes por segmento",
            color_discrete_sequence=[TEAL, CORAL, SLATE, "#C9A66B"],
            hole=.55,
        )
        style_figure(figure)
        st.plotly_chart(figure, width="stretch")

with segments_tab:
    st.subheader("Perfil de cada segmento")
    st.dataframe(
        resumo.style.format({
            "renda_media": "R$ {:.0f}", "frequencia_media": "{:.1f}",
            "ganhos_medios": "R$ {:.0f}", "recencia_media": "{:.0f} dias",
            "taxa_de_resposta": "{:.1%}",
        }),
        width="stretch", hide_index=True,
    )
    figure = px.scatter(
        clientes, x="Income", y="ganhos_gerados", color="segmento",
        title="Renda vs. ganhos gerados, por segmento",
        color_discrete_sequence=[TEAL, CORAL, SLATE, "#C9A66B"],
        opacity=.6,
    )
    style_figure(figure, height=520)
    st.plotly_chart(figure, width="stretch")

with hypothesis_tab:
    st.subheader("O grupo que aceita o incentivo já era diferente?")
    st.markdown(
        "Teste de Mann-Whitney U comparando quem aceitou e quem não aceitou a campanha, "
        "antes de qualquer leitura de causa."
    )
    comparacao = clientes.groupby("Response")[["Income", "frequencia_total", "Recency"]].median().reset_index()
    comparacao["Response"] = comparacao.Response.map({0: "Não aceitou", 1: "Aceitou"})
    figure = go.Figure()
    for coluna, cor in zip(["Income", "frequencia_total", "Recency"], [TEAL, CORAL, SLATE]):
        figure.add_bar(x=comparacao.Response, y=comparacao[coluna], name=coluna)
    figure.update_layout(barmode="group", title="Mediana de perfil, por resposta ao incentivo")
    style_figure(figure)
    st.plotly_chart(figure, width="stretch")
    st.caption(
        "Todas as três variáveis mostram diferença estatisticamente significativa (p < 0,001) entre "
        "quem aceita e quem não aceita. A taxa de resposta bruta superestima o efeito puro do incentivo."
    )

with monitoring_tab:
    st.subheader("Painel de acompanhamento por ciclo (simulado)")
    metrica = st.selectbox("Métrica", ["ganhos_medios", "taxa_de_resposta", "frequencia_media"], index=0)
    figure = px.line(
        painel, x="ciclo_simulado", y=metrica, color="segmento", markers=True,
        title=f"{metrica.replace('_',' ').title()} por ciclo e segmento",
        color_discrete_sequence=[TEAL, CORAL, SLATE, "#C9A66B"],
    )
    style_figure(figure, height=480)
    st.plotly_chart(figure, width="stretch")
    st.caption(
        "Ciclos simulados a partir de um recorte único no tempo. A estrutura de alerta é reaproveitável em "
        "produção, mas os números não representam previsão real de desempenho futuro."
    )
