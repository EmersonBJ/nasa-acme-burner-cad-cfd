import pandas as pd
from pathlib import Path

# Importando nossos motores
from Treinamento_SVR.svr_workflow_19304A1 import telemetria
from Treinamento_Visao.opencv_workflow_19304A1 import geometria

def processar_dados():
    print("="*60)
    print(" PIPELINE MULTIMODAL (FÍSICA + 3 CÂMERAS) - XGBOOST ")
    print("="*60)
    
    testes_para_rodar = ['A1', 'A2', 'A3', 'A7', 'B1', 'B2', 'B3', 'B4', 'K1']
    dataset_final = []
    
    for teste in testes_para_rodar:
        print(f"\n>>>> FUSÃO: 19304 {teste} <<<<")
        
        caminho_raw = Path(rf"D:\NASA\dataset\19304\{teste}\19304{teste}_data.csv")
        if not caminho_raw.exists(): continue
            
        # 1. Puxa Física Base
        df_raw = telemetria(caminho_raw)
        df_merged = df_raw.copy()
        
        # 2. Puxa Câmera UV
        zip_uv = list(Path(r"D:\NASA\dataset\19304\video").rglob(f"*{teste}*UV.zip"))
        if zip_uv:
            df_uv = geometria(zip_uv[0], "UV", 20, df_raw, teste)
            if df_uv is not None and not df_uv.empty:
                df_merged = pd.merge(df_merged, df_uv, left_on='Time', right_on='Tempo_NASA', how='inner')
                df_merged.drop(columns=['Tempo_NASA'], inplace=True)
            
        # 3. Puxa Câmera ACME (IGNORADA PARA PRESERVAR OS DADOS DAS OUTRAS CÂMERAS)
        # zip_acme = list(Path(r"D:\NASA\dataset\19304\video").rglob(f"*{teste}*ACME*.zip"))
        # zip_acme = sorted(zip_acme, key=lambda x: "Converted" not in str(x))
        # if zip_acme:
        #     df_acme = geometria(zip_acme[0], "ACME", 40, df_raw, teste)
        #     if df_acme is not None and not df_acme.empty:
        #         df_merged = pd.merge(df_merged, df_acme, left_on='Time', right_on='Tempo_NASA', how='inner')
        #         df_merged.drop(columns=['Tempo_NASA'], inplace=True)
            
        # 4. Puxa Câmera INTNS
        zip_intns = list(Path(r"D:\NASA\dataset\19304\video").rglob(f"*{teste}*INTNS*.zip"))
        zip_intns = sorted(zip_intns, key=lambda x: "ALL" not in str(x))
        if zip_intns:
            df_intns = geometria(zip_intns[0], "INTNS", 20, df_raw, teste)
            if df_intns is not None and not df_intns.empty:
                df_merged = pd.merge(df_merged, df_intns, left_on='Time', right_on='Tempo_NASA', how='inner')
                df_merged.drop(columns=['Tempo_NASA'], inplace=True)
        
        # Limpa as linhas que não tem fogo (usando o brilho da UV como base para não perder o "chicote")
        if 'Brilho_UV' in df_merged.columns:
            df_merged = df_merged[df_merged['Brilho_UV'] > 1000].copy()
            
        df_merged['ID_Teste'] = teste 
        dataset_final.append(df_merged)
        
    if not dataset_final:
        print("Nenhum dataset fundido!")
        return None
        
    dataset_geral = pd.concat(dataset_final, ignore_index=True)
    
    # Exporta o Dataset pronto
    saida = Path(__file__).parent / 'Dataset_Multimodal_Final.csv'
    dataset_geral.to_csv(saida, index=False)
    
    print("\n" + "="*60)
    print(f" PROCESSAMENTO CONCLUIDO. {len(dataset_geral)} frames com todos os sensores fundidos.")
    print(f" Salvo em: {saida.name}")
    print("="*60)
    
    return dataset_geral

if __name__ == "__main__":
    df_xgboost = processar_dados()
