import time
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

# Configurando o layout e o título da página
st.set_page_config(page_title='SINASC Rondônia', layout='wide')
custom_height = 300  
st.markdown(f'<img src="https://media.giphy.com/media/FtlUfrq3pVZXVNjoxf/giphy.gif" style="width:100%; height:{custom_height}px;">', unsafe_allow_html=True)
st.title('Explorando o Streamlit - Análise SINASC 🤓👆📊')

# Função para carregar os dados com cache
@st.cache_data
def carregar_dados(caminho):
    return pd.read_csv(caminho, parse_dates=['DTNASC'])

# Lendo o arquivo csv e mostrando um dataframe na tela
caminho_dados = r'C:\\Users\\Arthu\\OneDrive\\Área de Trabalho\\Data Science\\notebooks\\SINASC_RO_2019.csv'
dados_nascimentos = carregar_dados(caminho_dados)

# Barra de progresso
with st.spinner('Carregando dados...'):
    progress_bar = st.progress(0, text='Progresso: 0%')
    progress_text = st.empty()
    for percent_complete in range(0, 101, 10):
        time.sleep(1)
        progress_bar.progress(percent_complete)
        progress_text.text(f'Progresso: {percent_complete}%')

st.success('Dados carregados com sucesso!')

# Contexto sobre o assunto
st.header('Contexto sobre o assunto 🕵')
st.video('https://www.youtube.com/watch?v=8j4pOqbPgw8')
st.markdown(f'<iframe src="https://pt.wikipedia.org/wiki/Sistema_de_informa%C3%A7%C3%A3o_em_sa%C3%BAde" width="100%" height="500"></iframe>', unsafe_allow_html=True)
st.markdown(f'<iframe src="https://cidades.ibge.gov.br/brasil/ro/panorama" width="100%" height="500"></iframe>', unsafe_allow_html=True)

# Limpando o texto de progresso
progress_bar.empty()
progress_text.empty()

# Criando um checkbox para mostrar ou ocultar o DataFrame na barra lateral
show_dataframe = st.sidebar.checkbox('Mostrar / Ocultar DataFrame', value=True, key='show_dataframe')
if show_dataframe:
    st.dataframe(dados_nascimentos)

# Criando uma barra lateral com alguns widgets
st.sidebar.header('Filtro')
peso_min = st.sidebar.slider('Peso mínimo ao nascer (em gramas)', min_value=0, max_value=6000, value=0, step=100)
dados_nascimentos = dados_nascimentos[dados_nascimentos['PESO'] >= peso_min]

# Gráfico de pizza com os dados de nascimentos por sexo
st.header('Visualziando os dados')
st.subheader('Escolaridade Mãe')
fig, ax = plt.subplots()
ax.pie(dados_nascimentos['SEXO'].value_counts(), labels=['Feminino', 'Masculino'], autopct='%1.1f%%')
ax.set_title('Distribuição dos nascimentos por sexo')
ax.text(0, -1.4, 'Parabéns aos pais!', fontsize=16, color='green', ha='center')
st.pyplot(fig, use_container_width=True)

# Gráficos interativos com os dados de nascimentos por sexo, idade da mãe, peso ao nascer, etc.
st.header('Gráficos de nascimentos por variáveis')
st.subheader('Escolaridade Mãe')
fig1 = px.pie(dados_nascimentos, names='ESCMAE', title='Distribuição da escolaridade da mãe')
st.plotly_chart(fig1, use_container_width=True)

st.subheader('Idade da mãe - Histograma Interativo')
fig2 = px.histogram(dados_nascimentos, x='IDADEMAE', title='Distribuição da idade da mãe', color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig2, use_container_width=True)

st.subheader('Peso ao nascer e idade gestacional - Scatter Plot Interativo')
fig3 = px.scatter(dados_nascimentos, x='GESTACAO', y='PESO', title='Relação entre peso ao nascer e idade gestacional', color_discrete_sequence=px.colors.sequential.RdBu, marginal_x="histogram", marginal_y="histogram")
st.plotly_chart(fig3, use_container_width=True)

