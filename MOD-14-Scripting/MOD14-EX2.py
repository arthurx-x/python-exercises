# Importando bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Configuração do tema do Seaborn
sns.set_theme()

def gerar_grafico_e_salvar(sinasc, valor, indice, funcao_agregacao, rotulo_y, rotulo_x, opcao, nome_arquivo):
    # Criar tabela dinâmica
    dados_grafico = pd.pivot_table(data=sinasc, values=valor, index=indice, aggfunc=funcao_agregacao)

    # Aplicar opções de ordenação ou desempilhamento
    if opcao == 'sort':
        dados_grafico = dados_grafico.sort_values(valor)
    elif opcao == 'unstack':
        dados_grafico = dados_grafico.unstack()

    # Plotar e salvar o gráfico
    dados_grafico.plot()
    plt.ylabel(rotulo_y)
    plt.xlabel(rotulo_x)
    plt.savefig(nome_arquivo)
    plt.close()

# Iterar sobre os meses fornecidos como argumentos do sistema
for mes in sys.argv[1:]:
    # Ler o arquivo CSV correspondente ao mês
    sinasc = pd.read_csv(f'SINASC_RO_2019_{mes}.csv')
    
    # Obter a data máxima para criar diretório de saída
    max_data = sinasc.DTNASC.max()[:7]
    os.makedirs(f'./output/figs/{max_data}', exist_ok=True)

    # Gerar e salvar gráficos específicos
    gerar_grafico_e_salvar(sinasc, 'IDADEMAE', 'DTNASC', 'count', 'Quantidade de nascimentos',
                           'Data de nascimento', 'nenhuma', f'./output/figs/{max_data}/Quantidade de nascimentos.png')

    gerar_grafico_e_salvar(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'Média da idade das mães',
                           'Data de nascimento', 'unstack', f'./output/figs/{max_data}/Média da idade das mães por sexo.png')

    gerar_grafico_e_salvar(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'Média do peso dos bebês',
                           'Data de nascimento', 'unstack', f'./output/figs/{max_data}/Média do peso dos bebês por sexo.png')

    gerar_grafico_e_salvar(sinasc, 'APGAR1', 'ESCMAE', 'median', 'Mediana do APGAR1',
                           'Escolaridade', 'sort', f'./output/figs/{max_data}/Mediana do APGAR1 por escolaridade das mães.png')

    gerar_grafico_e_salvar(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'Média do APGAR1',
                           'Gestação', 'sort', f'./output/figs/{max_data}/Média do APGAR1 por gestação.png')

    gerar_grafico_e_salvar(sinasc, 'APGAR5', 'GESTACAO', 'mean', 'Média do APGAR5',
                           'Gestação', 'sort', f'./output/figs/{max_data}/Média do APGAR5 por gestação.png')

    # Imprimir informações sobre as datas
    print('Data inicial:', sinasc.DTNASC.min())
    print('Data final:', sinasc.DTNASC.max())
    print('Nome da pasta:', max_data, '\n')