import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")
st.title('Dashboard de Vendas')

@st.cache_data
def carregar_dados():
    diretorio_atual = os.path.dirname(__file__)
    caminho_csv = os.path.join(diretorio_atual, 'vendas.csv')

    df = pd.read_csv(caminho_csv, sep=';')
    df['mes'] = df['data_hora'].str[:7]
    return df

df = carregar_dados()

st.sidebar.title('Filtros')

lista_de_categorias = df['categoria'].unique()

categorias = st.sidebar.multiselect('Selecione as Categorias',
    options=sorted(lista_de_categorias),
    default=sorted(lista_de_categorias),
)

df_filtrado = df[df['categoria'].isin(categorias)]

receita_calculada = df_filtrado['valor_venda'].sum()
total_pedidos = len(df_filtrado)

col1, col2 = st.columns([1,1])
with col1:
    st.metric(label='Receita Total', value=f"R$ {receita_calculada:,.2f}")

with col2:
    st.metric(label='Total de Pedidos', value=total_pedidos)

aba1, aba2 = st.tabs(['Evolução Mensal', 'Tabela de Dados'])

with aba1:
    dados_agrupados = df_filtrado.groupby('mes')['valor_venda'].sum()
    st.area_chart(dados_agrupados)

with aba2:
    st.dataframe(df_filtrado)

    st.download_button(
        label="Baixar Tabela em CSV",
        data=df_filtrado.to_csv(index=False).encode('utf-8'),
        file_name="vendas_filtradas.csv",
        mime="text/csv"
    )
