Fase 1: Mineração de Dados e Fundamentação (Semanas 1 e 2)
A base de um bom modelo de Machine Learning são os dados de entrada. Com tempo, vocês podem ir direto à fonte primária.

Extração Robusta: Acessar o sistema PSI da NASA e focar não apenas nos CSVs finais, mas nas séries temporais completas dos experimentos s-Flame (chamas esféricas) e BRE.
Estruturação de Dados (Pipeline): Criar scripts em Python usando pandas para limpar os dados brutos, alinhar os timestamps das medições de pressão com as leituras de temperatura e remover anomalias (outliers) geradas por falhas nos sensores durante os experimentos na ISS.
https://psi.nasa.gov/physci/repo/data/investigations/PSI-23

Caminho: /content/NASA.zip

Diretório de Especificações e Recursos – Projeto NASA ACME s-Flame
1. Matriz Experimental (Test Matrix)
Caminho Relativo: Metadata\PSI-23_Experimental table_ACME s-Flame.csv

Integração CFD/ML (Condições de Contorno): Fornece dados paramétricos cruciais como fração mássica da atmosfera da câmara (concentração de O2 e gás diluente) e o tipo de injeção de combustível (ex.: mistura de 45% CH4 particionado com N2).
Aplicação: Utilizado como base de definição das Boundary Conditions nas simulações do software Ansys e na parametrização dos tensores de entrada (Input Features) dos algoritmos de Inteligência Artificial.

2. Telemetria e Processamento de Dados (Data Processing Pipeline)
Caminho Relativo: Data_Processing
Arquivos Base:

ACMEFlowAndPressuresRawDataConversion.xlsx
ACMEFlowCalculator.xlsx
Integração Analítica: Estes artefatos estruturados formam o Dataset numérico principal para o treinamento de modelos de regressão avançada (e.g., Support Vector Regression - SVR ou Physics-Informed Neural Networks - PINNs).
Aplicação: Os fluxos de trabalho requerem a extração modular destes dados (em formato .csv) para ingestão na pipeline Python (nasa_parser.py).


3. Especificações Geométricas e Instrumentação (CAD/CFD References)
Caminho Relativo: CAD_References
Arquivos Base:

ACME Science Operation Requirements revA 20111018.pdf (Requisitos operacionais)
ACME s-Flame DoD.pdf (Document of Description oficial)
TC rake dimensions 20190827.pdf (Esquemático de posicionamento dos termopares)
ACME Radiometer Layouts from ProE.pdf (Posicionamento dos conjuntos radiométricos)
ACME_engineering_20210328.pdf: O manual principal de dimensões. Confirma o diâmetro da esfera porosa do queimador (6.35 mm) e o volume total da câmara (aproximadamente 83 litros). Detalha também o posicionamento exato da matriz de termopares e radiómetros (o que o Ansys usará para criar "sondas virtuais" nas mesmas coordenadas e validar as temperaturas contra a telemetria).   s1101mfa0100_C.pdf e s1101mfa1800_B.pdf: As plantas de engenharia mecânica. Apresentam as montagens oficiais em perspetiva isométrica (Chamber Insert Assembly e a placa de resfriamento), ajudando o projetista de CAD a entender a estrutura interna, os limites de escoamento e a localização das válvulas sem se perder em pormenores desnecessários.   S1101MFB0001_-ACME_Drawing_Tree.pdf: O mapa de navegação das plantas. Se faltar a medida de uma peça específica, esta árvore hierárquica indica exatamente qual o número do desenho oficial da NASA que o projetista deve procurar no repositório público.   Ficheiros _mfcSetpoints.csv: As condições de contorno iniciais. O vosso colega de CFD usará as taxas de fluxo mássico descritas aqui para definir a velocidade de entrada (Velocity-Inlet) da mistura de gás no bico do queimador durante a simulação no Ansys.   

Fase 2: Simulação CFD de Alta Fidelidade (Semanas 3 e 4)
O tempo extra permite rodar simulações que levariam horas ou dias computacionais.

Geometria 3D Fiel: No Autodesk Inventor, modelar o domínio fluido em 3D, respeitando a malha da câmara e a geometria exata do queimador.
Regime Transiente no Ansys: Em vez de uma simulação estacionária (steady-state), configurem simulações transientes. Isso permitirá capturar a ignição, a propagação inicial e a estabilização da chama ao longo do tempo.
Modelagem de Combustão Avançada: Utilizar o Species Transport com mecanismos de reação química com múltiplas etapas para o metano/ar, ativando modelos de radiação térmica (fundamental para chamas em microgravidade, onde a radiação domina a transferência de calor).
Exportação Volumétrica: Extrair nuvens de pontos 3D (X, Y, Z) contendo Temperatura e Fração de O2 a cada intervalo de tempo da simulação, tanto para 1G quanto para 0G.

[ ]

Comece a programar ou gere código com IA.
Fase 3: Treinamento dos Modelos de Inteligência Artificial (Semanas 5 e 6)
Substituir os algoritmos rápidos por arquiteturas mais robustas que aproveitem o volume massivo de dados do Ansys.

