# ==============================================================================
# WORKFLOW DE VISAO COMPUTACIONAL (OPENCV) - PROVA DE CONCEITO (19304 A1)
# ==============================================================================
# REGRAS DE DADOS DA EQUIPE:
# 1. Leitura estrita da pasta Demo: Project_Demo\dataset_limpo\19304\video\A1\
#
# Experimental table:
## Test Type, First round of tests with nitrogen-diluted fuel and oxygen,
# Test Day*,19304,
# Year, 2019,
# Month, Oct.,
# Date, 31,
# Atmosphere*,~21% O2 with N4
# Fuel Bottle,45% CH4 with N2, (metano)
# Flames Ignited*,9,(A1, A2, A3, A7, B1, B2, B3, B4, K1)
# Notes,*Flames Ignited is the number ignited on that day (neglecting the day change on ISS).

# 1. Câmera ACME (A câmera Colorida Padrão)
# '19304A1_ACME.zip' (262 MB) - 176 imagens .hobj (Formato Raw Proprietário).
    # Arquivos .hobj intratáveis acima para imagens .tif perfeitas.
# '19304A1_ACME_Converted.zip' (908 MB) - 176 imagens .tif (Alta Qualidade) e 1 arquivo .txt com os timestamps.


# 2. Câmeras Especiais (UV e Espectral)
# '19304A1A_HiBMS.zip' (707 MB) - 632 imagens .tif e 1 .txt (Timestamps).
    # Essa é a High Bandwidth Multi-Spectral. 
    # Ela captura detalhes absurdos da chama em larguras de banda específicas.
# '19304A1B_LLL-UV.zip' (47 MB) - 308 imagens .tif e 1 .txt.
    # Low Light Ultra-Violet. 
    # Ela vê o brilho UV invisível da chama (MUITO útil para checar radiometria).

# 3. Câmera Intensificada (INTNS)
# '19304A1_INTNS.zip' (225 MB) - 251 imagens .tiff.
    # Câmera altamente sensível à luz, 
    # #usada para chamas "frias" que o olho humano quase não vê.
# '19304A1_INTNS_ALL.zip' (506 MB) - 607 imagens .tiff.
    # A mesma câmera acima, 
    # mas contendo a gravação do período completo (inclusive longo tempo de fundo escuro antes/depois da ignição).

# 4. O Vídeo do Streaming (VLC Record)
# 'vlc-record-2019-10-31-15h32m20s-udp_19304A1.zip' (90 MB) - 1 arquivo de vídeo .ts (MPEG Transport Stream).
       # É essencialmente o vídeo cru (sem compressão MP4) da gravação da tela que os engenheiros da NASA assistiram ao vivo.

# Discussões:
# Para uma análise mais profunda, poderiamos tentar uma analise multiespectral 
# ('19304A1B_LLL-UV.zip' , '19304A1_ACME_Converted.zip', '19304A1_INTNS_ALL.zip').
# Diferentes framerates (A câmera ACME tirou 176 fotos.
# A câmera INTNS tirou 251 fotos.
# A câmera LLL-UV tirou 308 fotos.
# A câmera HiBMS tirou 632 fotos.
# Poderiamos resolver com interpolação mas o principal problema está nas diferentes posições das câmeras.
# Matrizes de Homografia para centralizar o evento pode dar certo.
# Podemos filtrar os dados depois de parametrizarmos com OpenCV.
# O script roda no LLL-UV e gera uma coluna no CSV: Raio_Reacao_Quimica (mm).
# O script roda no ACME e gera uma coluna no CSV: Raio_Fuligem_Amarela (mm).
# O script roda no INTNS e gera uma coluna no CSV: Raio_Calor_Frio (mm).


import pandas as pd

def telemetria(data):
    """
    Lê o CSV bruto original da NASA (sensores físicos) e extrai 
    apenas as features termodinâmicas que vão compor o Vetor de Entrada da IA.
    """
    print(f"\n[1] Lendo Telemetria Bruta da NASA: {data}")
    # skiprows=1 porque a primeira linha do log da NASA tem metadados em texto
    df_bruto = pd.read_csv(data, skiprows=1)
    
    # Filtramos estritamente o que importa para a IA aprender a física do fogo
    # Time: Usaremos depois para sincronizar com o vídeo
    # MFCA3FuelFlow: Fluxo de massa de Metano medido
    # IonCurrent: Detecção química instantânea da chama
    # RadiometerCenter: Irradiação de calor nas paredes
    colunas_importantes = ['Time', 'MFCA3FuelFlow', 'IonCurrent', 'RadiometerCenter', 'TCBurner']
    
    df_vetor = df_bruto[colunas_importantes].copy()
    
    # Tratamento: se a NASA tiver tido queda de sinal e a linha vier vazia, removemos
    df_vetor = df_vetor.dropna()
    
    print(f"-> Telemetria processada: {len(df_vetor)} medições extraídas.")
    return df_vetor

# ==================================================
# ÁREA DE TESTES
# ==================================================
if __name__ == "__main__":
    # Apontamos diretamente para a raiz do dataset da NASA
    raw = r"D:\NASA\dataset\19304\A1\19304A1_data.csv"
    
    vetor_fisico = telemetria(raw)
    
    print("\n=== VETOR DE ENTRADA (FÍSICA PURA) ===")
    print(vetor_fisico.head(10))
    
    print("\n=== ESTATÍSTICAS DOS DADOS ===")
    print(vetor_fisico[['MFCA3FuelFlow', 'IonCurrent']].describe())
