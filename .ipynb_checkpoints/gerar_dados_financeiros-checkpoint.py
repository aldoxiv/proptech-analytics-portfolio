import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuração de semente para reproducibilidade dos dados
np.random.seed(42)

# ---- 1. GERAÇÃO DA DIMENSÃO PRODUTOS ----
# Correção efetuada na linha abaixo adicionando a lista de IDs
produtos_dados = {
    'ID_Produto': [101, 102, 103, 104],
    'Nome_Produto': ['Credito Pessoal', 'Cambio', 'Credito Consignado', 'Financiamento PJ'],
    'Taxa_Margem_Nativa': [0.12, 0.02, 0.06, 0.08]
}
dProdutos = pd.DataFrame(produtos_dados)

# ---- 2. GERAÇÃO DA DIMENSÃO CLIENTES ----
n_clientes = 250
segmentos = ['Varejo', 'Alta Renda', 'Corporate']
regioes = ['SP - Capital', 'SP - Interior', 'RJ', 'MG', 'DF']

dClientes = pd.DataFrame({
    'ID_Cliente': range(1001, 1001 + n_clientes),
    'Segmento': np.random.choice(segmentos, n_clientes, p=[0.60, 0.30, 0.10]),
    'Regiao': np.random.choice(regioes, n_clientes),
    'Data_Abertura_Conta': [datetime(2025, 1, 1) + timedelta(days=int(np.random.randint(0, 365))) for _ in range(n_clientes)]
})

# ---- 3. GERAÇÃO DA TABELA FATO OPERAÇÕES ----
n_transacoes = 5000
datas_fato = [datetime(2025, 1, 1) + timedelta(days=int(np.random.randint(0, 365))) for _ in range(n_transacoes)]

# Listas auxiliares para construção lógica da Fato
clientes_f = np.random.choice(dClientes['ID_Cliente'], n_transacoes)
produtos_f = np.random.choice(dProdutos['ID_Produto'], n_transacoes, p=[0.40, 0.20, 0.30, 0.10])
valores_f = []
status_f = []
dias_atraso_f = []
ratings_f = []

# Definição lógica baseada no tipo de produto
for prod in produtos_f:
    if prod == 101:  # Crédito Pessoal (Risco maior, ticket médio menor)
        valores_f.append(round(np.random.exponential(5000) + 1000, 2))
        rating = np.random.choice(['B', 'C', 'D', 'E'], p=[0.40, 0.30, 0.20, 0.10])
    elif prod == 102:  # Câmbio (Risco baixíssimo, volume alto)
        valores_f.append(round(np.random.normal(50000, 15000), 2))
        rating = np.random.choice(['A', 'B'], p=[0.85, 0.15])
    elif prod == 103:  # Consignado (Risco muito baixo, ticket médio)
        valores_f.append(round(np.random.normal(15000, 4000), 2))
        rating = np.random.choice(['A', 'B', 'C'], p=[0.70, 0.20, 0.10])
    else:  # Financiamento PJ (Ticket muito alto, risco moderado)
        valores_f.append(round(np.random.exponential(150000) + 20000, 2))
        rating = np.random.choice(['B', 'C', 'D', 'E', 'F'], p=[0.30, 0.40, 0.15, 0.10, 0.05])
    
    ratings_f.append(rating)

    # Regra de negócio para Inadimplência correlacionada ao Rating de Risco
    if rating in ['A', 'B']:
        status = np.random.choice(['Liquidado', 'Em Dia', 'Em Atraso'], p=[0.45, 0.53, 0.02])
    elif rating in ['C', 'D']:
        status = np.random.choice(['Liquidado', 'Em Dia', 'Em Atraso'], p=[0.30, 0.60, 0.10])
    else:  # E, F (Alto risco)
        status = np.random.choice(['Liquidado', 'Em Dia', 'Em Atraso'], p=[0.10, 0.50, 0.40])
    
    status_f.append(status)

    # Determinação dos dias de atraso se o status for 'Em Atraso'
    if status == 'Em Atraso':
        if rating in ['E', 'F']:
            dias_atraso_f.append(int(np.random.randint(60, 180)))
        else:
            dias_atraso_f.append(int(np.random.randint(1, 90)))
    else:
        dias_atraso_f.append(0)

dFatos_Operacoes = pd.DataFrame({
    'ID_Transacao': range(500001, 500001 + n_transacoes),
    'ID_Cliente': clientes_f,
    'ID_Produto': produtos_f,
    'Data': datas_fato,
    'Valor_Transacao': valores_f,
    'Status_Pagamento': status_f,
    'Dias_Atraso': dias_atraso_f,
    'Rating_Risco': ratings_f
})

# ---- 4. GERAÇÃO DA DIMENSÃO CALENDÁRIO ----
data_min = min(datas_fato).replace(month=1, day=1)
data_max = max(datas_fato).replace(month=12, day=31)
datas_periodo = pd.date_range(start=data_min, end=data_max)

dCalendario = pd.DataFrame({
    'Data': datas_periodo,
    'Ano': datas_periodo.year,
    'Mes': datas_periodo.month,
    'Trimestre': datas_periodo.quarter,
    'Dia_Util': np.where(datas_periodo.dayofweek < 5, 1, 0)
})

# ---- 5. SALVANDO OS ARQUIVOS COM SEGURANÇA ----
dProdutos.to_csv('dProdutos.csv', index=False, encoding='utf-8-sig')
dClientes.to_csv('dClientes.csv', index=False, encoding='utf-8-sig')
dFatos_Operacoes.to_csv('fFatos_Operacoes.csv', index=False, encoding='utf-8-sig')
dCalendario.to_csv('dCalendario.csv', index=False, encoding='utf-8-sig')

print("Massa de dados financeiros gerada com sucesso em arquivos .csv!")
