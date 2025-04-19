from read_data import get_data
from dea import calcular_eficiencia_crs_pulp, calcular_eficiencia_vrs_pulp
import pandas as pd
from analise_dea import analisar_resultados

def main():
    """
    Função principal que executa o processo de cálculo da eficiência DEA.
    """
    df = get_data()

    municipios = df['Município'].tolist()

    # Calcula eficiência CRS
    scores_crs = {}
    for municipio in municipios:
        score = calcular_eficiencia_crs_pulp(df, municipio)
        scores_crs[municipio] = score

    # Calcula eficiência VRS
    scores_vrs = {}
    for municipio in municipios:
        score = calcular_eficiencia_vrs_pulp(df, municipio)
        scores_vrs[municipio] = score

    df_resultados = pd.DataFrame({
        'Município': municipios,
        'Eficiência CRS': [scores_crs[m] for m in municipios],
        'Eficiência VRS': [scores_vrs[m] for m in municipios]
    })

    df_resultados['COD_MUN'] = df['COD_MUN']

    df_resultados['Escala de Eficiência'] = df_resultados['Eficiência CRS'] / df_resultados['Eficiência VRS']

    df_resultados = df_resultados.merge(df[['Município', 'gasto_per_capita', 'ideb_2019']], on='Município')

    df_resultados.sort_values(by='Eficiência CRS', ascending=False, inplace=True)

    df_resultados =  df_resultados.dropna(subset=['Eficiência CRS', 'Eficiência VRS', 'Escala de Eficiência'])

    df_resultados.to_csv('data_output/resultados_dea.csv', index=False)

    analisar_resultados(df_resultados)

if __name__ == '__main__':
    main()