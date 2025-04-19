# Análise de Eficiência dos Municípios de Santa Catarina usando DEA

Este projeto realiza uma análise de eficiência dos municípios do estado de Santa Catarina utilizando a metodologia DEA (Data Envelopment Analysis). O objetivo é avaliar a eficiência relativa dos municípios na transformação de recursos financeiros (gastos per capita) em resultados educacionais (IDEB).

## Estrutura do Projeto

```
.
├── data_input/              # Diretório com os dados de entrada
│   ├── BR_Municipios_2023.* # Shapefile dos municípios
│   ├── Gastos_2019.xlsx    # Dados de gastos 2019
│   └── IDEB_2019.xlsx      # Dados do IDEB 2019
│
├── data_output/            # Diretório com os resultados
│   ├── distribuicao_escores.png      # Gráfico de distribuição
│   ├── elevacao_necessaria.png       # Gráfico de elevação necessária
│   ├── fronteira_eficiencia.png      # Gráfico da fronteira
│   ├── mapa_eficiencia.png           # Mapa de eficiência
│   ├── resultados_dea.csv            # Resultados da análise DEA
|   |── resumo_categorias.xlsx        # Resultado da análise DEA por categoria
│   ├── top_10_mais_eficientes.xlsx   # Top 10 municípios eficientes
│   └── top_10_menos_eficientes.xlsx  # Top 10 municípios ineficientes
│
├── src/                    # Código fonte
│   ├── read_data.py       # Leitura e processamento dos dados
│   ├── dea.py             # Implementação do DEA
│   ├── main.py            # Script principal
│   └── analise_dea.py     # Análises e visualizações
│
├── requirements.txt        # Dependências do projeto
└── README.md              # Este arquivo
```

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Uso

1. Clone o repositório:
```bash
git clone https://github.com/NercinoN21/dea-sc
cd dea-sc
```

2. Crie e ative o ambiente virtual(Opcional, mas recomendado):
```bash
python -m venv venv

source venv/bin/activate # Para Linux e Mac
venv\Scripts\activate # Para cmd.exe (Prompt de Comando)
venv\Scripts\Activate.ps1 # Para PowerShell (Opção 1)
.\venv\Scripts\Activate.ps1 # Para PowerShell (Opção 2)
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o comando abaixo:
```bash
python src/main.py
```

## Análises Realizadas

O projeto gera as seguintes análises e visualizações:

1. **Fronteira de Eficiência**
   - Gráfico de dispersão mostrando a relação entre gasto per capita e IDEB
   - Identificação dos municípios na fronteira de eficiência

2. **Municípios que Precisam Elevar o IDEB**
   - Ranking dos municípios que necessitam maior elevação no IDEB
   - Cálculo do IDEB necessário para alcançar a eficiência

3. **Distribuição dos Escores**
   - Histogramas da distribuição dos escores CRS e VRS
   - Análise da dispersão da eficiência

4. **Rankings de Eficiência**
   - Top 10 municípios mais eficientes
   - Top 10 municípios menos eficientes
   - Comparação entre CRS e VRS

5. **Mapa de Eficiência**
   - Visualização espacial da eficiência por município
   - Mapas separados para CRS e VRS

## Metodologia

O projeto utiliza a metodologia DEA com as seguintes características:

- **Orientação**: Output-oriented (maximização do IDEB)
- **Retornos de Escala**: 
  - CRS (Constant Returns to Scale)
  - VRS (Variable Returns to Scale)
- **Input**: Gasto per capita
- **Output**: IDEB 2019

## Resultados

Os resultados são salvos no diretório `data_output/`:
- `resultados_dea.csv`: Tabela com todos os scores de eficiência
- `fronteira_eficiencia.png`: Gráfico da fronteira de eficiência
- `elevacao_necessaria.png`: Gráfico de elevação necessária no IDEB
- `distribuicao_escores.png`: Histogramas dos escores
- `mapa_eficiencia.png`: Mapas de eficiência por município
- `resumo_categorias.xlsx`: 
- `top_10_mais_eficientes.xlsx`: Lista dos municípios mais eficientes
- `top_10_menos_eficientes.xlsx`: Lista dos municípios menos eficientes

## Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue para discutir mudanças propostas ou envie um pull request.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Referências

- Charnes, A., Cooper, W. W., & Rhodes, E. (1978). Measuring the efficiency of decision making units. European Journal of Operational Research, 2(6), 429-444.
- Banker, R. D., Charnes, A., & Cooper, W. W. (1984). Some models for estimating technical and scale inefficiencies in data envelopment analysis. Management Science, 30(9), 1078-1092. 