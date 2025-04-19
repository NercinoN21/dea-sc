from pulp import *
import pandas as pd

def calcular_eficiencia_crs_pulp(df_municipios, municipio_nome):
    dados_aval = df_municipios[df_municipios['Município'] == municipio_nome].iloc[0]
    gasto_aval = dados_aval['gasto_per_capita']
    ideb_aval = dados_aval['ideb_2019']

    municipios_nomes = df_municipios['Município'].tolist()

    prob = LpProblem(f"DEA_CRS_Output_{municipio_nome}", LpMaximize)

    u = LpVariable("u_IDEB", lowBound=0)
    v = LpVariable("v_Gasto", lowBound=0)

    prob += u * ideb_aval

    prob += v * gasto_aval == 1

    for index, row in df_municipios.iterrows():
        gasto_j = row['gasto_per_capita']
        ideb_j = row['ideb_2019']
        prob += u * ideb_j <= v * gasto_j

    prob.solve(PULP_CBC_CMD(msg=False))

    if LpStatus[prob.status] == "Optimal":
        return value(prob.objective)
    else:
        return None

def calcular_eficiencia_vrs_pulp(df_municipios, municipio_nome):
    """
    Calcula a eficiência DEA com retornos variáveis de escala (VRS) para um município.
    
    Args:
        df_municipios: DataFrame com os dados dos municípios
        municipio_nome: Nome do município a ser avaliado
        
    Returns:
        float: Score de eficiência VRS
    """
    dados_aval = df_municipios[df_municipios['Município'] == municipio_nome].iloc[0]
    gasto_aval = dados_aval['gasto_per_capita']
    ideb_aval = dados_aval['ideb_2019']

    municipios_nomes = df_municipios['Município'].tolist()

    prob = LpProblem(f"DEA_VRS_Output_{municipio_nome}", LpMaximize)

    u = LpVariable("u_IDEB", lowBound=0)
    v = LpVariable("v_Gasto", lowBound=0)
    w = LpVariable("w", lowBound=None)  # Variável livre para VRS

    prob += u * ideb_aval + w

    prob += v * gasto_aval == 1

    for index, row in df_municipios.iterrows():
        gasto_j = row['gasto_per_capita']
        ideb_j = row['ideb_2019']
        prob += u * ideb_j + w <= v * gasto_j

    prob.solve(PULP_CBC_CMD(msg=False))

    if LpStatus[prob.status] == "Optimal":
        return value(prob.objective)
    else:
        return None

