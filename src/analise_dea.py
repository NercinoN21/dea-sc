import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import seaborn as sns

def analisar_resultados(df_resultados):
    """
    Realiza análises detalhadas dos resultados do DEA.
    
    Args:
        df_resultados: DataFrame com os resultados do DEA
    """
    # 1. Fronteira de eficiência
    plot_fronteira_eficiencia(df_resultados)
    
    # 2. Municípios que precisam elevar o IDEB
    plot_municipios_ineficientes(df_resultados)
    
    # 3. Escores de eficiência
    plot_distribuicao_escores(df_resultados)
    
    # 4. Top 10 mais e menos eficientes
    excel_top_municipios(df_resultados)
    
    # 5. Mapa de eficiência
    plot_mapa_eficiencia(df_resultados)

def plot_fronteira_eficiencia(df):
    """Plota a fronteira de eficiência."""
    plt.figure(figsize=(10, 6))
    
    eficientes = df[df['Eficiência CRS'] >= 0.95]
    plt.scatter(eficientes['gasto_per_capita'], eficientes['ideb_2019'], 
                color='green', label='Fronteira de Eficiência')
    
    plt.scatter(df['gasto_per_capita'], df['ideb_2019'], 
                color='blue', alpha=0.5, label='Demais Municípios')
    
    plt.xlabel('Gasto per capita (R$)')
    plt.ylabel('IDEB 2019')
    plt.title('Fronteira de Eficiência DEA')
    plt.legend()
    plt.grid(True)
    plt.savefig('data_output/fronteira_eficiencia.png')
    plt.close()

def categorizar_ineficiencia(percentual_aumento):
    """
    Categoriza o nível de ineficiência baseado no percentual de aumento necessário no IDEB.
    
    Args:
        percentual_aumento: Percentual de aumento necessário no IDEB
    
    Returns:
        str: Categoria de ineficiência (Eficiente, Leve, Moderada, Grave ou Crítica)
    """
    if percentual_aumento <= 5:  # Ajustado para considerar pequenas variações como eficiente
        return 'Eficiente'
    elif percentual_aumento <= 20:
        return 'Leve'
    elif percentual_aumento <= 50:
        return 'Moderada'
    elif percentual_aumento <= 100:
        return 'Grave'
    else:
        return 'Crítica'

