import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Configuração de semente para garantir a reproducibilidade dos dados
np.random.seed(42)

# ---- 1. GERAÇÃO DA BASE IMOBILIÁRIA CALIBRADA (VALORES REAIS BRASIL) ----
n_imoveis = 600

# Áreas realistas distribuídas entre 40m² e 220m²
areas_base = np.random.normal(loc=85, scale=30, size=n_imoveis).clip(40, 220)

# Preço por m² realista de mercado entre R$ 5.500 e R$ 11.500
valor_m2 = np.random.uniform(5500, 11500, size=n_imoveis)
precos_venda = areas_base * valor_m2

# Score de prospecção fixado estritamente na escala de 0,00 a 100,00
score_prospeccao = np.random.uniform(15, 98, size=n_imoveis)

df_imoveis = pd.DataFrame({
    'ID_Imovel': [f"IMOB-{i}" for i in range(80001, 80001 + n_imoveis)], # ID já nasce como Texto
    'Area_m2': np.round(areas_base, 2),
    'Preco_Venda_R$': np.round(precos_venda, 2),
    'Score_Prospeccao': np.round(score_prospeccao, 2)
})

# ---- 2. PRÉ-PROCESSAMENTO (Z-SCORE PARA O K-MEANS) ----
padronizador = StandardScaler()
dados_padronizados = padronizador.fit_transform(df_imoveis[['Area_m2', 'Preco_Venda_R$', 'Score_Prospeccao']])

# ---- 3. TREINAMENTO DO MODELO DE MACHINE LEARNING ----
k = 3
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df_imoveis['Cluster_ID'] = kmeans.fit_predict(dados_padronizados)

# ---- 4. ROTULAÇÃO E STORYTELLING DE MERCADO IMOBILIÁRIO ----
def rotular_cluster(row):
    if row['Cluster_ID'] == 0:
        return 'Oportunidades Economicas'
    elif row['Cluster_ID'] == 1:
        return 'Potencial Alto Padrao'
    else:
        return 'Eficiencia / Investimento Rapido'

df_imoveis['Segmento_Imovel'] = df_imoveis.apply(rotular_cluster, axis=1)

# ---- 5. SALVAMENTO ADAPTADO PARA SISTEMAS PT-BR (MUITO IMPORTANTE) ----
pasta_destino = os.path.join('..', 'dados', 'processed')

# Garante o funcionamento caso seja executado a partir da raiz do projeto
if not os.path.exists(os.path.join('..', 'dados')) and os.path.exists('dados'):
    pasta_destino = os.path.join('dados', 'processed')

os.makedirs(pasta_destino, exist_ok=True)

# SOLUÇÃO DA CHARADA: sep=';' e decimal=',' força o arquivo a nascer no padrão que o seu Power BI lê nativamente
df_imoveis.to_csv(
    os.path.join(pasta_destino, 'dImoveis_Segmentados.csv'), 
    index=False, 
    sep=';', 
    decimal=',', 
    encoding='utf-8-sig'
)

print(f"Pipeline de Machine Learning concluído com sucesso!")
print(f"Dataset calibrado e salvo para Power BI PT-BR em: {os.path.join(pasta_destino, 'dImoveis_Segmentados.csv')}")