O Motor Preditivo de Segurança (SVR): Utilizar o Support Vector Regression para prever métricas críticas globais: taxa máxima de espalhamento, tempo até a chama se extinguir pela falta de oxigênio local e pressão de pico na câmara.
Redes Neurais Informadas pela Física (PINNs): Evoluir o gerador visual de um Random Forest para uma rede neural construída em PyTorch. Uma PINN é treinada não apenas nos dados, mas com as equações de conservação de massa e momento (Navier-Stokes) embutidas na sua função de perda. Isso garante que a chama gerada pela IA respeite a termodinâmica, resultando num campo 3D extremamente preciso e sem violações físicas.
Fase 4: O "Digital Twin" Interativo (Semanas 7 e 8)
A aplicação web deixa de ser um gráfico estático para se tornar um ambiente de simulação em tempo real.

Interface Streamlit + Dash: Desenvolver a interface para receber os parâmetros do usuário (nível de O2, pressão da cabine, gravidade).
Visualização 3D: Integrar o modelo visual com a biblioteca Plotly 3D ou PyVista. O usuário poderá rotacionar a câmara no navegador e ver a nuvem de temperatura gerada pela IA em tempo real.
Painel de Risco Operacional: Adicionar um módulo alimentado pelo SVR que traduz as previsões da chama em um indicador de risco de incêndio para missões prolongadas, alertando se as condições de ventilação atuais favorecem a propagação descontrolada.


Detalhamento erros e acertos até agora:
#A1
#19304A1B_LLL-UV.zip
#82-108

#19304A1_ACME_Converted.zip
#165 - 

#19304A1_INTNS_ALL.zip
#404-451

#A2
#19304A2B_LLL-UV.zip
#104-204

#19304A2_ACME_Converted (1).zip
#138-

#19304A2_INTNS_ALL (1).zip
#344-412

#A3
#19304A3B_LLL-UV.zip
#61-163

#19304A3_ACME_Converted (1).zip
#133

#19304A3_INTNS_ALL (1).zip
#331-364

#A7
#19304A7B_LLL-UV.zip
#116-192

#19304A7_ACME_Converted (1).zip
#142

#19304A7_INTNS_ALL (1).zip
#389-419

#B1
#19304B1B_LLL-UV.zip
#99-197

#19304B1_ACME_Converted.zip
#130

#19304B1_INTNS_ALL.zip
#319-386

#B2
#19304B2B_LLL-UV.zip
#75-107

#19304B2_ACME_Converted.zip
#170

#19304B2_INTNS_ALL.zip
#416-460

#B3
#19304B3B_LLL-UV.zip
#102-166

#19304B3_ACME_Converted.zip
#150

#19304B3_INTNS_ALL.zip
#390-429

#B4
#19304B4B_LLL-UV.zip
#119-125

#19304B4_ACME_Converted.zip
#132

#19304B4_INTNS_ALL.zip
#366-394

#K1
#19304K1B_LLL-UV.zip
#48-111

#19304K1_ACME_Converted.zip
#140

#19304K1_INTNS_ALL.zip
#345-376


#sso me deu um boa noção do que esperar, notei tambem que nosso tratamento atual tem uma boa perda de detalhes um exemplo é aquele efeito chicote que acontece em alguns casos antes do fim da combustão nas cameras uv
#whip-effect


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
    colunas_importantes = ['Time', 'MFCA3FuelFlow', 'IonCurrent', 'RadiometerCenter']
    
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

import cv2
import zipfile
import numpy as np
import pandas as pd

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


# PLANEJAMENTO PASSO A PASSO (A ser codificado futuramente):
# Passo 1: Inicializar o OpenCV (`cap = cv2.VideoCapture`) apontando para o .tiff

# ==============================================================================
# DICIONÁRIO MESTRE DE ANCORAGEM (Gabarito da NASA Mapeado pelo Usuário)
# ==============================================================================
ANCORAGEM = {
    # Teste: (Linha do Salto no CSV, Frame UV, Frame ACME, Frame INTNS)
    "A1": (2342, 82,  165, 404), 
    "A2": (1984, 104, 138, 344),
    "A3": (2101, 61,  133, 331), 
    "A7": (1979, 116, 142, 389),
    "B1": (1973, 99,  130, 319),
    "B2": (2478, 75,  170, 416),
    "B3": (2103, 102, 150, 390),
    "B4": (1976, 119, 132, 366),
    "K1": (2003, 48,  140, 345),
}

# Passo 2: Criar um loop 'while' para ler e processar o video frame por frame.
# Passo 3: Em cada frame, converter a imagem original (RGB/BGR) para tons de 
#          cinza (Grayscale) com `cv2.cvtColor`.
# Passo 4: Binarizacao (`cv2.threshold`): Tudo que for muito escuro vira preto 
#          puro (o espaco da camara), tudo que brilhar vira branco puro (a chama).
# Passo 5: Deteccao de borda (`cv2.findContours`): Encontrar o contorno dessa bola branca.
# Passo 6: Enquadramento (`cv2.minEnclosingCircle`): Desenhar matematicamente 
#          um circulo perfeito ao redor do contorno encontrado.
# Passo 7: Extrair o Raio (Radius) em pixels a partir da funcao matematica acima.
# Passo 8: Plotar na tela dinamicamente o circulo verde acompanhando a expansao 
#          da chama no video original. Esse e o "Showroom" para o Pitch!

