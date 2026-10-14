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



import zipfile

import numpy as np

import cv2

import pandas as pd



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



            # Se não há nenhum pixel branco na máscara, é porque não há fogo.

           # if cv2.countNonZero(mascara_binaria) == 0:

               # print(f"[{img_nome}] Sem chamas detectadas. Ignorando frame.")

               # continue # Pula a exibição/cálculo e puxa a próxima foto!

            #indice_frame += 1

             

# Para garantir que o círculo Verde brilhe bonito na tela (mesmo nas câmeras P&B), criamos uma tela colorida:

            frame_tela = frame.copy()

            if len(frame_tela.shape) == 2: # Se a imagem for monocromática

                frame_tela = cv2.cvtColor(frame_tela, cv2.COLOR_GRAY2BGR)



                        # === SINCRONIZAÇÃO DA TELEMETRIA ABSOLUTA (SENSOR FUSION) ===

            # Pega o número do frame para qualquer câmera (Puxa do "00166.tif")

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

                # A câmera ACME se cega com o brilho do fio entre os frames 161 e 165.

                # Como sabemos que a verdadeira combustão só ocorre no 166, ignoramos o que vem antes!

                if tipo == "ACME" and numero_frame < 166:

                    contornos_validos = []  # Apaga da memória, não é fogo real!



                if contornos_validos:

                    # === MATEMÁTICA DE NUVENS FRAGMENTADAS ===

                    # Junta TODOS os pontos de TODOS os contornos encontrados numa única lista gigante

                    if tipo == "UV":

                        # A UV sofre com poeira isolada. Em vez de juntar tudo, pegue só a MAIOR ilha de fogo!

                        maior_contorno = max(contornos_validos, key=cv2.contourArea)

                        todos_os_pontos = maior_contorno

                    else:

                        # As outras lentes têm a chama mais bem definida, podem juntar tudo

                        todos_os_pontos = np.vstack(contornos_validos)



                   

                                        # === MATEMÁTICA DE ANCORAGEM ESPACIAL (SENSOR FUSION) ===

                    if df_ancora is not None and not df_ancora.empty:

                       

                        # 1. Correção do TEMPO (Regra de 3 Dinâmica)

                        total_frames_uv = len(df_ancora)

                        total_frames_atual = len(lista_imagens) # Usa o total real do ZIP atual! (176 ou 607)

                        fator_tempo = total_frames_uv / max(1, total_frames_atual)

                       

                        indice_uv_equivalente = int(indice_frame * fator_tempo)

                       

                        if indice_uv_equivalente < total_frames_uv:

                            x_uv = df_ancora.loc[indice_uv_equivalente, 'Centro_X']

                            y_uv = df_ancora.loc[indice_uv_equivalente, 'Centro_Y']

                           

                            # 2. Correção de ESPAÇO (Lê a resolução diretamente da memória)

                            altura_atual, largura_atual = frame.shape[:2]

                           

                            # Descobre o maior eixo registrado no CSV da UV para usar de escala

                            # (Adiciona +1 para evitar divisão por zero)

                            largura_uv = df_ancora['Centro_X'].max() * 2 + 1

                            altura_uv = df_ancora['Centro_Y'].max() * 2 + 1

                           

                            # Escala as coordenadas gigantes da UV para caber na telinha atual

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

                        # Se não tiver âncora (ex: na própria UV), usa a matemática padrão

                        ((x, y), raio_pixels) = cv2.minEnclosingCircle(todos_os_pontos)







               

                 # Só medimos se for algo real (raio > 2 pixels)

                    if raio_pixels > 2:

                       

                        # === LÓGICA DE CURVA (Filtro de Inércia Termodinâmica) ===

                        # Se o raio der um pulo maior que 20 pixels de uma vez, é ruído!

                        # Mantemos o raio anterior para a curva não quebrar.

                        diferenca = int(raio_pixels) - raio_anterior

                       

                        if raio_anterior > 10:

                            if diferenca < -15:

                                # Regra 1: Amortece quedas (Fogo não some do nada)

                                raio_int = raio_anterior - 5

                            elif diferenca > 50:

                                # Regra 2: Amortece saltos bruscos

                                raio_int = raio_anterior + 15

                            else:

                                raio_int = int(raio_pixels)

                        else:

                            raio_int = int(raio_pixels)



                        # VOCÊ TINHA APAGADO ESTA LINHA! ELA É O CORAÇÃO DA INÉRCIA:

                        raio_anterior = raio_int

                        centro_int = (int(x), int(y))

                         # Calcula a "Massa" geométrica total da chama (em Pixels Quadrados)

                        area_chama = int(sum([cv2.contourArea(c) for c in contornos_validos]))



                    # === NOVO: Salva os dados matemáticos E FÍSICOS na memória ===

                    dados_extraidos.append({

                            "Arquivo": img_nome,

                            "Camera": tipo,

                            "Tempo_NASA": tempo_atual,       # <--- Novo cruzamento

                            "Metano_g_s": fluxo_metano,      # <--- Novo cruzamento

                            "Radiacao_V": radiacao,

                            "Raio_px": raio_int,

                            "Area_px2": area_chama,



                            "Centro_X": centro_int[0],

                            "Centro_Y": centro_int[1]

                        })      



                    cv2.circle(frame_tela, centro_int, raio_int, (0, 255, 0), 2)

                    cv2.circle(frame_tela, centro_int, 3, (0, 0, 255), -1)



                      # === DESENHA A GEOMETRIA COMPLEXA EXATA (Polígono da Chama) ===

                        # Isso vai desenhar uma linha roxa contornando cada detalhe irregular do fogo!

                    cv2.drawContours(frame_tela, contornos_validos, -1, (255, 0, 255), 1)

               

                    cv2.putText(frame_tela, f"Raio: {raio_int} px", (20, 180),

                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    cv2.putText(frame_tela, f"Area (Geometria): {area_chama} px2", (20, 210),

                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)



                       

           

            # Para colar as duas, elas precisam ter a mesma profundidade de cor (3 canais)

            mascara_colorida = cv2.cvtColor(mascara_binaria, cv2.COLOR_GRAY2BGR)

           

            # Cola a Original (com o circulo) e a Máscara na mesma tela

            tela_unificada = np.hstack((frame_tela, mascara_colorida))

           

            # Exibe tudo em UMA única janela!

            cv2.namedWindow(nome_janela, cv2.WINDOW_NORMAL)

            cv2.imshow(nome_janela, tela_unificada)

            indice_frame += 1

            while True:

                # Se estiver pausado, o delay é 0 (congela a tela). Se não, o delay é 30ms (toca o vídeo).

                delay = 0 if is_paused else 30

                tecla = cv2.waitKey(delay) & 0xFF

               

                if tecla == ord(' '):  # Se o usuário apertar ESPAÇO

                    is_paused = not is_paused # Inverte o estado (Play <-> Pause)

                elif tecla == ord('d') or tecla == ord('n'): # 'D' ou 'N' para avançar 1 frame

                    break # Quebra a pausa atual, avança 1 foto, e no próximo loop congela de novo!

                elif tecla == ord('q'): # Se o usuário apertar 'q'

                    cv2.destroyAllWindows()

                    break # Encerra essa câmera, QUEBRA O LOOP e vai salvar o CSV!

                elif not is_paused:

                    break # Sai da pausa e permite que o loop 'for' puxe a próxima imagem!

    # === NOVO: Quando o zip acabar (ou você apertar Q), salva tudo num Excel (CSV) ===

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

    # Se a câmera for a ACME (Colorida / 3 canais), converte para Preto e Branco.

    if len(frame_denoised.shape) == 3:

        frame_cinza = cv2.cvtColor(frame_denoised, cv2.COLOR_BGR2GRAY)

    else:

        frame_cinza = frame_denoised.copy()

   

    if tipo == "UV":

     # A UV filma nuvem de gás espalhado.

        # GaussianBlur funde o gás fraco numa bolha contínua.

        frame_suave = cv2.GaussianBlur(frame_cinza, (5, 5), 0)

        multiplicador = 1.2 # Régua branda para não arrancar pedaços da nuvem

   

    #median blur nao deveria ser tirado do acme uma vez que perderiamos o nuance das cores num limiar?

    elif tipo == "INTNS":

 # A INTNS tem limites duros e perfeitos.

        # Filtro Mediano mata as estrelas do fundo maravilhosamente bem.

        frame_suave = cv2.medianBlur(frame_cinza, 5)

        multiplicador = 2.0 # Régua severa para matar tudo que não for fogo denso



    elif tipo == "ACME":

        # O MELHOR DOS DOIS MUNDOS: Subtração + Cor

        # 1. Usa a imagem original COLORIDA que já foi limpa da radiação!

        frame_suave = cv2.medianBlur(frame_denoised, 5)

       

        # 2. Salva o Molde Colorido do Metal Frio

        if fundo_estatico is None:

            fundo_estatico = frame_suave.copy()

           

        # 3. Subtrai o Metal Frio (Deixa apenas a Chama + O Metal que esquentou)

        frame_limpo = cv2.subtract(frame_suave, fundo_estatico)

       

                # --- NASA DOC REF: s-Flame_data_interpretation_20210920.pdf (Etapa D) ---

        # Máscara de ROI: Oculta a haste do queimador e fibras TFP que obstruem a câmera

        mask_roi = np.ones(frame_limpo.shape[:2], dtype=np.uint8) * 255

        altura, largura = mask_roi.shape

        # Bloqueia os últimos 15% inferiores da imagem (área de obstrução física das hastes)

        cv2.rectangle(mask_roi, (0, int(altura * 0.85)), (largura, altura), 0, -1)

       

        # Usa o mask_roi cru (1 canal), o OpenCV aplica em todos os canais de cor sozinho!

        frame_masked = cv2.bitwise_and(frame_limpo, frame_limpo, mask=mask_roi)



        # 4. Transforma o que sobrou (com ROI oculto) em HSV

        frame_hsv = cv2.cvtColor(frame_masked, cv2.COLOR_BGR2HSV)



                # 5. Filtro de Cor (O metal incandescente vermelho é barrado, só a fuligem amarela passa!)

        limite_inferior = np.array([10, 50, 100]) # Afrouxei o brilho pra não matar a borda da fuligem

        limite_superior = np.array([40, 255, 255])

       

        mascara_hsv = cv2.inRange(frame_hsv, limite_inferior, limite_superior)



        # Retorna a máscara perfeita, pulando o Sigma-Clipping lá de baixo!

        return mascara_hsv, fundo_estatico



    else:

        # ACME sofre com brilho forte. Por enquanto usamos Mediano.

        # Mais tarde substituiremos isso pelo filtro de cor HSV!

        frame_suave = cv2.medianBlur(frame_cinza, 5)

        multiplicador = 5.0    



    # --- NASA DOC REF: s-Flame_data_interpretation_20210920.pdf (Etapa C) ---

    #Remoção de frame inicial fica para todos

    if fundo_estatico is None:

        # Se for a primeira foto do vídeo, salva ela como o "Molde" de metal

        #como estamos rodadando um zip por vez o fundo volta a ser none no proximo ciclo

        fundo_estatico = frame_suave.copy()



    # Subtrai o "Molde" do frame atual. O metal vai dar resultado 0 (Preto)!

    frame_limpo = cv2.subtract(frame_suave, fundo_estatico)



    # --- NASA DOC REF: s-Flame_data_interpretation_20210920.pdf (Etapa D) ---

    # Máscara de ROI para as Câmeras em Preto e Branco (INTNS e UV)

    mask_roi_pb = np.ones(frame_limpo.shape, dtype=np.uint8) * 255

    altura_pb, largura_pb = mask_roi_pb.shape

    cv2.rectangle(mask_roi_pb, (0, int(altura_pb * 0.85)), (largura_pb, altura_pb), 0, -1)

   

    # Aplica o adesivo cego no metal

    frame_masked_pb = cv2.bitwise_and(frame_limpo, frame_limpo, mask=mask_roi_pb)



    # 2. Binarização (Threshold)

    # (Sigma-Clipping) Calcula a Média e o Desvio Padrão do brilho na imagem inteira

    media, desvio = cv2.meanStdDev(frame_masked_pb)

    # O threshold usa o multiplicador específico da lente!

    threshold_estatistico = media[0][0] + (multiplicador * desvio[0][0])

    threshold_estatistico = max(10, threshold_estatistico) # Chão de fábrica

   

    # --- NASA DOC REF: s-Flame_data_interpretation_20210920.pdf (Etapa E) ---

    # A documentação recomenda OTSU, mas Sigma-Clipping substitui perfeitamente para chamas pequenas.

    #Iguinorar entrada threshold e tentar automatizar por histograma de otsu (não funcionou chama muito pequena)

    # segundo teste com Sigma-Clipping

    _, mascara = cv2.threshold(frame_masked_pb, threshold_estatistico, 255, cv2.THRESH_BINARY)



   

    return mascara, fundo_estatico



# ==============================================================================

# EXECUÇÃO DO PITCH DE PROVA (PoC)

# ==============================================================================



if __name__ == "__main__":

    print("Iniciando Workflow de Extração Multiespectral da NASA...")

   

     # 1. Roda a UV primeiro (Ela vai gerar o 'Extracao_UV_NASA.csv' limpo)

    stream(ZIP_UV, "Camera 1: LLL-UV (Matriz Base)", threshold=20, tipo="UV", csv_ancora="Extracao_UV_NASA.csv")

   

    # 2. Roda a ACME consumindo a UV como Âncora Espacial (Resolve a distorção térmica)

    stream(ZIP_ACME, "Camera 2: ACME (Ancorada)", threshold=50, tipo="ACME", csv_ancora="Extracao_UV_NASA.csv")

   

    # 3. Roda a INTNS também ancorada na UV

    stream(ZIP_INTNS, "Camera 3: INTNS (Ancorada)", threshold=40, tipo="INTNS")





   # Tentei otimizar o threshold particularizando cada tipo de captura

   # Ideia de testar valores automaticamente para minimizar a variância do objeto e separar do fundo

   # Procurei presedencia da ideia, achei algo parecido com Teoria de Nobuyuki Otsu (1979). função flag

   # Não funciona bem. Sigma-Clipping funcionou melhor para cameras INTNS mas nem tanto para as UVs, testar uma abordagem Modular para cada camera evitando perder informações.

   



#Câmera 1 (LLL-UV): Ela enxerga a radiação química do radical CH*. Nós vamos usar essa câmera para extrair a coluna "Raio_da_Reacao_Quimica (mm)".

#Câmera 2 (INTNS): Ela enxerga as bordas térmicas mais fracas. Usaremos para a coluna "Raio_da_Expansao_Termica (mm)".

#Câmera 3 (ACME Colorida): Ela enxerga a luz visível. O amarelo brilhante que vemos não é gás, é Fuligem incandescente. Usaremos ela para criar a coluna "Raio_da_Fuligem (mm)".

# IA (SVR) vai fazer é cruzar as matrizes no tempo (Timestamp): A IA vai aprender que:

# "Quando injeta X gramas de Metano, a Nuvem UV cresce para 15 pixels, a Fuligem cresce para 8 pixels, e o resultado termodinâmico disso é uma Temperatura de 800°C."



#1 - pegar o tempo da tabela e sincronizar com o dos videos



#2 - ao invez de removermos só quando a tela está toda preta, precisamos saber quando a uma var tem ou algo asssim assim poderemos ficar apenas com os frames que nos interessam



#3- sobrepor as imagens de forma que consigamos fazer uma analise complementar evitando que por falha nossa duas imagens do mesmo tempo indiquem coisas diferentes

# Timestamps



#4 - estruturar uma logica de curva assim o raio deve desenvolver uma curva continua

#(se implementarmos corretamente as anteriores provavelmente nem precisaremos disso)(O Filtro de Inércia)



#3. A Incandescência do Metal no frame 160 da ACME

#Isso é física pura! Lembra que a nossa "Subtração de Fundo" apagava o metal porque ele estava na Foto 0? O problema é que, no final do experimento, o tubo de metal da ACME e do ignitor esquentam e começam a brilhar no escuro (incandescência térmica). Como o tubo não estava brilhando na Foto 0, a nossa matemática olha para o novo brilho do tubo e pensa: "Opa, brilho novo! Deve ser a chama!" e a régua vai lá para o tubo!



#4. A Solução do Brilho vs Cor (HSV)

#Para a ACME, você está absolutamente correto: ignorar a cor e usar só o Preto-e-Branco destrói a informação. A chama da ACME é a fuligem amarela e o gás azul. O metal quente brilha vermelho escuro. Se usarmos o espaço de cor HSV (Matiz, Saturação e Brilho), nós podemos mandar o OpenCV caçar exclusivamente a cor da Fuligem, cagando sumariamente para o metal vermelho, não importa o quão quente ele fique! 

