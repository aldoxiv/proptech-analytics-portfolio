import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Configuração de semente para garantir a reproducibilidade dos dados
np.random.seed(42)

# ---- 1. GERAÇÃO DA DIMENSÃO SISTEMAS CRÍTICOS ----
sistemas_dados = {
    'ID_Sistema': [501, 502, 503, 504],
    'Sistema_Critico': ['Pix & Canais Digitais', 'Banco de Dados Central', 'Esteira de Credito PJ', 'Mensageria Swift (Cambio)'],
    'Custo_Minuto_Downtime': [8500.00, 12000.00, 4500.00, 6000.00],
    'SLA_Contratual_Mensal_Min': [30, 15, 60, 45]
}
dSistemas = pd.DataFrame(sistemas_dados)

# ---- 2. GERAÇÃO DA TABELA FATO INCIDENTES (HISTÓRICO OPERACIONAL) ----
n_incidentes = 400
datas_incidentes = [datetime(2026, 1, 1) + timedelta(days=int(np.random.randint(0, 260))) for _ in range(n_incidentes)]

sistemas_f = np.random.choice(dSistemas['ID_Sistema'], n_incidentes, p=[0.40, 0.25, 0.20, 0.15])
duracao_minutos_f = []
causa_raiz_f = []

for sys in sistemas_f:
    if sys == 501:
        duracao_minutos_f.append(int(np.random.exponential(scale=8) + 2))
        causa_raiz_f.append(np.random.choice(['Instabilidade de API', 'Estouro de Timeout', 'Falha de Autenticacao'], p=[0.50, 0.30, 0.20]))
    elif sys == 502:
        duracao_minutos_f.append(int(np.random.exponential(scale=25) + 5))
        causa_raiz_f.append(np.random.choice(['Lock de Tabelas', 'Overload de CPU', 'Falha de Hardware'], p=[0.60, 0.30, 0.10]))
    else:
        duracao_minutos_f.append(int(np.random.randint(5, 45)))
        causa_raiz_f.append(np.random.choice(['Erro de Deploy', 'Timeout de Rede', 'Manutencao Emergencial']))

fFatos_Incidentes = pd.DataFrame({
    'ID_Incidente': [f"INC-{i}" for i in range(10001, 10001 + n_incidentes)],
    'ID_Sistema': sistemas_f,
    'Data_Ocorrencia': datas_incidentes,
    'Downtime_Minutos': duracao_minutos_f,
    'Causa_Raiz': causa_raiz_f
})

# ---- 3. SALVAMENTO ADAPTADO PARA SISTEMAS PT-BR (POWER BI) ----
pasta_destino = os.path.join('..', 'dados', 'processed')
if not os.path.exists(os.path.join('..', 'dados')) and os.path.exists('dados'):
    pasta_destino = os.path.join('dados', 'processed')

os.makedirs(pasta_destino, exist_ok=True)

dSistemas.to_csv(os.path.join(pasta_destino, 'dSistemas.csv'), index=False, sep=';', decimal=',', encoding='utf-8-sig')
fFatos_Incidentes.to_csv(os.path.join(pasta_destino, 'fFatos_Incidentes.csv'), index=False, sep=';', decimal=',', encoding='utf-8-sig')

print("Massa de dados de SLA Tecnológico gerada com sucesso para Power BI PT-BR!")
