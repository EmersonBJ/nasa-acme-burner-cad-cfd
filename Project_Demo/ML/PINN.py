#A Mágica do PINN (Physics-Informed Neural Network)
#Eu criei uma Rede Neural PyTorch com 4 camadas Tanh. Por que Tanh? Porque a função tangente hiperbólica é derivável suavemente em qualquer ponto. E nós vamos precisar das derivadas!

#O pulo do gato está na Função de Perda (Loss Function). O XGBoost só tentava minimizar o erro entre a previsão e a câmera. O nosso PINN vai calcular dois erros:

#Erro de Dados: O quanto a previsão se afasta do que o seu OpenCV mediu.
#Erro de Termodinâmica (A grande novidade): O PyTorch vai usar o sistema de Autograd (Derivação Automática) para calcular a derivada temporal $\frac{dA}{dt}$ da área da chama gerada pela rede.
#Eu criei dois "pesos" físicos: Alpha (Taxa de Expansão pela Injeção de Gás) e Beta (Taxa de Dissipação/Resfriamento).
#A rede é obrigada a prever uma chama que obedeça à equação: Crescimento = (Gás Entrando * Alpha) - (Área Atual * Beta). Se ela prever uma chama que quebra essa lei de conservação, ela recebe uma penalidade massiva no erro!
#O modelo vai aprender a simular o fogo da NASA por trás dos panos. E no final, ele vai gerar um gráfico PINN_Simulacao_A1.png comparando a linha denteada (do OpenCV real) com a curva contínua perfeitamente termodinâmica que ele simulou para o teste A1.

import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os

print("="*60)
print(" INICIANDO TREINAMENTO FÍSICO COM PINN (NASA MICROGRAVITY) ")
print("="*60)