# Mapa de nascimentos por município
dados_nascimentos['TOTAL_FILHOS'] = dados_nascimentos[['QTDFILVIVO', 'QTDFILMORT']].sum(axis=1)
dados_nascimentos.dropna(subset=['munResLat', 'munResLon', 'TOTAL_FILHOS'], inplace=True)
st.header('Mapa de nascimentos por município')
fig = px.scatter_mapbox(
    dados_nascimentos,
    lat='munResLat',
    lon='munResLon',
    color='TOTAL_FILHOS',
    size='TOTAL_FILHOS',
    mapbox_style='carto-darkmatter',
    zoom=5,
    color_continuous_scale='reds',
    title='Heatmap de nascimentos por município',
).update_layout(mapbox=dict(accesstoken='YOUR_MAPBOX_ACCESS_TOKEN'))
st.plotly_chart(fig, use_container_width=True)

# Seletor de intervalo de datas
DTNASC = pd.to_datetime(dados_nascimentos['DTNASC'], format='%d%m%Y')
date_selector_expander = st.sidebar.date_input("Selecione a Data Inicial", min_value=DTNASC.min(), max_value=DTNASC.max(), value=DTNASC.min(), key='date_selector', format="DD/MM/YYYY")
end_date = st.sidebar.date_input("Selecione a Data Final", min_value=DTNASC.min(), max_value=DTNASC.max(), value=DTNASC.max(), key='end_date', format="DD/MM/YYYY")
start_date, end_date = pd.to_datetime(date_selector_expander, format="%Y-%m-%d"), pd.to_datetime(end_date, format="%Y-%m-%d")
filtered_data = dados_nascimentos[(DTNASC >= start_date) & (DTNASC <= end_date)]
date_info = f"**Intervalo de Datas Selecionado:**\n\nInício: {start_date.strftime('%d/%m/%Y')}\n\nFim: {end_date.strftime('%d/%m/%Y')}"
st.sidebar.info(date_info)
st.markdown(
    """
    <style>
    div[data-testid="stSidebar"] .stAlert {
        background-color: green;
    }
    </style>
    """,
    unsafe_allow_html=True)

# Mensagem de aviso para datas fora do intervalo disponível
if start_date < DTNASC.min() or end_date > DTNASC.max():
    st.warning('Atenção: Certifique-se de que as datas selecionadas estão dentro do intervalo disponível.')

# Gerador de Gráfico
st.title('Gerador de Gráfico')
st.write("Selecione as colunas para o gráfico:")
coluna_categoria = st.selectbox("Selecione a coluna de categoria", dados_nascimentos.columns, key='coluna_categoria')
coluna_valor = st.selectbox("Selecione a coluna de valor", dados_nascimentos.columns, key='coluna_valor')

def plot_grafico(df, categoria_col, valor_col):
    df[categoria_col] = df[categoria_col].astype(str)
    chart = alt.Chart(df).mark_bar().encode(
        x=categoria_col,
        y=valor_col,
        tooltip=[categoria_col, valor_col]
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

if st.button("Gerar Gráfico"):
    if coluna_categoria in dados_nascimentos.columns and coluna_valor in dados_nascimentos.columns:
        plot_grafico(dados_nascimentos, coluna_categoria, coluna_valor)
    else:
        st.error("Selecione colunas válidas para o gráfico.")

# Espaço reservado para GIF no final
st.title('Por hoje é isso!✌')
custom_height = 300  
st.markdown(f'<img src="https://i.kym-cdn.com/photos/images/newsfeed/002/054/274/08a.gif" style="width:100%; height:{custom_height}px;">', unsafe_allow_html=True)

# Sugestões de Melhoria/ Solicitações
with st.expander('Sugestões de Melhoria/ Solicitações'):
    lista_tarefas = []
    tarefa = st.text_input("Digite")
    if st.button("Adicionar") and tarefa:
        lista_tarefas.append(tarefa)
    st.write("Lista:")
    for i, tarefa in enumerate(lista_tarefas, start=1):
        st.text(f"{i}. {tarefa}")