def plot_municipios_ineficientes(df):
    """Plota municípios que precisam elevar o IDEB."""
    df['ideb_necessario'] = df.apply(
        lambda row: row['ideb_2019'] * (1/row['Eficiência CRS'])
        if row['Eficiência CRS'] > 0 and row['Eficiência CRS'] < 1
        else row['ideb_2019'],
        axis=1
    )
    
    # Limita o IDEB necessário a 10 (nota máxima possível)
    df['ideb_necessario'] = df['ideb_necessario'].apply(lambda x: min(x, 10))
    
    df['elevacao_necessaria'] = df['ideb_necessario'] - df['ideb_2019']
    
    df['percentual_aumento'] = (df['elevacao_necessaria'] / df['ideb_2019']) * 100
    
    df['categoria_ineficiencia'] = df['percentual_aumento'].apply(categorizar_ineficiencia)
    
    contagem_categorias = df['categoria_ineficiencia'].value_counts().sort_index()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    
    top_10_ineficientes = df.nlargest(10, 'elevacao_necessaria')
    bars = ax1.barh(top_10_ineficientes['Município'], 
                    top_10_ineficientes['elevacao_necessaria'])
    ax1.set_xlabel('Elevação necessária no IDEB')
    ax1.set_title('Top 10 Municípios que Precisam Maior Elevação no IDEB')
    
    for i, bar in enumerate(bars):
        categoria = top_10_ineficientes.iloc[i]['categoria_ineficiencia']
        percentual = top_10_ineficientes.iloc[i]['percentual_aumento']
        ideb_atual = top_10_ineficientes.iloc[i]['ideb_2019']
        ideb_nec = top_10_ineficientes.iloc[i]['ideb_necessario']
        ax1.text(bar.get_width(), bar.get_y() + bar.get_height()/2, 
                f'  {categoria} ({percentual:.1f}%) - IDEB: {ideb_atual:.1f} → {ideb_nec:.1f}', 
                va='center')
    
    cores = {'Eficiente': 'green', 'Leve': 'lightgreen', 
             'Moderada': 'yellow', 'Grave': 'orange', 'Crítica': 'red'}
    bars = ax2.bar(contagem_categorias.index, contagem_categorias.values, 
                   color=[cores[cat] for cat in contagem_categorias.index])
    ax2.set_title('Distribuição dos Municípios por Categoria de Ineficiência')
    ax2.set_ylabel('Número de Municípios')
    
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('data_output/elevacao_necessaria.png')
    plt.close()
    
    resumo_categorias = df.groupby('categoria_ineficiencia').agg({
        'Município': 'count',
        'ideb_2019': ['mean', 'min', 'max'],
        'ideb_necessario': ['mean', 'min', 'max'],
        'elevacao_necessaria': ['mean', 'min', 'max'],
        'percentual_aumento': ['mean', 'min', 'max']
    }).round(2)
    
    resumo_categorias.columns = [
        'Quantidade de Municípios',
        'IDEB Médio', 'IDEB Mínimo', 'IDEB Máximo',
        'IDEB Necessário Médio', 'IDEB Necessário Mínimo', 'IDEB Necessário Máximo',
        'Elevação Necessária Média', 'Elevação Mínima', 'Elevação Máxima',
        'Percentual Médio', 'Percentual Mínimo', 'Percentual Máximo'
    ]
    
    resumo_categorias.to_excel('data_output/resumo_categorias.xlsx')

def plot_distribuicao_escores(df):
    """Plota a distribuição dos escores de eficiência."""
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    sns.histplot(df['Eficiência CRS'], kde=True)
    plt.title('Distribuição dos Escores CRS')
    
    plt.subplot(1, 2, 2)
    sns.histplot(df['Eficiência VRS'], kde=True)
    plt.title('Distribuição dos Escores VRS')
    
    plt.tight_layout()
    plt.savefig('data_output/distribuicao_escores.png')
    plt.close()

def excel_top_municipios(df):
    """Exporta os 10 mais e menos eficientes para um arquivo Excel."""

    df_top_10 = df.sort_values(by='Eficiência CRS', ascending=False).head(10)

    df_bottom_10 = df.sort_values(by='Eficiência CRS', ascending=True).head(10)
    
    df_top_10.to_excel('data_output/top_10_mais_eficientes.xlsx', index=False)
    df_bottom_10.to_excel('data_output/top_10_menos_eficientes.xlsx', index=False)

def plot_mapa_eficiencia(df):
    """Plota mapa com a distribuição espacial da eficiência."""
    try:
        df['COD_MUN'] = df['COD_MUN'].astype(str)
        
        sc = gpd.read_file('data_input/SC_Municipios_2023.shp')
        
        sc = sc.merge(df, left_on='CD_MUN', right_on='COD_MUN')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        
        sc.plot(column='Eficiência CRS', cmap='RdYlGn', 
                legend=True, ax=ax1)
        ax1.set_title('Eficiência CRS por Município')
        
        sc.plot(column='Eficiência VRS', cmap='RdYlGn', 
                legend=True, ax=ax2)
        ax2.set_title('Eficiência VRS por Município')
        
        plt.tight_layout()
        plt.savefig('data_output/mapa_eficiencia.png')
        plt.close()
    except Exception as e:
        print(f"Erro ao gerar mapa: {str(e)}")
        print("Certifique-se de que o shapefile está disponível em data/BR_Municipios_2022.shp")

if __name__ == '__main__':
    df_resultados = pd.read_csv('resultados_dea.csv')
    analisar_resultados(df_resultados) 