# =======================================================
# 1. ARQUITETURA DA PINN (Physics-Informed Neural Network)
# =======================================================
class CombustaoPINN(nn.Module):
    def __init__(self):
        super().__init__()
        # A rede recebe 2 inputs: Tempo e Vazão (FuelFlow)
        # Tanh é essencial porque precisamos que a função seja diferenciável suavemente (Autograd)
        self.net = nn.Sequential(
            nn.Linear(2, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Tanh(),
            nn.Linear(64, 1) # Retorna 1 output: Área prevista
        )
        
        # O SEGREDO DA PINN: Parâmetros Físicos Aprendíveis
        # A rede vai "descobrir" a termodinâmica por trás da chama
        self.alpha = nn.Parameter(torch.tensor([1.0], requires_grad=True)) # Expansão Térmica
        self.beta = nn.Parameter(torch.tensor([0.1], requires_grad=True))  # Dissipação Térmica

    def forward(self, t, flow):
        inputs = torch.cat([t, flow], dim=1)
        return self.net(inputs)

# =======================================================
# 2. CARREGAMENTO DOS DADOS PUROS
# =======================================================
try:
    df = pd.read_csv(r"D:\NASA\Project_Demo\Dataset_Multimodal_Final.csv")
except FileNotFoundError:
    print("[!] Arquivo Dataset_Multimodal_Final.csv não encontrado. Rode o pipeline antes!")
    exit()

# Filtrar para não ter valores nulos
df = df.dropna(subset=['Time', 'MFCA3FuelFlow', 'Area_UV'])

def time_to_seconds(t_str):
    try:
        parts = str(t_str).split(':')
        if len(parts) == 4:
            h, m, s, ms = parts
            return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000.0
    except:
        pass
    return 0.0

df['Time'] = df['Time'].apply(time_to_seconds)

# Para facilitar a equação diferencial, vamos normalizar os eixos
scaler_t = StandardScaler()
scaler_flow = StandardScaler()
scaler_area = StandardScaler()

t_scaled = scaler_t.fit_transform(df[['Time']].values)
flow_scaled = scaler_flow.fit_transform(df[['MFCA3FuelFlow']].values)
area_scaled = scaler_area.fit_transform(df[['Area_UV']].values)

# Transformando em Tensores do PyTorch
# IMPORTANTE: O Tempo (t) precisa de requires_grad=True para calcular a Derivada Parcial dA/dt
t_tensor = torch.tensor(t_scaled, dtype=torch.float32, requires_grad=True)
flow_tensor = torch.tensor(flow_scaled, dtype=torch.float32)
area_tensor = torch.tensor(area_scaled, dtype=torch.float32)

# =======================================================
# 3. MOTOR DE OTIMIZAÇÃO FÍSICA
# =======================================================
modelo = CombustaoPINN()
optimizer = torch.optim.Adam(modelo.parameters(), lr=0.001)

epochs = 3000
print("-> Dados Normalizados e Injetados.")
print("-> Iniciando cálculo das Derivadas Parciais de Navier-Stokes (Simuladas)...\n")

for epoch in range(epochs):
    optimizer.zero_grad()
    
    # 3.1 A rede chuta o tamanho da Área
    area_pred = modelo(t_tensor, flow_tensor)
    
    # 3.2 LOSS DOS DADOS: O quanto ela errou do sensor OpenCV? (O que o XGBoost faz)
    loss_data = torch.mean((area_pred - area_tensor) ** 2)
    
    # 3.3 LOSS DA FÍSICA: Usando Autograd para calcular a Equação Diferencial Ordinary (ODE)
    # Lei modelada: A taxa de variação da Área (dA/dt) = (Alpha * Gás Injetado) - (Beta * Dissipação Térmica Atual)
    dA_dt = torch.autograd.grad(
        area_pred, t_tensor, 
        grad_outputs=torch.ones_like(area_pred),
        create_graph=True
    )[0]
    
    # Resíduo da Física = O que a equação teórica diz VS O que a rede fez
    physics_residual = dA_dt - (modelo.alpha * flow_tensor - modelo.beta * area_pred)
    loss_physics = torch.mean(physics_residual ** 2)
    
    # LOSS TOTAL = Fidelidade aos Sensores + Fidelidade às Leis da Física
    loss_total = loss_data + (0.5 * loss_physics)
    
    loss_total.backward()
    optimizer.step()
    
    if epoch % 500 == 0:
        print(f"Epoch {epoch:4d} | Loss: {loss_total.item():.4f} "
              f"| Alpha (Expansão): {modelo.alpha.item():.3f} | Beta (Dissipação): {modelo.beta.item():.3f}")

print("\n" + "="*60)
print(" TREINAMENTO PINN CONCLUÍDO! ")
print("="*60)
print(f" -> Taxa Termodinâmica de Expansão (Alpha) descoberta: {modelo.alpha.item():.4f}")
print(f" -> Taxa de Dissipação (Beta) descoberta: {modelo.beta.item():.4f}")

# =======================================================
# 4. EXPORTAR GRÁFICO DO TESTE "A1" PARA COMPROVAÇÃO VISUAL
# =======================================================
print("\n-> Gerando Gráfico Comparativo para o Teste A1...")
df_a1 = df[df['ID_Teste'] == 'A1']
if not df_a1.empty:
    t_a1_raw = df_a1[['Time']].values
    flow_a1_raw = df_a1[['MFCA3FuelFlow']].values
    area_a1_real = df_a1[['Area_UV']].values
    
    t_a1_scaled = torch.tensor(scaler_t.transform(t_a1_raw), dtype=torch.float32)
    flow_a1_scaled = torch.tensor(scaler_flow.transform(flow_a1_raw), dtype=torch.float32)
    
    modelo.eval() # Congela a rede
    with torch.no_grad():
        area_pred_scaled = modelo(t_a1_scaled, flow_a1_scaled).numpy()
        
    area_pred_real = scaler_area.inverse_transform(area_pred_scaled)
    
    plt.figure(figsize=(10, 5))
    plt.plot(t_a1_raw, area_a1_real, 'bo-', label='Realidade Medida (OpenCV)', markersize=4)
    plt.plot(t_a1_raw, area_pred_real, 'r*-', label='Simulação PINN (Leis da Física)', markersize=4)
    plt.title('Validação Termodinâmica da Chama - PINN vs Realidade (Teste A1)')
    plt.xlabel('Tempo da NASA (s)')
    plt.ylabel('Área da Chama (Pixels²)')
    plt.legend()
    plt.grid()
    
    caminho_grafico = r"D:\NASA\Project_Demo\PINN_Simulacao_A1.png"
    plt.savefig(caminho_grafico)
    print(f"[OK] Gráfico salvo com sucesso em: {caminho_grafico}")
else:
    print("[!] Teste A1 não encontrado no dataset para gerar gráfico.")
