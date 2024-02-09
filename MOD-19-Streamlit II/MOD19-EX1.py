# Importando bibliotecass
import timeit
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Configuração do tema do seaborn
sns.set_theme(style='ticks', rc={'axes.spines.right': False, 'axes.spines.top': False})

# Define os caminhos dos arquivos como variáveis
branding_image_path = r"C:\Users\Arthu\OneDrive\Área de Trabalho\Data Science\notebooks\bank_branding.jpg"
data_file_path = r'C:\Users\Arthu\OneDrive\Área de Trabalho\Data Science\notebooks\bank-additional-full.csv'

# Função para carregar dados
@st.cache_data
def carregar_dados(caminho_arquivo: str, sep: str) -> pd.DataFrame:
    return pd.read_csv(caminho_arquivo, sep=sep)

# Função para filtro multisseleção
def filtro_multisselecao(dados: pd.DataFrame, coluna: str, selecionados: list[str]) -> pd.DataFrame:
    return dados if 'all' in selecionados else dados[dados[coluna].isin(selecionados)].reset_index(drop=True)

# Função para aplicar filtros
def aplicar_filtros(banco, idades, filtros_selecionados):
    for col in ['job', 'marital', 'default', 'housing', 'loan', 'contact', 'month', 'day_of_week']:
        banco = banco.pipe(filtro_multisselecao, col, filtros_selecionados[col])

    return banco.query('age.between(@idades[0], @idades[1])')

def main():
    # Configuração da página
    st.set_page_config("Análise de Telemarketing 📊", layout="wide", initial_sidebar_state="expanded")

    # Exibição de imagem de marca na barra lateral
    st.sidebar.image(image=Image.open(fp=branding_image_path))

    # Título principal e separador
    st.write('# Análise de Telemarketing 📈')
    st.markdown(body='---')

    # Medindo o tempo de execução
    with st.spinner("Carregando dados..."):
        inicio = timeit.default_timer()
        banco_bruto = carregar_dados(data_file_path, sep=';')
        banco = banco_bruto.copy()

    # Exibindo o tempo de execução
    elapsed_time = round(timeit.default_timer() - inicio, 2)
    st.write('Tempo de Execução:', f'{elapsed_time:.2f}', 'segundos')

    # Exibindo informações dos dados brutos
    st.write('## Antes dos Filtros 📊')
    st.write(banco_bruto)
    st.write('Quantidade de Linhas:', banco_bruto.shape[0])
    st.write('Quantidade de Colunas:', banco_bruto.shape[1])

    # Formulário na barra lateral para filtros
    with st.sidebar.form(key='meu_formulario'):
        # Slider para idade
        idade_minima, idade_maxima = banco['age'].min(), banco['age'].max()
        idades = st.slider(label='Idade', min_value=idade_minima, max_value=idade_maxima, value=(idade_minima, idade_maxima), step=1)

        # Filtros de multisseleção para várias colunas
        filtros_selecionados = {}
        for col in ['job', 'marital', 'default', 'housing', 'loan', 'contact', 'month', 'day_of_week']:
            opcoes = banco[col].unique().tolist() + ['all']
            filtros_selecionados[col] = st.multiselect(label=col.capitalize(), options=opcoes, default=['all'])

        # Aplicar filtros nos dados
        banco = aplicar_filtros(banco, idades, filtros_selecionados)

        # Botão de envio para aplicar filtros
        botao_enviar = st.form_submit_button(label='Aplicar')

    # Exibindo informações dos dados filtrados
    st.write('## Após os Filtros 📊')
    st.write(banco)
    st.write('Quantidade de Linhas:', banco.shape[0])
    st.write('Quantidade de Colunas:', banco.shape[1])

    # Separador
    st.markdown('---')

    # Gráficos para dados brutos e filtrados
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
    chart_titles = ['Dados Brutos', 'Dados Filtrados']

    for i, dados in enumerate([banco_bruto, banco]):
        pct_alvo = dados['y'].value_counts(normalize=True).sort_index() * 100
        sns.barplot(x=pct_alvo.index, y=pct_alvo.values, ax=axes[i])
        axes[i].bar_label(axes[i].containers[0], fmt='%.1f%%')  # Exibindo valores em porcentagem
        axes[i].set_title(label=chart_titles[i], fontweight='bold')

    # Exibindo proporção de aceitação
    st.write('## Proporção de Aceite 📊')
    st.pyplot(plt)

if __name__ == '__main__':
    main()