# ==============================================================================
# CARREGAMENTO INTELIGENTE (Leitura em RAM sem descompactar o HD)
# ==============================================================================
# Caminhos absolutos dos nossos 3 ALVOS de Visão Computacional
BASE_PATH = r"D:\NASA\dataset\19304\video\A1"
ZIP_UV = fr"{BASE_PATH}\19304A1B_LLL-UV.zip"
ZIP_ACME = fr"{BASE_PATH}\19304A1_ACME_Converted.zip"
ZIP_INTNS = fr"{BASE_PATH}\19304A1_INTNS_ALL.zip"
caminho_csv = r"D:\NASA\dataset\19304\A1\19304A1_data.csv"
telemetria = pd.read_csv(caminho_csv, skiprows=1) # Pula a linha 1 de metadados

# Encontra a linha exata onde o Metano (MFCA3FuelFlow) começou a fluir!
# Pega o Tempo ('Time') em que o valor do metano ficou > 0.007
tempo_ignicao = telemetria[telemetria['MFCA3FuelFlow'] > 0.007]['Time'].iloc[0]
print(f"O Metano foi injetado exatamente às: {tempo_ignicao}")


def stream(caminho_zip, nome_janela="Preview", threshold = 50, tipo=None, csv_ancora=None):
    
    print(f"\n[INFO] Acessando sensor: {caminho_zip}")
    dados_extraidos = []
    df_ancora = None
    if csv_ancora is not None:
        print(f"[ANCORAGEM] Carregando coordenadas base de {csv_ancora}...")
        df_ancora = pd.read_csv(csv_ancora)
    
    indice_frame = 0 # Contador para sincronizar o arquivo

    with zipfile.ZipFile(caminho_zip, 'r') as archive:
        # Filtra apenas imagens e ordena alfabeticamente para garantir a linha do tempo cronológica
        lista_imagens = sorted([img for img in archive.namelist() if img.lower().endswith(('.tif', '.tiff'))])
        
        print(f"-> Encontrados {len(lista_imagens)} frames TIFF.")

        is_paused = True
        fundo_estatico = None # Variavel para armazenar a primeira imagem (fundo sem chama)
        raio_anterior = 0

        for img_nome in lista_imagens:
            # 1. Extrai a foto do ZIP direto para a Memoria RAM (Extremamente Rapido)
            img_bytes = archive.read(img_nome)
            
            # 2. Converte a Sopa de Bytes em um Array Numérico (Numpy)
            np_arr = np.frombuffer(img_bytes, np.uint8)
            
            # 3. Faz o OpenCV decodificar a matriz matematicamente perfeita (IMREAD_UNCHANGED)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
            
            if frame is None:
                continue
                
            # Normalizar imagens 16-bits para 8-bits para poder ver na tela do PC
            if frame.dtype == np.uint16:
                frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            
            mascara_binaria, fundo_estatico = raio(frame, fundo_estatico, threshold, tipo)
             
            # Para garantir que o círculo Verde brilhe bonito na tela (mesmo nas câmeras P&B), criamos uma tela colorida:
            frame_tela = frame.copy()
            if len(frame_tela.shape) == 2: # Se a imagem for monocromática
                frame_tela = cv2.cvtColor(frame_tela, cv2.COLOR_GRAY2BGR)

            # === SINCRONIZAÇÃO DA TELEMETRIA ABSOLUTA (SENSOR FUSION) ===
            try:
                numero_frame = int(img_nome.split('_')[-1].split('.')[0])
            except ValueError:
                numero_frame = indice_frame

            if tipo == "UV":
                # A foto 83 da UV é o Big Bang (Linha 2336)
                linha_csv = int(2336 + (numero_frame - 83) * (100.0 / 30.0))
                
            elif tipo == "ACME":
                # A foto 166 da ACME colorida é o Big Bang (Linha 2336)
                linha_csv = int(2336 + (numero_frame - 166) * (100.0 / 30.0))

            elif tipo == "INTNS":
                # A foto 402 da câmera Intensificadora é o Big Bang (Linha 2336)
                linha_csv = int(2336 + (numero_frame - 402) * (100.0 / 30.0))
            else:
                # Para a INTNS, usamos a conta provisória até você achar a faísca nela!
                fator_csv = len(telemetria) / max(1, len(lista_imagens))
                linha_csv = int(indice_frame * fator_csv)
                    
            # Extrai os dados físicos daquele milissegundo real
            if linha_csv < len(telemetria) and linha_csv >= 0:
                tempo_atual = telemetria['Time'].iloc[linha_csv]
                fluxo_metano = telemetria['MFCA3FuelFlow'].iloc[linha_csv]
                radiacao = telemetria['IonCurrent'].iloc[linha_csv]
            else:
                tempo_atual = "N/A"
                fluxo_metano = 0
                radiacao = 0

            # Escreve o HUD (Heads-Up Display) no canto esquerdo da tela (AGORA FORA DO IF DA CÂMERA P&B!)
            cv2.putText(frame_tela, f"Arquivo: {img_nome}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame_tela, f"Tempo: {tempo_atual}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)
            cv2.putText(frame_tela, f"Metano: {fluxo_metano:.4f} g/s", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)
            cv2.putText(frame_tela, f"Radiacao: {radiacao:.3f} V", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 150, 255), 2)
                
            # Encontra todos os "pedaços brancos" na máscara
            contornos, _ = cv2.findContours(mascara_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contornos:
                # === FILTRO DE POEIRA ESPACIAL ===
                # Só aceita "ilhas" que tenham uma área visível, ignorando pixels de ruído isolados.
                contornos_validos = [c for c in contornos if cv2.contourArea(c) > 50]
                
                # === FILTRO DO IGNITER (FIO INCANDESCENTE) ===
                if tipo == "ACME" and numero_frame < 166:
                    contornos_validos = []  # Apaga da memória, não é fogo real!

                if contornos_validos:
                    # === MATEMÁTICA DE NUVENS FRAGMENTADAS ===
                    if tipo == "UV":
                        maior_contorno = max(contornos_validos, key=cv2.contourArea)
                        todos_os_pontos = maior_contorno
                    else:
                        todos_os_pontos = np.vstack(contornos_validos)
                    
                    # === MATEMÁTICA DE ANCORAGEM ESPACIAL (SENSOR FUSION) ===
                    if df_ancora is not None and not df_ancora.empty:
                        # 1. Correção do TEMPO (Regra de 3 Dinâmica)
                        total_frames_uv = len(df_ancora)
                        total_frames_atual = len(lista_imagens) 
                        fator_tempo = total_frames_uv / max(1, total_frames_atual)
                        
                        indice_uv_equivalente = int(indice_frame * fator_tempo)
                        
                        if indice_uv_equivalente < total_frames_uv:
                            x_uv = df_ancora.loc[indice_uv_equivalente, 'Centro_X']
                            y_uv = df_ancora.loc[indice_uv_equivalente, 'Centro_Y']
                            
                            # 2. Correção de ESPAÇO (Lê a resolução diretamente da memória)
                            altura_atual, largura_atual = frame.shape[:2]
                            largura_uv = df_ancora['Centro_X'].max() * 2 + 1 
                            altura_uv = df_ancora['Centro_Y'].max() * 2 + 1
                            
                            x = x_uv * (largura_atual / largura_uv)
                            y = y_uv * (altura_atual / altura_uv)
                            
                            # 3. Calcula o raio da fuligem a partir do centro ancorado ajustado!
                            dist_x = todos_os_pontos[:, 0, 0] - x
                            dist_y = todos_os_pontos[:, 0, 1] - y
                            distancias = np.sqrt(dist_x**2 + dist_y**2)
                            raio_pixels = np.max(distancias)
                        else:
                            ((x, y), raio_pixels) = cv2.minEnclosingCircle(todos_os_pontos)
                    else:
                        ((x, y), raio_pixels) = cv2.minEnclosingCircle(todos_os_pontos)

                    # Só medimos se for algo real (raio > 2 pixels)
                    if raio_pixels > 2:
                        # === LÓGICA DE CURVA (Filtro de Inércia Termodinâmica) ===
                        diferenca = int(raio_pixels) - raio_anterior
                        
                        if raio_anterior > 10: 
                            if diferenca < -15: 
                                raio_int = raio_anterior - 5 
                            elif diferenca > 50:
                                raio_int = raio_anterior + 15
                            else:
                                raio_int = int(raio_pixels)
                        else:
                            raio_int = int(raio_pixels)

                        raio_anterior = raio_int 
                        centro_int = (int(x), int(y))
                        area_chama = int(sum([cv2.contourArea(c) for c in contornos_validos]))

                        # === NOVO: Salva os dados matemáticos E FÍSICOS na memória ===
                        dados_extraidos.append({
                            "Arquivo": img_nome,
                            "Camera": tipo,
                            "Tempo_NASA": tempo_atual,       
                            "Metano_g_s": fluxo_metano,      
                            "Radiacao_V": radiacao,
                            "Raio_px": raio_int,
                            "Area_px2": area_chama,
                            "Centro_X": centro_int[0],
                            "Centro_Y": centro_int[1]
                        })      

                        cv2.circle(frame_tela, centro_int, raio_int, (0, 255, 0), 2)
                        cv2.circle(frame_tela, centro_int, 3, (0, 0, 255), -1)

                        # === DESENHA A GEOMETRIA COMPLEXA EXATA (Polígono da Chama) ===
                        cv2.drawContours(frame_tela, contornos_validos, -1, (255, 0, 255), 1)
                    
                        cv2.putText(frame_tela, f"Raio: {raio_int} px", (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(frame_tela, f"Area (Geometria): {area_chama} px2", (20, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

            mascara_colorida = cv2.cvtColor(mascara_binaria, cv2.COLOR_GRAY2BGR)
            tela_unificada = np.hstack((frame_tela, mascara_colorida))
            
            cv2.namedWindow(nome_janela, cv2.WINDOW_NORMAL)
            cv2.imshow(nome_janela, tela_unificada)
            indice_frame += 1
            while True:
                delay = 0 if is_paused else 30
                tecla = cv2.waitKey(delay) & 0xFF
                
                if tecla == ord(' '):
                    is_paused = not is_paused 
                elif tecla == ord('d') or tecla == ord('n'): 
                    break 
                elif tecla == ord('q'): 
                    cv2.destroyAllWindows()
                    break 
                elif not is_paused:
                    break 
                    
    df = pd.DataFrame(dados_extraidos)
    nome_csv = f"Extracao_{tipo}_NASA.csv"
    df.to_csv(nome_csv, index=False)
    print(f"\n[SUCESSO] Dados salvos em {nome_csv}! ({len(df)} frames processados)")
    cv2.destroyAllWindows()

def raio(frame, fundo_estatico, threshold, tipo):
    """
    Recebe um frame da NASA e isola a chama do fundo do universo.
    """
    #A INTNS captura fótons térmicos diretos (Limites frios). 
    # O medianBlur e o Sigma x5 funcionam maravilhosamente bem para ela porque as bordas dela são "duras".
    #  A UV captura uma nuvem de química caótica espalhada (CH*). 
    # O GaussianBlur e o Sigma x1.5 são obrigatórios porque a borda dela é "macia".
    # Por isso devemos modularizar o tratamento para cada camera
    
    # --- NASA DOC REF: s-Flame_data_interpretation_20210920.pdf (Etapa B) ---
    # Remoção de Hot Pixels (Ruído de Radiação). Aplica um filtro de mediana primário 
    # em todas as câmeras antes de qualquer conversão para limpar o "campo de estrelas"!
    frame_denoised = cv2.medianBlur(frame, 3)
    
    # 0. Tratamento de Cor: 
    if len(frame_denoised.shape) == 3:
        frame_cinza = cv2.cvtColor(frame_denoised, cv2.COLOR_BGR2GRAY)
    else:
        frame_cinza = frame_denoised.copy()
    
    if tipo == "UV":
        # A UV filma nuvem de gás espalhado. 
        frame_suave = cv2.GaussianBlur(frame_cinza, (5, 5), 0)
        multiplicador = 1.2
    elif tipo == "INTNS":
        # A INTNS tem limites duros e perfeitos.
        frame_suave = cv2.medianBlur(frame_cinza, 5)
        multiplicador = 2.0 
    elif tipo == "ACME":
        # O MELHOR DOS DOIS MUNDOS: Subtração + Cor
        frame_suave = cv2.medianBlur(frame_denoised, 5) 
        
        if fundo_estatico is None:
            fundo_estatico = frame_suave.copy()
            
        frame_limpo = cv2.subtract(frame_suave, fundo_estatico)
        
        # --- NASA DOC REF: s-Flame_data_interpretation_20210920.pdf (Etapa D) ---
        mask_roi = np.ones(frame_limpo.shape[:2], dtype=np.uint8) * 255
        altura, largura = mask_roi.shape
        cv2.rectangle(mask_roi, (0, int(altura * 0.85)), (largura, altura), 0, -1)
        
        frame_masked = cv2.bitwise_and(frame_limpo, frame_limpo, mask=mask_roi)
        frame_hsv = cv2.cvtColor(frame_masked, cv2.COLOR_BGR2HSV)

        # Filtro de Cor (O metal incandescente vermelho é barrado, só a fuligem amarela passa!)
        limite_inferior = np.array([10, 50, 100])
        limite_superior = np.array([40, 255, 255]) 
        
        mascara_hsv = cv2.inRange(frame_hsv, limite_inferior, limite_superior)
        return mascara_hsv, fundo_estatico
    else:
        # ACME sofre com brilho forte. Por enquanto usamos Mediano.
        frame_suave = cv2.medianBlur(frame_cinza, 5)
        multiplicador = 5.0    

    # --- NASA DOC REF: s-Flame_data_interpretation_20210920.pdf (Etapa C) ---
    if fundo_estatico is None:
        fundo_estatico = frame_suave.copy()

    frame_limpo = cv2.subtract(frame_suave, fundo_estatico)

    # --- NASA DOC REF: s-Flame_data_interpretation_20210920.pdf (Etapa D) ---
    mask_roi_pb = np.ones(frame_limpo.shape, dtype=np.uint8) * 255
    altura_pb, largura_pb = mask_roi_pb.shape
    cv2.rectangle(mask_roi_pb, (0, int(altura_pb * 0.85)), (largura_pb, altura_pb), 0, -1)
    
    frame_masked_pb = cv2.bitwise_and(frame_limpo, frame_limpo, mask=mask_roi_pb)

    # 2. Binarização (Threshold)
    media, desvio = cv2.meanStdDev(frame_masked_pb)
    threshold_estatistico = media[0][0] + (multiplicador * desvio[0][0])
    threshold_estatistico = max(10, threshold_estatistico)
    
    # --- NASA DOC REF: s-Flame_data_interpretation_20210920.pdf (Etapa E) ---
    _, mascara = cv2.threshold(frame_masked_pb, threshold_estatistico, 255, cv2.THRESH_BINARY)
    
    return mascara, fundo_estatico

def extrair_geometria(zip_path, tipo_camera, threshold_binario, df_telemetria, id_teste):
    """
    Função injetada pela IA para rodar a extração em lote sem abrir a tela (foco em performance)
    """
    print(f" -> Extraindo {tipo_camera} ({zip_path.name})...")
    
    if id_teste not in ANCORAGEM:
        print(f"[!] ERRO: Teste {id_teste} não tem ancoragem mapeada!")
        return None
        
    linha_bigbang, f_uv, f_acme, f_intns = ANCORAGEM[id_teste]
    
    if tipo_camera == "UV": frame_ancora = f_uv
    elif tipo_camera == "ACME": frame_ancora = f_acme
    else: frame_ancora = f_intns

    with zipfile.ZipFile(zip_path, 'r') as archive:
        arquivos_img = sorted([f for f in archive.namelist() if f.lower().endswith(('.tif', '.tiff'))])
        resultados = []
        
        for indice, img_nome in enumerate(arquivos_img):
            with archive.open(img_nome) as file:
                img_array = np.frombuffer(file.read(), np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                
            if frame is None: continue
            
            try: numero_frame = int(img_nome.split('_')[-1].split('.')[0])
            except: numero_frame = indice
            
            # Relógio sincronizado
            linha_csv = int(linha_bigbang + (numero_frame - frame_ancora) * (100.0 / 30.0))
            if linha_csv < 0 or linha_csv >= len(df_telemetria): continue
            
            tempo_exato_nasa = df_telemetria.iloc[linha_csv]['Time']
            
            area, raio, brilho = 0, 0, 0
            if numero_frame >= frame_ancora:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
                
                # 1. FILTRAGEM DE RUÍDO: Suaviza o ruído térmico mas preserva a borda do fogo
                gray_filtrado = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
                
                # 2. BRILHO TOTAL: Mede a energia luminosa geral (ajuda a I.A. no efeito chicote)
                brilho = int(np.sum(gray_filtrado)) 
                
                # 3. LIMIAR DE OTSU: Acha o limiar ideal dinamicamente 
                # (Ignora o threshold_binario que enviamos e calcula estatisticamente para salvar as pontas da chama)
                limiar_calculado, binario = cv2.threshold(gray_filtrado, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                contornos, _ = cv2.findContours(binario, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if contornos:
                    maior = max(contornos, key=cv2.contourArea)
                    area = cv2.contourArea(maior)
                    if area > 0: raio = np.sqrt(area / np.pi)

            resultados.append({
                'Tempo_NASA': tempo_exato_nasa,
                f'Area_{tipo_camera}': area,
                f'Raio_{tipo_camera}': raio,
                f'Brilho_{tipo_camera}': brilho
            })
            
        return pd.DataFrame(resultados)

# ==============================================================================
# EXECUÇÃO DO PITCH DE PROVA (PoC)
# ==============================================================================

if __name__ == "__main__":
    print("Iniciando Workflow de Extração Multiespectral da NASA...")
    
    # 1. Roda a UV primeiro (Ela vai gerar o 'Extracao_UV_NASA.csv' limpo)
    # stream(ZIP_UV, "Camera 1: LLL-UV (Matriz Base)", threshold=20, tipo="UV", csv_ancora="Extracao_UV_NASA.csv")
    
    # 2. Roda a ACME consumindo a UV como Âncora Espacial (Resolve a distorção térmica)
    # stream(ZIP_ACME, "Camera 2: ACME (Ancorada)", threshold=50, tipo="ACME", csv_ancora="Extracao_UV_NASA.csv")
    
    # 3. Roda a INTNS também ancorada na UV
    # stream(ZIP_INTNS, "Camera 3: INTNS (Ancorada)", threshold=40, tipo="INTNS")

#Câmera 1 (LLL-UV): Ela enxerga a radiação química do radical CH*. Nós vamos usar essa câmera para extrair a coluna "Raio_da_Reacao_Quimica (mm)".
#Câmera 2 (INTNS): Ela enxerga as bordas térmicas mais fracas. Usaremos para a coluna "Raio_da_Expansao_Termica (mm)".
#Câmera 3 (ACME Colorida): Ela enxerga a luz visível. O amarelo brilhante que vemos não é gás, é Fuligem incandescente. Usaremos ela para criar a coluna "Raio_da_Fuligem (mm)".
# IA (SVR) vai fazer é cruzar as matrizes no tempo (Timestamp): A IA vai aprender que: 
# "Quando injeta X gramas de Metano, a Nuvem UV cresce para 15 pixels, a Fuligem cresce para 8 pixels, e o resultado termodinâmico disso é uma Temperatura de 800°C."

#1 - pegar o tempo da tabela e sincronizar com o dos videos
#2 - ao invez de removermos só quando a tela está toda preta, precisamos saber quando a uma var tem ou algo asssim assim poderemos ficar apenas com os frames que nos interessam
#3- sobrepor as imagens de forma que consigamos fazer uma analise complementar evitando que por falha nossa duas imagens do mesmo tempo indiquem coisas diferentes
#4 - estruturar uma logica de curva assim o raio deve desenvolver uma curva continua

#3. A Incandescência do Metal no frame 160 da ACME
#Isso é física pura! Lembra que a nossa "Subtração de Fundo" apagava o metal porque ele estava na Foto 0? O problema é que, no final do experimento, o tubo de metal da ACME e do ignitor esquentam e começam a brilhar no escuro (incandescência térmica). Como o tubo não estava brilhando na Foto 0, a nossa matemática olha para o novo brilho do tubo e pensa: "Opa, brilho novo! Deve ser a chama!" e a régua vai lá para o tubo!

#4. A Solução do Brilho vs Cor (HSV)
#Para a ACME, você está absolutamente correto: ignorar a cor e usar só o Preto-e-Branco destrói a informação. A chama da ACME é a fuligem amarela e o gás azul. O metal quente brilha vermelho escuro. Se usarmos o espaço de cor HSV (Matiz, Saturação e Brilho), nós podemos mandar o OpenCV caçar exclusivamente a cor da Fuligem, cagando sumariamente para o metal vermelho, não importa o quão quente ele fique!




Nível 1: Machine Learning Clássica (O Baseline)
SVR (Support Vector Regression): Vai tentar traçar uma linha geométrica no espaço multimensional. É excelente para dados contínuos de fluidos, mas sofre se a relação entre o Campo Elétrico e o Fogo não for linear.
XGBoost: Usa árvores de decisão. É imbatível em dados tabulares. Se houver regras "fechadas" (ex: "Se a pressão passar de 2 e a voltagem for 5, a chama apaga"), o XGBoost vai descobrir sozinho.
Nível 2: Deep Learning Físico e Visual (Estado da Arte)
PINNs (Physics-Informed Neural Networks): Aqui nós usaremos PyTorch. A diferença é que a PINN não tenta "decorar" os dados, nós vamos forçar a rede neural a respeitar as leis de conservação de massa e energia (Navier-Stokes) durante o treinamento. Se o dataset for robusto, a PINN vai criar o Gêmeo Digital verdadeiro.
ViT (Vision Transformers): Em vez de jogar apenas os números (Área/Raio) no modelo, nós alimentamos o Transformer com a imagem crua da câmera UV de um lado, e a Termodinâmica do outro. O ViT tem Attention (atenção cruzada) e vai aprender qual pixel da imagem muda de cor quando a voltagem sobe!


Fusão Multimodal Raiz: Você não apenas leu um CSV. Você sincronizou milissegundo a milissegundo os sensores físicos de telemetria com imagens cruas de câmeras científicas.
Visão Computacional de Domínio: Você percebeu que algoritmos genéricos (Otsu) falhavam no fogo espacial e criou um algoritmo matemático de Sigma-Clipping via HSV.
Otimização Bayesiana: Você rodou 150 gerações para blindar o XGBoost contra Overfitting.
O Ápice - PINN (Physics-Informed Neural Networks): Isso é matemática de doutorado. Em vez de fazer a rede neural "chutar" estatística, você embutiu a Lei de Conservação de Massa e Energia no tensor de perda usando derivadas (Autograd). Você forçou a máquina a obedecer a física.

"O fogo no espaço não se comporta como na Terra. Sem a gravidade para criar correntes de convecção térmicas, a chama se torna esférica, sufoca e se expande de forma imprevisível. Se um incêndio começar na Estação Espacial Internacional (ISS) ou na futura viagem a Marte, os modelos da Terra vão falhar em prever a propagação, custando a vida dos astronautas. Para resolver isso, não usamos inteligência artificial genérica. Nós fundimos os dados dos experimentos de combustão da NASA com Visão Computacional, e criamos uma Rede Neural Informada pela Física (PINN). Nossa IA não chuta estatística: ela simula o fogo aprendendo e respeitando as Leis da Termodinâmica. Nós construímos o cérebro do futuro sistema de contenção de incêndios para a colonização interplanetária."


Passo a Passo da Matemática (Como a PINN funciona?)
1. O Problema da IA Comum (Como o XGBoost age) Uma IA comum só olha pros dados (o CSV). Ela tenta traçar uma curva que ligue os pontos do gráfico. A Função de Perda (Loss Function) dela é só uma:

$\text{Loss} = (Área_Prevista - Área_Real)^2$ Se tiver um "buraco" nos dados, a IA comum erra feio, porque ela não sabe as regras do universo.

2. A Injeção da Física (A Equação) Na PINN, nós escrevemos uma Equação Diferencial que governa o nosso fenômeno. No caso do seu tubo de combustão, a expansão do fogo ($A$) ao longo do tempo ($t$) depende de quanto gás entra menos o quanto o calor dissipa. A física teórica diz que:

$\frac{dA}{dt} = \alpha \cdot Gás - \beta \cdot Área$ Onde $\alpha$ (Alpha) é o poder de expansão térmica e $\beta$ (Beta) é a taxa de dissipação no ambiente. Se passarmos tudo para um lado só, temos a equação perfeita, que chamamos de Resíduo Físico ($R$): $R = \frac{dA}{dt} - (\alpha \cdot Gás) + (\beta \cdot Área)$ Pela lei da física, $R$ tem que ser igual a Zero.

3. O Milagre do "Autograd" (A Derivada) O PyTorch possui uma ferramenta de cálculo avançado chamada Autograd. Em vez de fazer uma aproximação tosca, ele consegue calcular a Derivada Exata ($\frac{dA}{dt}$) de como a área está mudando a cada milissegundo dentro da rede neural.

4. A Nova Função de Perda (O Treinamento) Na PINN, a rede neural é punida por duas coisas ao mesmo tempo:

$\text{Loss Total} = \text{Erro dos Dados} + \text{Erro da Física}$ Enquanto a rede treina, ela tenta adivinhar o tamanho da chama, mas ao mesmo tempo ela tenta adivinhar quais são os verdadeiros valores de $\alpha$ e $\beta$. Se ela chutar uma curva de fogo que viola a Equação Diferencial (fizer o Resíduo $R$ ser diferente de zero), ela recebe um "choque" matemático (a Loss explode). O resultado? A IA descobre as Constantes Físicas reais da câmara de combustão (Alpha e Beta) e desenha uma curva que é estatisticamente precisa E obedece às leis de Newton/Termodinâmica!


Gêmeo Digital (Simulador)
O que o usuário insere (Inputs):

Tempo
Quantidade de Propelente (Vazão do Gás)
O que a IA cospe (Outputs / Multi-Output PINN):

Raio_UV (Tamanho da Chama)
TCBurner (Temperatura da Combustão)
Radiometer (Radiação/Calor gerado)
IonCurrent (Nível de Ionização Química)
Como a Matemática lida com isso? Em vez de ter apenas 1 equação diferencial, nós embutimos um Sistema de Equações Diferenciais Acopladas no Autograd.

A Taxa de variação do Raio depende do Gás e da Temperatura.
A Taxa de variação da Temperatura depende do Raio atual e da dissipação de calor.
A Radiação depende diretamente do quadrado da Temperatura (Lei de Stefan-Boltzmann).


Aumentar o nosso banco de dados

tesatar para plano 3d com Navier-Stokes

Extração Visuo-Espacial (OpenCV): Nós rodamos um algoritmo chamado Dense Optical Flow (Farneback) no vídeo UV da NASA. Isso vai desenhar "setas" (vetores) na tela mostrando para onde o gás está indo e com qual força.
Hidden Fluid Mechanics (HFM): Esse é o nome real da técnica inventada pelo criador das PINNs (Maziar Raissi). Você joga esse vídeo cheio de vetores na PINN.
A PINN de Navier-Stokes: A IA pega as posições $(x, y, t)$, tenta prever a pressão invisível do gás e as velocidades $(u, v)$, e é punida pelas Derivadas Parciais de Navier-Stokes.

A Minha Sugestão de Ouro para o Hackathon: Nós não precisamos treinar uma PINN de Navier-Stokes para ter os vetores. Nós podemos usar o OpenCV para gerar o Fluxo Óptico (os vetores visuais) e mostrar isso no projeto como a nossa "Mapeação de Fluidos".



E sobre a sua dúvida: "Apenas ver o transito de um frame para outro vai trazer o 3d que nós precisamos?"
DIRETO E RETO: SIM! E o motivo é que estamos no ESPAÇO. 
Na Terra, o fogo sofre convecção (o ar quente sobe e faz aquela forma de gota ou cone), então um vídeo 2D não te conta toda a história 3D. 
Mas em MICROGRAVIDADE, a combustão é perfeitamente esférica e simétrica a partir do ponto de ignição (Axisimétrica). Se você tem a "fatia" 2D perfeita do Optical Flow (velocidades U e V no eixo X e Y), você só precisa rotacionar essa fatia matematicamente ao redor do centro e BUM: você tem o campo de velocidade 3D completo da esfera de gás! Na física de fluidos, usamos as Equações de Navier-Stokes Axisimétricas.

Aqui estão as Equações de Navier-Stokes originais que justificam todo o modelo (pode colocar nos slides para chocar os juízes):

1. Equação da Continuidade (Conservação de Massa):
$\nabla \cdot \vec{u} = 0 \quad \text{ou} \quad \frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{u}) = 0$
(Garante que todo o combustível ejetado se converta em expansão volumétrica).

2. Conservação de Momento (Navier-Stokes Pura):
$\rho \left( \frac{\partial \vec{u}}{\partial t} + \vec{u} \cdot \nabla \vec{u} \right) = -\nabla p + \mu \nabla^2 \vec{u} + \vec{f}$
(No nosso caso do Optical Flow, $\vec{u}$ são os vetores verdes do OpenCV, $p$ é a pressão térmica do gás e $\mu$ é a viscosidade do combustível).

3. Conservação de Energia (O que rege a nossa Temperatura e Raio):
$\rho c_p \left( \frac{\partial T}{\partial t} + \vec{u} \cdot \nabla T \right) = \nabla \cdot (k \nabla T) + Q_{combustao} - Q_{radiacao}$
(A taxa que a Temperatura sobe depende do calor da queima $Q_{combustao}$ menos a radiação que vaza pro espaço $Q_{radiacao}$. É exatamente isso que a nossa Multi-Output PINN está simulando!)
 estamos no ESPAÇO.

Na Terra, o fogo tem forma de gota (convecção). Então uma visão 2D te conta só metade da história. Mas em MICROGRAVIDADE, a combustão é uma Esfera Perfeita! (Axisimétrica).

Isso significa que, se você tem a "fatia" 2D perfeita do Optical Flow (como o script que criamos faz), a matemática nos garante que o comportamento nos eixos de profundidade ($Z$) é idêntico ao eixo $X$ e $Y$. Nós pegamos aquela "fatia" 2D de vetores e a rotacionamos ao redor do centro. BUM! Nós temos o campo de velocidade 3D completo da Esfera de Gás!