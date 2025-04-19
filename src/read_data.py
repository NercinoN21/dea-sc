from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def read_ideb_2019_excel() -> pd.DataFrame:
    """
    Lê e processa os dados do IDEB 2019 para o estado de Santa Catarina.

    Returns:
        pd.DataFrame: DataFrame contendo os dados do IDEB processados
    """
    try:
        file_path = Path('data_input/IDEB_2019.xlsx')
        if not file_path.exists():
            raise FileNotFoundError(f'Arquivo {file_path} não encontrado')

        df = pd.read_excel(
            file_path, sheet_name='Planilha1', skiprows=7, usecols='A:H'
        )

        colunas_vl = [col for col in df.columns if col.startswith('VL')]
        for coluna in colunas_vl:
            df[coluna] = pd.to_numeric(
                df[coluna].replace(['ND', '-'], 0.0), errors='coerce'
            ).fillna(0.0)

        df['CO_MUNICIPIO'] = df['CO_MUNICIPIO'].astype(str)
        df['CO_UF'] = df['CO_MUNICIPIO'].str[:2]

        # Filtra apenas Santa Catarina (UF 42)
        df = df[df['CO_UF'] == '42'].copy()

        df = df.rename(columns={'CO_MUNICIPIO': 'COD_MUN', 'CO_UF': 'UF'})
        df = df[['COD_MUN'] + colunas_vl]

        return df

    except Exception as e:
        raise Exception(f'Erro ao processar dados do IDEB: {str(e)}')


def read_gastos_2019_excel() -> pd.DataFrame:
    """
    Lê e processa os dados de gastos de 2019.

    Returns:
        pd.DataFrame: DataFrame contendo os dados de gastos processados
    """
    try:
        file_path = Path('data_input/Gastos_2019.xlsx')
        if not file_path.exists():
            raise FileNotFoundError(f'Arquivo {file_path} não encontrado')

        df = pd.read_excel(file_path, sheet_name='Planilha1', usecols='A:F')
        df = df.query('UF == "SC"')

        df['COD_MUN'] = df['COD_MUN'].astype(str)

        return df

    except Exception as e:
        raise Exception(f'Erro ao processar dados de gastos: {str(e)}')


def get_data() -> pd.DataFrame:
    """
    Combina os dados do IDEB e gastos em um único DataFrame.

    Returns:
        pd.DataFrame: DataFrame combinado com dados do IDEB e gastos
    """
    try:
        ideb = read_ideb_2019_excel()
        gastos = read_gastos_2019_excel()

        df_final = ideb.merge(gastos, on='COD_MUN', how='left')
        df_final['gasto_per_capita'] = (
            df_final['Valor do gasto (R$)'] / df_final['População']
        )
        df_final.rename(
            columns={'VL_OBSERVADO_2019': 'ideb_2019'}, inplace=True
        )

        return df_final[['Município', 'COD_MUN', 'ideb_2019', 'gasto_per_capita']]

    except Exception as e:
        raise Exception(f'Erro ao combinar dados: {str(e)}')


if __name__ == '__main__':
    try:
        df = get_data()
        print('Dados processados com sucesso!')
        print(f'Total de registros: {len(df)}')
        print(df.head())
        breakpoint()
    except Exception as e:
        print(f'Erro: {str(e)}')
