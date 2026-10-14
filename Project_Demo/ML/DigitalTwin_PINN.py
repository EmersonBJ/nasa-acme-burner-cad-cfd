import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import optuna
import warnings
import matplotlib.pyplot as plt
import os

optuna.logging.set_verbosity(optuna.logging.WARNING)
warnings.filterwarnings("ignore")

print("="*60)
print(" OTIMIZAÇÃO BAYESIANA DO GÊMEO DIGITAL (PINN) ")
print("="*60)

# ==========================================
# 1. ARQUITETURA DO GÊMEO DIGITAL DINÂMICA
# ==========================================
class DigitalTwinPINN(nn.Module):
    def __init__(self, n_layers, n_neurons):
        super().__init__()
        layers = []
        layers.append(nn.Linear(2, n_neurons))
        layers.append(nn.Tanh())
        
        for _ in range(n_layers - 1):
            layers.append(nn.Linear(n_neurons, n_neurons))
            layers.append(nn.Tanh())
            
        layers.append(nn.Linear(n_neurons, 4)) # Output: [Área, Temp, Radiação, Íons]
        self.net = nn.Sequential(*layers)
        
        # Parâmetros Físicos Acoplados
        self.alpha_area = nn.Parameter(torch.tensor([1.0], requires_grad=True)) 
        self.beta_temp = nn.Parameter(torch.tensor([0.5], requires_grad=True))

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

