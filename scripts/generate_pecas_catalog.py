import os
import csv
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_path = os.path.join(root, 'pecas_faltantes.csv')
xlsx_path = os.path.join(root, 'pecas_faltantes.xlsx')
html_path = os.path.join(root, 'pecas_faltantes.html')

dwg_dir = os.path.join(root, 'PSI-Documents', 'Engineering Documents', 'Desenhos_Tecnicos_NASA')

# Index PDFs
pdf_map = {}
for dirpath, _, filenames in os.walk(dwg_dir):
    for f in filenames:
        if f.lower().endswith('.pdf'):
            rel = os.path.relpath(os.path.join(dirpath, f), root).replace('\\', '/')
            pdf_map[f.lower()] = rel

# Index STEPs
step_map = {}
for dirpath, _, filenames in os.walk(root):
    if '.git' in dirpath: continue
    for f in filenames:
        if f.lower().endswith(('.step', '.stp')):
            rel = os.path.relpath(os.path.join(dirpath, f), root).replace('\\', '/')
            step_map[f.lower()] = rel

def find_pdf(pn, fallback=""):
    if fallback and os.path.exists(os.path.join(root, fallback.replace('/', '\\'))):
        return fallback
    pn_clean = pn.lower().replace('-', '').replace('_', '').replace(' ', '')
    matches = []
    for k, v in pdf_map.items():
        k_clean = k.replace('-', '').replace('_', '').replace(' ', '')
        if pn_clean in k_clean:
            matches.append(v)
    if matches:
        matches.sort(key=lambda x: len(os.path.basename(x)))
        return matches[0]
    return fallback

def find_step(pn, fallback=""):
    if fallback and os.path.exists(os.path.join(root, fallback.replace('/', '\\'))):
        return fallback
    pn_clean = pn.lower().replace('-', '').replace('_', '').replace(' ', '')
    matches = []
    for k, v in step_map.items():
        k_clean = k.replace('-', '').replace('_', '').replace(' ', '')
        if pn_clean in k_clean:
            priority = 0 if 'cads_nosso' in v.lower() else 1
            matches.append((priority, len(v), v))
    if matches:
        matches.sort()
        return matches[0][2]
    return fallback

