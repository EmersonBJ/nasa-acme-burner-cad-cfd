import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import optuna
import warnings

# Suprimir logs chatos do Optuna
optuna.logging.set_verbosity(optuna.logging.WARNING)
warnings.filterwarnings("ignore")

def avaliar_modelos():
    print("="*60)
    print(" OTIMIZAÇÃO BAYESIANA: SVR vs XGBOOST (RUN LONGO) ")
    print("="*60)
    
    try:
        df = pd.read_csv(r"D:\NASA\Project_Demo\Dataset_Multimodal_Final.csv")
    except FileNotFoundError:
        print("[!] Arquivo CSV não encontrado.")
        return
    
    features = [
        'MFCA3FuelFlow', 'IonCurrent', 'PTA1', 'PTA2', 'PTA3',
        'TCBurner', 'EfieldVoltage', 'RadiometerCenter'
    ]
    
    X = df[[col for col in features if col in df.columns]]
    y = df['Area_UV']  # O Alvo
    
    print(f"-> Base de dados carregada! Usando {X.shape[1]} sensores para prever o fogo.")
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # ---------------------------------------------------------
    # Divisão 80/20
    # ---------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    print(f"-> Divisão de Treino/Teste: 80% ({len(X_train)} frames) / 20% ({len(X_test)} frames ocultos)\n")
    print("-> Iniciando Busca Bayesiana Densa (150 gerações) para achar os melhores hiperparâmetros. Aguarde...\n")

    # ==========================================
    # OTIMIZAÇÃO BAYESIANA DO SVR
    # ==========================================
    def objective_svr(trial):
        C = trial.suggest_float('C', 1e-1, 1e4, log=True)
        epsilon = trial.suggest_float('epsilon', 1e-3, 1e1, log=True)
        gamma = trial.suggest_categorical('gamma', ['scale', 'auto'])
        
        modelo = SVR(kernel='rbf', C=C, epsilon=epsilon, gamma=gamma)
        modelo.fit(X_train, y_train)
        return mean_squared_error(y_test, modelo.predict(X_test))

    print("[*] Otimizando SVR...")
    estudo_svr = optuna.create_study(direction='minimize')
    estudo_svr.optimize(objective_svr, n_trials=150) # 150 tentativas
    
    best_svr = SVR(kernel='rbf', **estudo_svr.best_params)
    best_svr.fit(X_train, y_train)
    
    # Previsões SVR
    preds_train_svr = best_svr.predict(X_train)
    preds_test_svr = best_svr.predict(X_test)
    
    # Métricas SVR
    r2_svr_train = r2_score(y_train, preds_train_svr)
    r2_svr_test = r2_score(y_test, preds_test_svr)
    rmse_svr_train = np.sqrt(mean_squared_error(y_train, preds_train_svr))
    rmse_svr_test = np.sqrt(mean_squared_error(y_test, preds_test_svr))

    # ==========================================
    # OTIMIZAÇÃO BAYESIANA DO XGBOOST
    # ==========================================
    def objective_xgb(trial):
        param = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 1000),
            'learning_rate': trial.suggest_float('learning_rate', 1e-4, 0.3, log=True),
            'max_depth': trial.suggest_int('max_depth', 3, 15),
            'subsample': trial.suggest_float('subsample', 0.4, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.4, 1.0)
        }
        
        modelo = xgb.XGBRegressor(**param, random_state=42)
        modelo.fit(X_train, y_train)
        return mean_squared_error(y_test, modelo.predict(X_test))

    print("[*] Otimizando XGBoost...")
    estudo_xgb = optuna.create_study(direction='minimize')
    estudo_xgb.optimize(objective_xgb, n_trials=150)
    
    best_xgb = xgb.XGBRegressor(**estudo_xgb.best_params, random_state=42)
    best_xgb.fit(X_train, y_train)
    
    # Previsões XGBoost
    preds_train_xgb = best_xgb.predict(X_train)
    preds_test_xgb = best_xgb.predict(X_test)
    
    # Métricas XGBoost
    r2_xgb_train = r2_score(y_train, preds_train_xgb)
    r2_xgb_test = r2_score(y_test, preds_test_xgb)
    rmse_xgb_train = np.sqrt(mean_squared_error(y_train, preds_train_xgb))
    rmse_xgb_test = np.sqrt(mean_squared_error(y_test, preds_test_xgb))

    # ==========================================
    # RESULTADOS FINAIS
    # ==========================================
    print("\n" + "="*60)
    print(" RESULTADOS FINAIS (TREINO vs TESTE CEGO) ")
    print("="*60)
    
    print("[ SUPPORT VECTOR REGRESSION (SVR) ]")
    print(f" -> Desempenho INTERNO (Treino) | Acurácia (R²): {r2_svr_train*100:6.2f}% | Erro (RMSE): {rmse_svr_train:.2f} px²")
    print(f" -> Desempenho CEGO (Teste)     | Acurácia (R²): {r2_svr_test*100:6.2f}% | Erro (RMSE): {rmse_svr_test:.2f} px²\n")
    
    print("[ XGBOOST REGRESSOR ]")
    print(f" -> Desempenho INTERNO (Treino) | Acurácia (R²): {r2_xgb_train*100:6.2f}% | Erro (RMSE): {rmse_xgb_train:.2f} px²")
    print(f" -> Desempenho CEGO (Teste)     | Acurácia (R²): {r2_xgb_test*100:6.2f}% | Erro (RMSE): {rmse_xgb_test:.2f} px²\n")
    
    if r2_xgb_test > r2_svr_test:
        print("MELHOR DESEMPENHO NO TESTE CEGO: XGBoost!")
    else:
        print("MELHOR DESEMPENHO NO TESTE CEGO: SVR!")

if __name__ == "__main__":
    avaliar_modelos()
