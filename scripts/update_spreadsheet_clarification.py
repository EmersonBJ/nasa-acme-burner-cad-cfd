import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

excel_path = r'D:\NASA_CAD_Reverse_Engineering\pecas_faltantes.xlsx'
csv_path = r'D:\NASA_CAD_Reverse_Engineering\pecas_faltantes.csv'
html_path = r'D:\NASA_CAD_Reverse_Engineering\pecas_faltantes.html'

wb = openpyxl.load_workbook(excel_path)
ws = wb.active

headers = [cell.value for cell in ws[1]]
print("Headers:", headers)

col_feito = headers.index('Feito? (SIM / NÃO)') + 1
col_decisao = headers.index('Precisa Fazer no CAD? (Decisão de Engenharia)') + 1
col_status = headers.index('Status no CAD') + 1
col_pn = headers.index('Part Number NASA') + 1
col_obs = headers.index('Papel Físico / Observações de Modelagem (Precisa Fazer ou Não?)') + 1

# Styles
fill_green = PatternFill(start_color="D4EDDA", end_color="D4EDDA", fill_type="solid") # light green
fill_blue = PatternFill(start_color="D1ECF1", end_color="D1ECF1", fill_type="solid") # light blue/info
fill_gray = PatternFill(start_color="E2E3E5", end_color="E2E3E5", fill_type="solid") # neutral gray
font_green = Font(color="155724", bold=True)
font_blue = Font(color="0C5460", bold=True)
font_gray = Font(color="383D41", bold=False)

for row in range(2, ws.max_row + 1):
    pn = str(ws.cell(row=row, column=col_pn).value or '').strip()
    
    # 1. UML Window Covers
    if 'UML1' in pn or 'UML2' in pn or 'UML4' in pn:
        ws.cell(row=row, column=col_feito).value = 'SIM'
        ws.cell(row=row, column=col_feito).fill = fill_green
        ws.cell(row=row, column=col_feito).font = font_green
        ws.cell(row=row, column=col_decisao).value = 'JÁ MODELADO'
        ws.cell(row=row, column=col_status).value = 'Modelado (.stp pronto / Integrado)'
        
    # 2. Burner Support Tube 1219
    elif pn == 'S1101MFD1219':
        ws.cell(row=row, column=col_feito).value = 'SIM'
        ws.cell(row=row, column=col_feito).fill = fill_green
        ws.cell(row=row, column=col_feito).font = font_green
        ws.cell(row=row, column=col_decisao).value = 'JÁ MODELADO'
        ws.cell(row=row, column=col_status).value = 'Modelado (.step pronto / Integrado no Queimador S1101MFA1216_E)'

    # 3. Burner Stem Cover 1269
    elif pn == 'S1101MFD1269':
        ws.cell(row=row, column=col_feito).value = 'SIM'
        ws.cell(row=row, column=col_feito).fill = fill_green
        ws.cell(row=row, column=col_feito).font = font_green
        ws.cell(row=row, column=col_decisao).value = 'JÁ ATENDIDO / SIMPLIFICADO NO BURNER'
        ws.cell(row=row, column=col_status).value = 'Integrado na Montagem do Queimador S1101MFA1216'
        ws.cell(row=row, column=col_obs).value = '[INTEGRADO NO QUEIMADOR]: A cobertura da base da haste já está incorporada no flange base e no diâmetro de assentamento do queimador S1101MFA1216_E.'

    # 4. Igniter internal parts (1338, 1336, 1333, 1334, 1335, 1337, 1321, 1332)
    elif pn in ['S1101MFA1338', 'S1101MFA1336', 'S1101MFD1333', 'S1101MFD1334', 'S1101MFD1335', 'S1101MFD1337', 'S1101MFD1321', 'S1101MFA1332']:
        ws.cell(row=row, column=col_feito).value = 'SIM'
        ws.cell(row=row, column=col_feito).fill = fill_green
        ws.cell(row=row, column=col_feito).font = font_green
        ws.cell(row=row, column=col_decisao).value = 'JÁ ATENDIDO NA MONTAGEM S1101MFA1300'
        ws.cell(row=row, column=col_status).value = 'Integrado na Montagem do Ignitor (s1101mfa1300 / s1101mfa1339)'
        ws.cell(row=row, column=col_obs).value = '[JÁ ATENDIDO NA MONTAGEM GLOBAL DO IGNITOR]: Subcomponente interno da ponta/presilha do ignitor. A geometria macro completa já existe em s1101mfa1300_montado_corrigido.stp e na ponta s1101mfa1339. Para o Ansys CFD, detalhes internos de fixação sofrem defeaturing para viabilizar a malha.'

    # 5. External Optics / PMTs (2316, 1523)
    elif pn == 'S1101MFA2316':
        ws.cell(row=row, column=col_feito).value = 'NÃO PRECISA'
        ws.cell(row=row, column=col_feito).fill = fill_gray
        ws.cell(row=row, column=col_feito).font = font_gray
        ws.cell(row=row, column=col_decisao).value = 'NÃO PRECISA (Fora do Fluido CFD / Sensor Externo)'
        ws.cell(row=row, column=col_status).value = 'Dispensado para CFD / Físico Externo'
        ws.cell(row=row, column=col_obs).value = '[FORA DO CFD]: Filtro óptico azul de vidro Schott BG7 montado na frente do sensor PMT óptico externo. Fica fora da câmara e não tem contato com os gases, fluido ou chama.'

    elif pn == 'S1101MFD1523':
        ws.cell(row=row, column=col_feito).value = 'NÃO PRECISA'
        ws.cell(row=row, column=col_feito).fill = fill_gray
        ws.cell(row=row, column=col_feito).font = font_gray
        ws.cell(row=row, column=col_decisao).value = 'NÃO PRECISA (Fora do Fluido CFD / Máscara Óptica)'
        ws.cell(row=row, column=col_status).value = 'Dispensado para CFD / Máscara de Sensor'
        ws.cell(row=row, column=col_obs).value = '[FORA DO CFD]: Placa de abertura limitadora de campo óptico (FOV) do radiômetro externo. Radiação no Ansys é calculada por modelo volumétrico numérico (DO/P1).'

    # 6. CIR-CHAMBER-83L
    elif 'CIR-CHAMBER' in pn:
        ws.cell(row=row, column=col_feito).value = 'EM MONTAGEM'
        ws.cell(row=row, column=col_feito).fill = fill_blue
        ws.cell(row=row, column=col_feito).font = font_blue
        ws.cell(row=row, column=col_decisao).value = 'CONTORNO DE PAREDE CFD (83L)'
        ws.cell(row=row, column=col_status).value = 'Em Montagem (Anel 8 Janelas Pronto + Volume 83L)'
        ws.cell(row=row, column=col_obs).value = '[CONTORNO DO CFD]: Define o volume gasoso de 83 litros e as paredes externas. O anel das 8 janelas e tampas já está pronto (cir_anel_8_janelas_e_tampas_ansys.stp).'

wb.save(excel_path)
print("Updated excel:", excel_path)

# Also update CSV and HTML
df = pd.read_excel(excel_path)
df.to_csv(csv_path, index=False, encoding='utf-8-sig')
df.to_html(html_path, index=False, classes='table table-striped table-bordered table-hover')
print("Updated CSV and HTML successfully!")
