
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Citas Médicas",
    page_icon="🏥",
    layout="wide"
)

df = pd.read_csv("citas_medicas.csv")

df["fecha"] = pd.to_datetime(df["fecha"])
df["mes"] = df["fecha"].dt.month

st.title("🏥 Dashboard de Gestión de Citas Médicas")
st.write("Análisis de citas médicas simuladas de un hospital de Lima Norte.")

total_citas = len(df)
total_atendidas = (df["estado"] == "Atendida").sum()
total_canceladas = (df["estado"] == "Cancelada").sum()
total_no_asistio = (df["estado"] == "No asistió").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de citas", total_citas)
col2.metric("Atendidas", total_atendidas)
col3.metric("Canceladas", total_canceladas)
col4.metric("No asistió", total_no_asistio)

st.divider()

especialidad = st.selectbox(
    "Filtrar por especialidad",
    ["Todas"] + sorted(df["especialidad"].unique().tolist())
)

if especialidad != "Todas":
    df_filtrado = df[df["especialidad"] == especialidad]
else:
    df_filtrado = df

st.subheader("Citas por Especialidad")

citas_especialidad = df_filtrado["especialidad"].value_counts().reset_index()
citas_especialidad.columns = ["especialidad", "cantidad"]

fig1 = px.bar(
    citas_especialidad,
    x="especialidad",
    y="cantidad",
    text="cantidad"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Estado de las Citas")

fig2 = px.pie(
    df_filtrado,
    names="estado"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Citas por Mes")

citas_mes = df_filtrado.groupby("mes").size().reset_index(name="cantidad")

fig3 = px.line(
    citas_mes,
    x="mes",
    y="cantidad",
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Vista de datos")

st.dataframe(df_filtrado)