def executar_gemeo_digital_bayesiana():
    df = pd.read_csv(r"D:\NASA\Project_Demo\Dataset_Multimodal_Final.csv")
    df = df.dropna(subset=['Time', 'MFCA3FuelFlow', 'Area_UV', 'TCBurner', 'RadiometerCenter', 'IonCurrent'])
    df['Time'] = df['Time'].apply(time_to_seconds)

    scaler_t = StandardScaler()
    scaler_flow = StandardScaler()
    scaler_area = StandardScaler()
    scaler_temp = StandardScaler()
    scaler_rad = StandardScaler()
    scaler_ion = StandardScaler()

    t_scaled = scaler_t.fit_transform(df[['Time']].values)
    flow_scaled = scaler_flow.fit_transform(df[['MFCA3FuelFlow']].values)
    area_scaled = scaler_area.fit_transform(df[['Area_UV']].values)
    temp_scaled = scaler_temp.fit_transform(df[['TCBurner']].values)
    rad_scaled = scaler_rad.fit_transform(df[['RadiometerCenter']].values)
    ion_scaled = scaler_ion.fit_transform(df[['IonCurrent']].values)

    X_scaled = np.hstack([t_scaled, flow_scaled])
    y_scaled = np.hstack([area_scaled, temp_scaled, rad_scaled, ion_scaled])

    # 80/20 Teste Cego
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)
    
    t_train = torch.tensor(X_train[:, 0:1], dtype=torch.float32, requires_grad=True)
    flow_train = torch.tensor(X_train[:, 1:2], dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    
    t_test = torch.tensor(X_test[:, 0:1], dtype=torch.float32)
    flow_test = torch.tensor(X_test[:, 1:2], dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    print("-> Iniciando Busca Evolutiva (20 gerações rápidas)...")
    
    def objective(trial):
        n_layers = trial.suggest_int('n_layers', 2, 6)
        n_neurons = trial.suggest_int('n_neurons', 32, 256)
        lr = trial.suggest_float('lr', 1e-4, 1e-2, log=True)
        phys_weight = trial.suggest_float('phys_weight', 0.1, 2.0)
        
        modelo = DigitalTwinPINN(n_layers, n_neurons)
        optimizer = torch.optim.Adam(modelo.parameters(), lr=lr)
        
        for epoch in range(300): # 300 épocas pra Optuna ter uma ideia
            optimizer.zero_grad()
            preds = modelo(t_train, flow_train)
            
            loss_data = torch.mean((preds - y_train_tensor) ** 2)
            
            area_pred = preds[:, 0:1]
            temp_pred = preds[:, 1:2]
            
            dA_dt = torch.autograd.grad(area_pred, t_train, grad_outputs=torch.ones_like(area_pred), create_graph=True)[0]
            res_area = dA_dt - (modelo.alpha_area * flow_train)
            
            dT_dt = torch.autograd.grad(temp_pred, t_train, grad_outputs=torch.ones_like(temp_pred), create_graph=True)[0]
            res_temp = dT_dt - (modelo.beta_temp * dA_dt)
            
            loss_physics = torch.mean(res_area**2) + torch.mean(res_temp**2)
            
            loss_total = loss_data + (phys_weight * loss_physics)
            loss_total.backward()
            optimizer.step()
            
        modelo.eval()
        with torch.no_grad():
            test_preds = modelo(t_test, flow_test)
            val_loss = torch.mean((test_preds - y_test_tensor) ** 2).item()
            
        return val_loss

    estudo = optuna.create_study(direction='minimize')
    estudo.optimize(objective, n_trials=20)
    
    best = estudo.best_params
    print("\n" + "="*60)
    print(" MELHOR ARQUITETURA DO GÊMEO DIGITAL ")
    print("="*60)
    print(f" -> Camadas Ocultas: {best['n_layers']}")
    print(f" -> Neurônios por Camada: {best['n_neurons']}")
    print(f" -> Peso da Lei da Física: {best['phys_weight']:.2f}x")
    
    print("\n-> Treinando o Simulador Campeão até o Fim (2000 épocas)...")
    modelo_campeao = DigitalTwinPINN(best['n_layers'], best['n_neurons'])
    optimizer = torch.optim.Adam(modelo_campeao.parameters(), lr=best['lr'])
    
    for epoch in range(2000):
        optimizer.zero_grad()
        preds = modelo_campeao(t_train, flow_train)
        loss_data = torch.mean((preds - y_train_tensor) ** 2)
        
        area_pred = preds[:, 0:1]
        temp_pred = preds[:, 1:2]
        
        dA_dt = torch.autograd.grad(area_pred, t_train, grad_outputs=torch.ones_like(area_pred), create_graph=True)[0]
        res_area = dA_dt - (modelo_campeao.alpha_area * flow_train)
        
        dT_dt = torch.autograd.grad(temp_pred, t_train, grad_outputs=torch.ones_like(temp_pred), create_graph=True)[0]
        res_temp = dT_dt - (modelo_campeao.beta_temp * dA_dt)
        
        loss_physics = torch.mean(res_area**2) + torch.mean(res_temp**2)
        
        loss_total = loss_data + (best['phys_weight'] * loss_physics)
        loss_total.backward()
        optimizer.step()
        
    print("\n[ FÍSICA DESCOBERTA NO GÊMEO DIGITAL ]")
    print(f" -> Alpha (Expansão por Vazão): {modelo_campeao.alpha_area.item():.4f}")
    print(f" -> Beta (Aquecimento por Expansão): {modelo_campeao.beta_temp.item():.4f}")

    print("\n-> Simulando o cenário completo. Exportando Dashboard Otimizado...")
    t_full = torch.tensor(t_scaled, dtype=torch.float32)
    flow_full = torch.tensor(flow_scaled, dtype=torch.float32)
    
    modelo_campeao.eval()
    with torch.no_grad():
        preds_finais = modelo_campeao(t_full, flow_full).numpy()
    
    area_final = scaler_area.inverse_transform(preds_finais[:, 0:1])
    temp_final = scaler_temp.inverse_transform(preds_finais[:, 1:2])
    
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(df['Time'].values, scaler_area.inverse_transform(area_scaled), 'b-', alpha=0.3, label='Sensor Real (Área)')
    plt.plot(df['Time'].values, area_final, 'r--', label='Gêmeo Digital (Área)')
    plt.ylabel("Área da Chama")
    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.plot(df['Time'].values, scaler_temp.inverse_transform(temp_scaled), 'g-', alpha=0.3, label='Sensor Real (Temperatura)')
    plt.plot(df['Time'].values, temp_final, 'orange', linestyle='--', label='Gêmeo Digital (Temperatura)')
    plt.ylabel("Temperatura")
    plt.xlabel("Tempo (s)")
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(r"D:\NASA\Project_Demo\Gemeo_Digital_Dashboard_Bayesiano.png")
    print(r"[OK] Dashboard salvo em: D:\NASA\Project_Demo\Gemeo_Digital_Dashboard_Bayesiano.png")

if __name__ == "__main__":
    executar_gemeo_digital_bayesiana()
