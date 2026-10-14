import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import optuna
import warnings
import os

optuna.logging.set_verbosity(optuna.logging.WARNING)
warnings.filterwarnings("ignore")

# ==========================================
# 1. PINN DINÂMICA (Molda-se à Bayesiana)
# ==========================================
class DynamicPINN(nn.Module):
    def __init__(self, n_layers, n_neurons):
        super().__init__()
        layers = []
        layers.append(nn.Linear(2, n_neurons))
        layers.append(nn.Tanh())
        
        for _ in range(n_layers - 1):
            layers.append(nn.Linear(n_neurons, n_neurons))
            layers.append(nn.Tanh())
            
        layers.append(nn.Linear(n_neurons, 1))
        self.net = nn.Sequential(*layers)
        
        self.alpha = nn.Parameter(torch.tensor([1.0], requires_grad=True))
        self.beta = nn.Parameter(torch.tensor([0.1], requires_grad=True))

    def forward(self, t, flow):
        inputs = torch.cat([t, flow], dim=1)
        return self.net(inputs)

def time_to_seconds(t_str):
    try:
        parts = str(t_str).split(':')
        if len(parts) == 4:
            h, m, s, ms = parts
            return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000.0
    except:
        pass
    return 0.0

def executar_pinn_bayesiana():
    print("="*60)
    print(" OTIMIZAÇÃO BAYESIANA DA FÍSICA (PINN + OPTUNA) ")
    print("="*60)
    
    # ------------------------------------------
    # PREPARAÇÃO 80/20 (Igual ao XGBoost!)
    # ------------------------------------------
    df = pd.read_csv(r"D:\NASA\Project_Demo\Dataset_Multimodal_Final.csv")
    df = df.dropna(subset=['Time', 'MFCA3FuelFlow', 'Area_UV'])
    df['Time'] = df['Time'].apply(time_to_seconds)

    scaler_t = StandardScaler()
    scaler_flow = StandardScaler()
    scaler_area = StandardScaler()

    t_scaled = scaler_t.fit_transform(df[['Time']].values)
    flow_scaled = scaler_flow.fit_transform(df[['MFCA3FuelFlow']].values)
    area_scaled = scaler_area.fit_transform(df[['Area_UV']].values)
    
    X_scaled = np.hstack([t_scaled, flow_scaled])
    y_scaled = area_scaled

    # O TESTE CEGO DE 20%
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)
    
    t_train = torch.tensor(X_train[:, 0:1], dtype=torch.float32, requires_grad=True)
    flow_train = torch.tensor(X_train[:, 1:2], dtype=torch.float32)
    area_train = torch.tensor(y_train, dtype=torch.float32)
    
    t_test = torch.tensor(X_test[:, 0:1], dtype=torch.float32)
    flow_test = torch.tensor(X_test[:, 1:2], dtype=torch.float32)
    area_test = torch.tensor(y_test, dtype=torch.float32)

    print("-> Iniciando a Busca Evolutiva (20 gerações rápidas para prova de conceito)...")
    
    # ==========================================
    # FUNÇÃO OBJETIVO (O que o Optuna tenta melhorar)
    # ==========================================
    def objective(trial):
        n_layers = trial.suggest_int('n_layers', 2, 6)       # Quantas camadas de neurônios?
        n_neurons = trial.suggest_int('n_neurons', 16, 128)  # Qual a largura do cérebro?
        lr = trial.suggest_float('lr', 1e-4, 1e-2, log=True) # Velocidade de aprendizado
        phys_weight = trial.suggest_float('phys_weight', 0.1, 2.0) # O quanto a Física importa?
        
        modelo = DynamicPINN(n_layers, n_neurons)
        optimizer = torch.optim.Adam(modelo.parameters(), lr=lr)
        
        # Treino relâmpago de 300 épocas por geração
        for epoch in range(300):
            optimizer.zero_grad()
            area_pred = modelo(t_train, flow_train)
            loss_data = torch.mean((area_pred - area_train) ** 2)
            
            # Autograd - A derivada analítica exata da rede!
            dA_dt = torch.autograd.grad(area_pred, t_train, grad_outputs=torch.ones_like(area_pred), create_graph=True)[0]
            physics_residual = dA_dt - (modelo.alpha * flow_train - modelo.beta * area_pred)
            loss_physics = torch.mean(physics_residual ** 2)
            
            loss_total = loss_data + (phys_weight * loss_physics)
            loss_total.backward()
            optimizer.step()
            
        # Avalia a geração nos 20% cegos
        modelo.eval()
        with torch.no_grad():
            test_pred = modelo(t_test, flow_test)
            val_loss = mean_squared_error(area_test.numpy(), test_pred.numpy())
            
        return val_loss

    # Roda a Bayesiana!
    estudo = optuna.create_study(direction='minimize')
    estudo.optimize(objective, n_trials=20)
    
    best = estudo.best_params
    print("\n" + "="*60)
    print(" MELHOR ARQUITETURA PINN DESCOBERTA ")
    print("="*60)
    print(f" -> Camadas Ocultas: {best['n_layers']}")
    print(f" -> Neurônios por Camada: {best['n_neurons']}")
    print(f" -> Peso da Lei da Física: {best['phys_weight']:.2f}x")
    
    print("\n-> Treinando a Arquitetura Campeã até o Fim (2000 épocas)...")
    modelo_campeao = DynamicPINN(best['n_layers'], best['n_neurons'])
    optimizer = torch.optim.Adam(modelo_campeao.parameters(), lr=best['lr'])
    
    for epoch in range(2000):
        optimizer.zero_grad()
        area_pred = modelo_campeao(t_train, flow_train)
        loss_data = torch.mean((area_pred - area_train) ** 2)
        
        dA_dt = torch.autograd.grad(area_pred, t_train, grad_outputs=torch.ones_like(area_pred), create_graph=True)[0]
        physics_residual = dA_dt - (modelo_campeao.alpha * flow_train - modelo_campeao.beta * area_pred)
        loss_physics = torch.mean(physics_residual ** 2)
        
        loss_total = loss_data + (best['phys_weight'] * loss_physics)
        loss_total.backward()
        optimizer.step()
        
    # TESTE CEGO E MÉTRICAS FINAIS
    modelo_campeao.eval()
    with torch.no_grad():
        # Treino
        pred_train_scaled = modelo_campeao(t_train, flow_train).numpy()
        pred_train_real = scaler_area.inverse_transform(pred_train_scaled)
        area_train_real = scaler_area.inverse_transform(area_train.numpy())
        
        # Teste (Os 20%)
        pred_test_scaled = modelo_campeao(t_test, flow_test).numpy()
        pred_test_real = scaler_area.inverse_transform(pred_test_scaled)
        area_test_real = scaler_area.inverse_transform(area_test.numpy())
        
    r2_train = r2_score(area_train_real, pred_train_real)
    rmse_train = np.sqrt(mean_squared_error(area_train_real, pred_train_real))
    
    r2_test = r2_score(area_test_real, pred_test_real)
    rmse_test = np.sqrt(mean_squared_error(area_test_real, pred_test_real))

    print("\n" + "="*60)
    print(" RESULTADOS FINAIS DA PINN OTIMIZADA ")
    print("="*60)
    print(f" -> Desempenho INTERNO (Treino) | Acurácia (R²): {r2_train*100:6.2f}% | Erro (RMSE): {rmse_train:.2f} px²")
    print(f" -> Desempenho CEGO (Teste)     | Acurácia (R²): {r2_test*100:6.2f}% | Erro (RMSE): {rmse_test:.2f} px²")
    print("\n[ FÍSICA DESCOBERTA ]")
    print(f" -> Alpha (Expansão): {modelo_campeao.alpha.item():.4f}")
    print(f" -> Beta (Dissipação): {modelo_campeao.beta.item():.4f}")

if __name__ == "__main__":
    executar_pinn_bayesiana()
