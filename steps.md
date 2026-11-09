# NASA ACME s-Flame — Roteiro de Engenharia Reversa e Modelagem CAD 3D

Este documento estabelece o plano técnico e as fases de execução para a reconstrução tridimensional paramétrica e engenharia reversa do hardware de voo da missão **NASA ACME s-Flame (Combustion Integrated Rack — ISS)**.

---

## Fase 1: Auditoria Técnica e Catalogação Dimensional (124 Componentes)
* Mapeamento completo dos desenhos oficiais da NASA (ACME Engineering 20210328, Seção 5, págs. 75–88).
* Classificação em 8 subsistemas principais:
  1. *Burner Subsystem* (Queimador Esférico e Base S1101MFA1200)
  2. *Igniter Subsystem* (Mecanismo Articulado e Ponta Kanthal S1101MFA1300)
  3. *Thermometry Subsystem* (Pente Far Rake S1101MFA1609 e Termopares 200mm)
  4. *Radiometry Subsystem* (Aberturas e Radiômetros S1101MFA1520/1526)
  5. *Optical & Camera Diagnostics* (Câmeras Internas e Filtros S1101MFA2300)
  6. *Gas Supply & Manifolds* (Manifolds de Entrada e Chaveamento S1101MFA1100/1104)
  7. *Chamber Vessel & Insert* (Vaso CIR de 83L e Insert S1101MFA0003)
  8. *EMS Structural Cage* (Estrutura de Montagem S1101MFA1000)
* Geração do checklist dinâmico: `pecas_faltantes.html`, `pecas_faltantes.xlsx` e `pecas_faltantes.csv`.

---

## Fase 2: Modelagem Paramétrica do Queimador e Base (S1101MFA1200)
* Modelagem da esfera porosa de bronze sinterizado de $\varnothing 6,25\text{ mm}$ ($1/4"$).
* Tubo de suporte capilar de parede justa $OD=1,80\text{ mm}$ (`S1101MFD1270`, desvio oficial ACME-DEV-031) e colar `S1101MFD1210`.
* Termopar embutido $TC_{\text{Burner}}$ (`S1101EFA1215`) inserido $0,76\text{--}1,0\text{ mm}$ no hemisfério sul da matriz condutiva.
* Conjunto da base isolante `S1101MFA1200`:
  * Placa base estrutural `S1101MFD1201`
  * Par de lâminas isolantes de fluorocarbono de $0,010"$ cada ($0,020" = 0,508\text{ mm}$ total, `S1101MFD1202`) com rasgo oblongo
  * Placa inferior de compressão `S1101MFD1203` e buchas de centragem `MFD1204/1205/1206`
  * Vedações O-ring `AS3209-013` e parafusos modificados `S1101MFP1025`
  * Capa do rasgo da base `S1101MFD1269`.

---

## Fase 3: Engenharia Reversa do Mecanismo do Ignitor (S1101MFA1300)
* Resolução da cinemática de 4 barras do atuador rotativo:
  * Posição estendida / preheat: $+39,11^\circ$ (ponta Kanthal a $1,25\text{ mm}$ do ápice da esfera)
  * Posição retraída / standby: $-26,38^\circ$
  * Curso angular total: $65,49^\circ$
* Modelagem das peças móveis:
  * Corpo atuador `S1101MFA1301` e base de montagem `S1101MFA1303`
  * Braço articulado `S1101MFA1308` e biela `S1101MFD1305`
  * Ponta de ignição com filamento em alça `S1101MFA1319` (fio Kanthal A-1 $\varnothing 0,25\text{ mm}$)
  * Isolador cerâmico cilíndrico `S1101MFD1320` ($\varnothing 4,75\text{ mm}$ com 2 furos $\varnothing 0,5\text{ mm}$ a $2,0\text{ mm}$)
  * Suporte terminal bipartido em cobre-berílio `S1101MFD1333/1334` e capas `MFA1336/1338`.
* Validação de não-interferência espacial contra a gaiola EMS via `scripts/verify_kinematics.py`.

---

## Fase 4: Instrumentação de Campo (Far Rake & Radiometria)
* **Pente Far Array (`S1101MFA1609`):**
  * O único pente de termopares instalado em voo no s-Flame.
  * 4 estações de medição com tubos de alumina: $r = 45\text{ mm}$ (`MFD1619`), $60\text{ mm}$ (`MFD1620`), $100\text{ mm}$ (`MFD1621`) e $100\text{ mm}$ ortogonal.
  * Braço estrutural `S1101MFA1612`, suporte vertical `MFA1613` e chicote Micro-D `EFA1611`.
* **Termopares de Campo Distante a 200 mm:**
  * Sensor do lado do ignitor (`S1101MFA1623` - TC200A)
  * Sensor do lado do relé com ponta dobrada em $30^\circ$ (`S1101MFA1627` - TC200B)
  * Suportes e capas angulares `MFA1624/1628/1640`.
* **Radiômetros de Banda Larga:**
  * Radiômetro axial padrão (`S1101MFA1520`) e radiômetro offset a $60^\circ$ (`S1101MFA1526`)
  * Placas de abertura sem lente `S1101MFD1523` ($138,5\text{ mm}$ e $205,4\text{ mm}$) para ray-tracing de penumbra óptica.
* **Tampas de Janelas Ópticas (`Window Blanks`):**
  * `UML1, UML2, UML4/8, UML5` fosfatadas/anodizadas pretas para eliminar reflexão secundária (ACME-WAI-048).

---

## Fase 5: Estrutura EMS e Vaso CIR (83 Litros)
* Reconstrução da carcaça do Vaso CIR (`CIR-CHAMBER-83L`) para definição do volume de confinamento isocórico.
* Montagem geral do insert `S1101MFA0003` alojado na câmara.
* Gaiola estrutural EMS (`S1101MFA1000`): placas superior e inferior `1001/1003`, colunas tubulares `1008` e tirantes diagonais `1014`.

---

## Fase 6: Automação Paramétrica vs. Modelagem Manual de Alta Complexidade
* **Automação Procedural (Python + Autodesk Inventor API):**
  * Execução via `scripts/inventor_cad_automation.py` para geração rápida de corpos axisimétricos, flanges concêntricas e exportação em lote AP214 STEP.
* **Refinamento Manual Especializado (Emerson B. J.):**
  * Resolução de peças aeroespaciais com Datums compostos (A, B e C), paredes ultra-finas ($0,016"$), telas perfuradas e interfaces com restrição cinemática estrita.

---

## Entregas e Artefatos do Repositório
* Modelos 3D nativos Inventor (`.ipt` / `.iam`) e universais STEP AP214 (`.stp`).
* Desenhos técnicos originais da NASA em alta resolução (`.pdf`).
* Catálogo interativo de peças com hiperlinks: [`pecas_faltantes.html`](pecas_faltantes.html).
* Planilha de controle técnico de engenharia: [`pecas_faltantes.xlsx`](pecas_faltantes.xlsx).
* Gráfico de inventário de componentes em 300 DPI: [`assets/distribuicao_pecas_cad.png`](assets/distribuicao_pecas_cad.png).
