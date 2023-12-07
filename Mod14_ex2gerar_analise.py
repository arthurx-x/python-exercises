import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

sns.set_theme()

def plot_and_save(sinasc, value, index, func, ylabel, xlabel, opcao, filename):
    plot_data = pd.pivot_table(data=sinasc, values=value, index=index, aggfunc=func)

    if opcao == 'sort':
        plot_data = plot_data.sort_values(value)
    elif opcao == 'unstack':
        plot_data = plot_data.unstack()

    plot_data.plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.savefig(filename)
    plt.close()

for mes in sys.argv[1:]:
    sinasc = pd.read_csv(f'SINASC_RO_2019_{mes}.csv')
    max_data = sinasc.DTNASC.max()[:7]
    os.makedirs(f'./output/figs/{max_data}', exist_ok=True)

    plot_and_save(sinasc, 'IDADEMAE', 'DTNASC', 'count', 'Quantidade de nascimentos',
                  'Data de nascimento', 'nenhuma', f'./output/figs/{max_data}/Quantidade de nascimentos.png')

    plot_and_save(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'Média da idade das mães',
                  'Data de nascimento', 'unstack', f'./output/figs/{max_data}/Média da idade das mães por sexo.png')

    plot_and_save(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'Média do peso dos bebês',
                  'Data de nascimento', 'unstack', f'./output/figs/{max_data}/Média do peso dos bebês por sexo.png')

    plot_and_save(sinasc, 'APGAR1', 'ESCMAE', 'median', 'Mediana do APGAR1',
                  'Escolaridade', 'sort', f'./output/figs/{max_data}/Mediana do APGAR1 por escolaridade das mães.png')

    plot_and_save(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'Média do APGAR1',
                  'Gestação', 'sort', f'./output/figs/{max_data}/Média do APGAR1 por gestação.png')

    plot_and_save(sinasc, 'APGAR5', 'GESTACAO', 'mean', 'Média do APGAR5',
                  'Gestação', 'sort', f'./output/figs/{max_data}/Média do APGAR5 por gestação.png')

    print('Data inicial:', sinasc.DTNASC.min())
    print('Data final:', sinasc.DTNASC.max())
    print('Nome da pasta:', max_data, '\n')