# Read source CSV from D:\NASA
src_csv = r'D:\NASA\pecas_faltantes.csv'
with open(src_csv, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    raw_rows = list(reader)

headers = [
    'Grupo / Subsistema',
    'Prioridade (s-Flame)',
    'Feito? (SIM / NÃO)',
    'Part Number NASA',
    'Nome do Componente / Montagem (Inglês NASA)',
    'Tipo',
    'Status no CAD',
    'Papel no Ansys / Digital Twin',
    'Arquivo STEP (.STEP / .STP)',
    'Arquivo Desenho Técnico (.PDF)',
    'Papel Físico no Experimento e Simulação Multifísica (Ansys Fluent / Digital Twin)',
    'Documento / Desenho de Referência NASA'
]

data_rows = raw_rows[1:]

def unformula(v):
    if not v: return ""
    m = re.search(r'=HYPERLINK\("([^"]+)",\s*"([^"]+)"\)', v)
    if m:
        return m.group(2)
    return v

def sanitize_text(text):
    text = text.replace('Fluent e PINN', 'Fluent e Gêmeo Digital')
    text = text.replace('Ansys Fluent e 4D PINN', 'Ansys Fluent e Gêmeo Digital 3D')
    text = text.replace('4D PINN', 'Gêmeo Digital 3D')
    text = text.replace('no PINN', 'no Gêmeo Digital')
    text = text.replace('pelo PINN', 'pelo Gêmeo Digital')
    text = text.replace('PINN', 'Gêmeo Digital')
    return text

master_items = []
for r in data_rows:
    pn = unformula(r[3])
    step_raw = unformula(r[8])
    dwg_raw = unformula(r[9])
    
    resolved_dwg = find_pdf(pn, dwg_raw)
    resolved_step = find_step(pn, step_raw)
    
    feito = r[2]
    if feito == 'SIM' and not resolved_step and 'Integrado' not in step_raw:
        resolved_step = step_raw if step_raw else 'Modelado (.stp pronto)'
    elif feito == 'NÃO' and not resolved_step:
        resolved_step = 'A Modelar / Faltante'
        
    master_items.append({
        'grupo': r[0],
        'prioridade': r[1],
        'feito': feito,
        'pn': pn,
        'nome': r[4],
        'tipo': r[5],
        'status_cad': r[6],
        'papel_ansys': r[7],
        'step': resolved_step,
        'dwg': resolved_dwg,
        'papel_fisico': sanitize_text(r[10]),
        'ref_doc': r[11]
    })

def get_abs_path(rel_val):
    if not rel_val or 'A Modelar' in rel_val or 'Faltante' in rel_val or 'Integrado' in rel_val or rel_val == '---':
        return None
    norm = rel_val.replace('/', '\\')
    full = os.path.join(root, norm) if not norm.startswith('D:\\') else norm
    if os.path.exists(full):
        return full
    return None

# 1. Export CSV
csv_out_rows = [headers]
for it in master_items:
    pn = it['pn']
    dwg = it['dwg']
    step = it['step']
    abs_dwg = get_abs_path(dwg)
    abs_step = get_abs_path(step)
    
    part_no_cell = f'=HYPERLINK("{abs_dwg}", "{pn}")' if abs_dwg else pn
    step_cell = f'=HYPERLINK("{abs_step}", "{os.path.basename(abs_step)}")' if abs_step else step
    dwg_cell = f'=HYPERLINK("{abs_dwg}", "{os.path.basename(abs_dwg)}")' if abs_dwg else dwg
    
    csv_out_rows.append([
        it['grupo'], it['prioridade'], it['feito'], part_no_cell,
        it['nome'], it['tipo'], it['status_cad'], it['papel_ansys'],
        step_cell, dwg_cell, it['papel_fisico'], it['ref_doc']
    ])

with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerows(csv_out_rows)

print(f"Exported clean CSV: {csv_path}")

# 2. Export Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Peças NASA s-Flame"

font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
fill_header = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
font_body = Font(name="Calibri", size=10)
font_link = Font(name="Calibri", size=10, color="0000FF", underline="single")
font_bold = Font(name="Calibri", size=10, bold=True)

fill_sim = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
font_sim = Font(name="Calibri", size=10, bold=True, color="006100")
fill_nao = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
font_nao = Font(name="Calibri", size=10, bold=True, color="9C0006")

thin_border = Side(border_style="thin", color="D9D9D9")
border_cell = Border(left=thin_border, right=thin_border, top=thin_border, bottom=thin_border)

ws.append(headers)
for col_num in range(1, len(headers) + 1):
    c = ws.cell(row=1, column=col_num)
    c.font = font_header
    c.fill = fill_header
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

for row_idx, it in enumerate(master_items, start=2):
    pn = it['pn']
    dwg = it['dwg']
    step = it['step']
    abs_dwg = get_abs_path(dwg)
    abs_step = get_abs_path(step)
    
    row_data = [
        it['grupo'], it['prioridade'], it['feito'], pn,
        it['nome'], it['tipo'], it['status_cad'], it['papel_ansys'],
        os.path.basename(abs_step) if abs_step else step,
        os.path.basename(abs_dwg) if abs_dwg else dwg,
        it['papel_fisico'], it['ref_doc']
    ]
    ws.append(row_data)
    
    for col_idx in range(1, len(row_data) + 1):
        c = ws.cell(row=row_idx, column=col_idx)
        c.font = font_body
        c.border = border_cell
        c.alignment = Alignment(vertical="center")
        
    c_feito = ws.cell(row=row_idx, column=3)
    c_feito.alignment = Alignment(horizontal="center", vertical="center")
    if it['feito'] == "SIM":
        c_feito.fill = fill_sim
        c_feito.font = font_sim
    else:
        c_feito.fill = fill_nao
        c_feito.font = font_nao
        
    c_pn = ws.cell(row=row_idx, column=4)
    if abs_dwg:
        c_pn.hyperlink = abs_dwg
        c_pn.font = font_link
        c_pn.alignment = Alignment(horizontal="center", vertical="center")
    else:
        c_pn.font = font_bold
        c_pn.alignment = Alignment(horizontal="center", vertical="center")
        
    c_step = ws.cell(row=row_idx, column=9)
    if abs_step:
        c_step.hyperlink = abs_step
        c_step.font = font_link
    elif "A Modelar" in step:
        c_step.font = Font(name="Calibri", size=9, italic=True, color="808080")
        
    c_dwg = ws.cell(row=row_idx, column=10)
    if abs_dwg:
        c_dwg.hyperlink = abs_dwg
        c_dwg.font = font_link

ws.freeze_panes = "A2"
ws.auto_filter.ref = ws.dimensions

col_widths = {
    1: 25, 2: 30, 3: 14, 4: 18, 5: 38, 6: 25,
    7: 22, 8: 35, 9: 25, 10: 25, 11: 55, 12: 35
}

for col_num, width in col_widths.items():
    col_letter = get_column_letter(col_num)
    ws.column_dimensions[col_letter].width = width

wb.save(xlsx_path)
print(f"Exported clean Excel: {xlsx_path}")

# 3. Export HTML
total_count = len(master_items)
done_count = sum(1 for it in master_items if it['feito'] == 'SIM')
missing_count = total_count - done_count
pct_done = round(done_count / total_count * 100, 1)

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NASA ACME — Catálogo de Engenharia Reversa 3D & Hardware de Voo</title>
    <style>
        :root {{
            --bg: #090d16;
            --surface: #131b2e;
            --surface-hover: #1c2742;
            --border: #24324f;
            --text: #f1f5f9;
            --muted: #94a3b8;
            --primary: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.2);
            --p1-bg: rgba(239, 68, 68, 0.2);
            --p1-text: #f87171;
            --p2-bg: rgba(249, 115, 22, 0.2);
            --p2-text: #fb923c;
            --p3-bg: rgba(234, 179, 8, 0.2);
            --p3-text: #facc15;
            --p4-bg: rgba(148, 163, 184, 0.15);
            --p4-text: #cbd5e1;
            --sim-bg: rgba(34, 197, 94, 0.2);
            --sim-text: #4ade80;
            --nao-bg: rgba(239, 68, 68, 0.2);
            --nao-text: #f87171;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 24px 32px;
        }}
        header {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
        }}
        h1 {{
            margin: 0;
            font-size: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
            letter-spacing: -0.02em;
        }}
        .badge {{
            font-size: 13px;
            padding: 4px 12px;
            border-radius: 999px;
            background: #0369a1;
            color: white;
            font-weight: 600;
        }}
        .summary-cards {{
            display: flex;
            gap: 16px;
        }}
        .stat-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 18px;
            text-align: center;
        }}
        .stat-val {{
            font-size: 20px;
            font-weight: bold;
            color: #fff;
        }}
        .stat-lbl {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--muted);
            margin-top: 2px;
        }}
        .controls {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
            background: var(--surface);
            padding: 18px;
            border-radius: 10px;
            border: 1px solid var(--border);
        }}
        .search-bar {{
            display: flex;
            gap: 12px;
        }}
        input[type="text"] {{
            flex: 1;
            padding: 10px 16px;
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: #fff;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }}
        input[type="text"]:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 0 2px var(--primary-glow);
        }}
        .filter-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }}
        .filter-label {{
            font-size: 12px;
            font-weight: 600;
            color: var(--muted);
            text-transform: uppercase;
            margin-right: 4px;
        }}
        .btn {{
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.04);
            color: var(--text);
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.15s;
        }}
        .btn:hover {{
            background: var(--surface-hover);
            border-color: #3b4e77;
        }}
        .btn.active {{
            background: var(--primary);
            color: #0f172a;
            border-color: var(--primary);
            font-weight: 700;
        }}
        .table-wrap {{
            overflow-x: auto;
            background: var(--surface);
            border-radius: 10px;
            border: 1px solid var(--border);
            max-height: calc(100vh - 320px);
            position: relative;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            text-align: left;
        }}
        th {{
            background: #090d16;
            color: #e2e8f0;
            font-weight: 600;
            padding: 12px 14px;
            border-bottom: 2px solid var(--border);
            white-space: nowrap;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        td {{
            padding: 10px 14px;
            border-bottom: 1px solid var(--border);
            vertical-align: middle;
        }}
        tr:hover td {{
            background: rgba(255, 255, 255, 0.03);
        }}
        .tag-sim {{
            background: var(--sim-bg);
            color: var(--sim-text);
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: bold;
            display: inline-block;
            text-align: center;
        }}
        .tag-nao {{
            background: var(--nao-bg);
            color: var(--nao-text);
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: bold;
            display: inline-block;
            text-align: center;
        }}
        .tag-prio {{
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 11px;
            display: inline-block;
            white-space: nowrap;
        }}
        .prio-p1 {{ background: var(--p1-bg); color: var(--p1-text); }}
        .prio-p2 {{ background: var(--p2-bg); color: var(--p2-text); }}
        .prio-p3 {{ background: var(--p3-bg); color: var(--p3-text); }}
        .prio-p4 {{ background: var(--p4-bg); color: var(--p4-text); }}
        .prio-ref {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; }}
        .tag-role {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 11px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        a.link-file {{
            color: #38bdf8;
            text-decoration: none;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}
        a.link-file:hover {{
            text-decoration: underline;
            color: #7dd3fc;
        }}
        .text-muted {{ color: var(--muted); }}
    </style>
</head>
<body>
    <header>
        <div>
            <h1>NASA ACME s-Flame <span class="badge">Engenharia Reversa & Modelagem CAD 3D</span></h1>
            <div style="color: var(--muted); font-size: 13px; margin-top: 4px;">
                Mapeamento Completo de Peças, Desenhos Técnicos (.PDF), Modelos Paramétricos STEP e Síntese Híbrida (Automação API + Refinamento Humano)
            </div>
        </div>
        <div class="summary-cards">
            <div class="stat-card">
                <div class="stat-val">{total_count}</div>
                <div class="stat-lbl">Total Peças</div>
            </div>
            <div class="stat-card">
                <div class="stat-val" style="color: #4ade80;">{done_count}</div>
                <div class="stat-lbl">Prontas (SIM)</div>
            </div>
            <div class="stat-card">
                <div class="stat-val" style="color: #f87171;">{missing_count}</div>
                <div class="stat-lbl">A Modelar</div>
            </div>
            <div class="stat-card">
                <div class="stat-val" style="color: #38bdf8;">{pct_done}%</div>
                <div class="stat-lbl">Concluído</div>
            </div>
        </div>
    </header>

    <div class="controls">
        <div class="search-bar">
            <input type="text" id="searchInput" placeholder="Pesquisar por Part Number, Nome, Grupo, Prioridade ou Descrição..." onkeyup="filterTable()">
        </div>
        <div class="filter-group">
            <span class="filter-label">Status:</span>
            <button class="btn active" onclick="setStatusFilter('ALL', this)">Todos ({total_count})</button>
            <button class="btn" onclick="setStatusFilter('SIM', this)">Prontos / Concluídos ({done_count})</button>
            <button class="btn" onclick="setStatusFilter('NÃO', this)">Faltantes / A Modelar ({missing_count})</button>
        </div>
        <div class="filter-group">
            <span class="filter-label">Prioridade:</span>
            <button class="btn active" onclick="setPriorityFilter('ALL', this)">Todas</button>
            <button class="btn" onclick="setPriorityFilter('P1', this)">P1 — Crítica</button>
            <button class="btn" onclick="setPriorityFilter('P2', this)">P2 — Alta</button>
            <button class="btn" onclick="setPriorityFilter('P3', this)">P3 — Média</button>
            <button class="btn" onclick="setPriorityFilter('P4', this)">P4 — Baixa / Referência</button>
            <button class="btn" onclick="setPriorityFilter('Referência', this)">Referência</button>
        </div>
    </div>

    <div class="table-wrap">
        <table id="dataTable">
            <thead>
                <tr>
                    <th>Grupo / Subsistema</th>
                    <th>Prioridade</th>
                    <th>Feito?</th>
                    <th>Part Number</th>
                    <th>Nome Oficial (Inglês NASA)</th>
                    <th>Tipo</th>
                    <th>Papel Físico & Montagem</th>
                    <th>Status no CAD</th>
                    <th>Arquivo STEP</th>
                    <th>Desenho Técnico (.PDF)</th>
                    <th>Descrição Técnica & GD&T</th>
                </tr>
            </thead>
            <tbody>
"""

for it in master_items:
    pn = it['pn']
    prio = it['prioridade']
    feito = it['feito']
    dwg = it['dwg']
    step = it['step']
    abs_dwg = get_abs_path(dwg)
    abs_step = get_abs_path(step)
    
    if 'P1' in prio:
        prio_cls = 'prio-p1'
    elif 'P2' in prio:
        prio_cls = 'prio-p2'
    elif 'P3' in prio:
        prio_cls = 'prio-p3'
    elif 'P4' in prio:
        prio_cls = 'prio-p4'
    else:
        prio_cls = 'prio-ref'
        
    tag_feito = f'<span class="tag-sim">SIM</span>' if feito == 'SIM' else f'<span class="tag-nao">NÃO</span>'
    
    if abs_dwg:
        dwg_fwd = abs_dwg.replace('\\', '/')
        file_url = f"file:///{dwg_fwd}"
        pn_html = f'<a class="link-file" href="{file_url}" target="_blank" title="Abrir Desenho Técnico">{pn} ↗</a>'
    else:
        pn_html = f'<strong>{pn}</strong>'
        
    if abs_step:
        step_fwd = abs_step.replace('\\', '/')
        step_url = f"file:///{step_fwd}"
        step_html = f'<a class="link-file" href="{step_url}" target="_blank" title="Abrir Modelo 3D STEP">📦 {os.path.basename(abs_step)}</a>'
    elif 'Integrado' in step:
        step_html = f'<span class="text-muted" style="font-size: 11px;">🔗 {step}</span>'
    else:
        step_html = f'<span class="text-muted" style="font-style: italic;">{step}</span>'
        
    if abs_dwg:
        dwg_fwd = abs_dwg.replace('\\', '/')
        dwg_url = f"file:///{dwg_fwd}"
        dwg_html = f'<a class="link-file" href="{dwg_url}" target="_blank" title="Abrir Desenho Técnico">📄 {os.path.basename(abs_dwg)}</a>'
    else:
        dwg_html = f'<span class="text-muted">{dwg}</span>'
        
    html_content += f"""                <tr data-feito="{feito}" data-prio="{prio}">
                    <td><strong>{it['grupo']}</strong></td>
                    <td><span class="tag-prio {prio_cls}">{prio}</span></td>
                    <td style="text-align: center;">{tag_feito}</td>
                    <td>{pn_html}</td>
                    <td>{it['nome']}</td>
                    <td><span class="text-muted">{it['tipo']}</span></td>
                    <td><span class="tag-role">{it['papel_ansys']}</span></td>
                    <td>{it['status_cad']}</td>
                    <td>{step_html}</td>
                    <td>{dwg_html}</td>
                    <td style="min-width: 280px; max-width: 450px;">{it['papel_fisico']}</td>
                </tr>
"""

html_content += """            </tbody>
        </table>
    </div>

    <script>
        let currentStatusFilter = 'ALL';
        let currentPriorityFilter = 'ALL';

        function setStatusFilter(val, btn) {
            currentStatusFilter = val;
            btn.parentElement.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterTable();
        }

        function setPriorityFilter(val, btn) {
            currentPriorityFilter = val;
            btn.parentElement.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterTable();
        }

        function filterTable() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const rows = document.querySelectorAll('#dataTable tbody tr');

            rows.forEach(r => {
                const text = r.innerText.toLowerCase();
                const feito = r.getAttribute('data-feito');
                const prio = r.getAttribute('data-prio');

                let matchSearch = text.includes(query);
                let matchStatus = (currentStatusFilter === 'ALL') || (feito === currentStatusFilter);
                let matchPriority = (currentPriorityFilter === 'ALL') || prio.includes(currentPriorityFilter);

                if (matchSearch && matchStatus && matchPriority) {
                    r.style.display = '';
                } else {
                    r.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Exported clean HTML: {html_path}")
