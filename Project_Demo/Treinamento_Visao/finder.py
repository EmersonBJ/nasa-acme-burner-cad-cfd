import cv2
import zipfile
import numpy as np
import pandas as pd
from pathlib import Path

def achar_linha_csv_big_bang(pasta_id):
    caminho_csv = Path(rf"D:\NASA\dataset\19304\{pasta_id}\19304{pasta_id}_data.csv")
    if not caminho_csv.exists(): return None
    df = pd.read_csv(caminho_csv, skiprows=1)
    try:
        linha_ignicao = df[df['IonCurrent'] > -0.5].index[0]
        print(f"\n[FÍSICA] {pasta_id} -> CSV Linha: {linha_ignicao}")
        return linha_ignicao
    except: return None

def tocar_video_para_inspecao(caminho_zip):
    print(f"\n[PLAY] Inspecionando {caminho_zip.name}")
    print("-> ESPAÇO: Pausa | D: Avança | A: Volta | Q: Próximo vídeo")
    
    with zipfile.ZipFile(caminho_zip, 'r') as archive:
        arquivos_img = sorted([f for f in archive.namelist() if f.lower().endswith(('.tif', '.tiff'))])
        if not arquivos_img: return
            
        indice, pausado = 0, False
        while 0 <= indice < len(arquivos_img):
            img_nome = arquivos_img[indice]
            
            try: numero_frame = int(img_nome.split('_')[-1].split('.')[0])
            except: numero_frame = indice
                
            with archive.open(img_nome) as file:
                frame = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
                
            if frame is None:
                indice += 1
                continue
                
            frame_resized = cv2.resize(frame, (800, 800))
            cv2.putText(frame_resized, f"FRAME: {numero_frame}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
            cv2.imshow("FINDER NASA", frame_resized)
            
            tecla = cv2.waitKey(0 if pausado else 60) & 0xFF
            if tecla in (ord('q'), ord('Q')): break
            elif tecla == ord(' '): pausado = not pausado
            elif tecla in (ord('d'), ord('D')): indice += 1; pausado = True
            elif tecla in (ord('a'), ord('A')): indice -= 1; pausado = True
            elif not pausado: indice += 1
                
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # TODAS as pastas do Dataset 19304!
    testes = ['A1', 'A2', 'A3', 'A7', 'B1', 'B2', 'B3', 'B4', 'K1'] 
    
    for teste in testes:
        print("\n" + "="*60)
        print(f" MAPEANDO TESTE {teste}")
        print("="*60)
        achar_linha_csv_big_bang(teste)
        
        # Câmera 1: UV
        zip_uv = list(Path(r"D:\NASA\dataset\19304\video").rglob(f"*{teste}*UV.zip"))
        if zip_uv: tocar_video_para_inspecao(zip_uv[0])
            
                # Câmera 2: ACME
        zip_acme = list(Path(r"D:\NASA\dataset\19304\video").rglob(f"*{teste}*ACME*.zip"))
        # Prioriza o arquivo "_Converted" se ele existir
        zip_acme = sorted(zip_acme, key=lambda x: "Converted" not in str(x))
        if zip_acme: tocar_video_para_inspecao(zip_acme[0])
            
        # Câmera 3: INTNS
        zip_intns = list(Path(r"D:\NASA\dataset\19304\video").rglob(f"*{teste}*INTNS*.zip"))
        # Prioriza o arquivo "_ALL" se ele existir
        zip_intns = sorted(zip_intns, key=lambda x: "ALL" not in str(x))
        if zip_intns: tocar_video_para_inspecao(zip_intns[0])
#19304
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


#19254

#19256

#19308 (Quatro dias depois do nosso teste!)

#19352

#20006

#20013

#20024

#20029

#20132