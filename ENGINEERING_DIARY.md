# DIÁRIO TÉCNICO DE ENGENHARIA REVERSA & MODELAGEM CAD 3D
## Hardware de Voo NASA ACME s-Flame (Combustion Integrated Rack — ISS)

---

### Visão Geral do Projeto
Este diário documenta o processo sistemático de engenharia reversa, análise de tolerâncias geométricas (GD&T), cinemática de mecanismos e síntese paramétrica tridimensional das peças e montagens do experimento **NASA ACME s-Flame**, executado em microgravidade na Estação Espacial Internacional (ISS).

O trabalho foi desenvolvido combinando **automação paramétrica via scripts Python integrados à API COM do Autodesk Inventor** e **modelagem manual especializada conduzida pelo Engenheiro Mecânico Aeroespacial Emerson B. J.**

---

### 1. Auditoria e Estruturação de 124 Componentes

A reconstrução do modelo digital exigiu cruzar 342 desenhos técnicos originais da NASA (`ACME_engineering_20210328.pdf`), waivers formais e modelos brutos de entrada:
1. **Queimador Esférico e Base (`S1101MFA1200`):** 25 componentes e submontagens.
2. **Atuador do Ignitor e Braço Articulado (`S1101MFA1300`):** 19 componentes e montagens cinemáticas.
3. **Pentes de Termopares e Campo Distante (`S1101MFA1609`):** 30 componentes de termometria de precisão.
4. **Radiômetros de Banda Larga e Tampas Ópticas (`S1101MFA1520/1526`):** 8 componentes.
5. **Câmeras Internas, Lentes e Roda de Filtros (`S1101MFA1400/2300`):** 21 componentes.
6. **Manifolds de Suprimento de Gás (`S1101MFA1100/1104`):** 6 blocos usinados.
7. **Vaso CIR (83L) e Queimador BRE (`CIR-CHAMBER-83L`):** 7 componentes de contorno.
8. **Gaiola Estrutural EMS (`S1101MFA1000`):** 8 componentes estruturais principais.

---

### 2. Engenharia Reversa do Queimador Esférico (S1101MFA1200 / S1101MFA1216)

#### 2.1 Desvio Dimensional Crítico: ACME-DEV-031
* **Problema Identificado nos Desenhos:** O desenho conceitual indicava tubo de suporte de $\varnothing 1/16"$ ($1,588\text{ mm}$). Porém, os relatórios de montagem do queimador de voo S/N 1003 e as fotografias da câmara revelaram o tubo real com $OD = 1,80\text{ mm}$ ($28,8\%$ do diâmetro da esfera $D_0 = 6,25\text{ mm}$).
* **Impacto Térmico:** Essa diferença geométrica governa o sumidouro condutivo de calor ($h_q = 48,7\text{ W/m}^2\text{K}$) e o gap reflexivo abaixo do polo sul da esfera (Fig. 46), gerando uma assimetria norte-sul de $+53,4\%$ na radiação de radicais $CH^*$.
* **Resolução CAD:** O modelo `S1101MFD1270` foi gerado exatamente com $OD = 1,80\text{ mm}$ e o colar `S1101MFD1210` foi ajustado para vedação de tolerância justa.

#### 2.2 Isolamento Térmico e Elétrico da Base
* **Correção da Peça `S1101MFD1202`:** A especificação inicial de isolador cerâmico maciço foi corrigida com base no desenho `s1101mfa1200_A.pdf`. A peça consiste em um par de lâminas isolantes finas de fluorocarbono de $0,010"$ cada ($0,020" = 0,508\text{ mm}$ no total), com rasgo oblongo central usinado para passagem dos dois anéis de vedação O-ring `AS3209-013`.
* **Fixadores Especiais:** Modelagem dos 4 parafusos de cabeça cilíndrica com sextavado interno modificados `S1101MFP1025` (rosca $.190\text{-}32\text{ UNRF-3A} \times .750"$), que se alojam dentro das buchas de centragem cerâmicas `S1101MFD1204/1205`.

---

### 3. Mecanismo Articulado do Ignitor (S1101MFA1300)

#### 3.1 Cinemática e Restrições de Montagem
O atuador rotativo do ignitor opera em um mecanismo articulado de 4 barras:
* **Posição Estendida (Preheat / Disparo):** Ângulo de $+39,11^\circ$ do braço `S1101MFA1308` em relação à horizontal. Nesta posição, o filamento Kanthal A-1 se posiciona a exatamente $1,25\text{ mm}$ acima da superfície porosa do polo norte da esfera.
* **Posição Retraída (Standby / Pós-Ignição):** Ângulo de $-26,38^\circ$ do braço e retração do êmbolo Haydon.
* **Curso Total:** $65,49^\circ$ de varredura angular, acionado em $0,60\text{ s}$ de retração (conforme waiver ACME-DEV-050).

#### 3.2 Otimização e Limpeza de Geometrias
* **Eliminação de Faces Fragmentadas:** Os modelos brutos importados continham centenas de faces facetadas redundantes resultantes de conversões mal calibradas.
* **Refinamento:** O modelo de montagem `s1101mfa1300.iam` e as peças individuais `s1101mfa1301.ipt`, `1303.ipt`, `1308.ipt` e `s1101mfd1305.ipt` foram reconstruídos como sólidos B-Rep perfeitos, eliminando todas as arestas espúrias e garantindo transições de tangência suaves.

---

### 4. Pente Far Rake (S1101MFA1609) e Termometria de Voo

#### 4.1 Identificação do Hardware Real de Voo
* A documentação de engenharia ACME descreve dois pentes: *Near Array* (`S1101MFA1605`) e *Far Array* (`S1101MFA1609`).
* **Auditoria de Voo:** A análise das telemetrias revelou que o pente *Near Array* **nunca foi instalado nas corridas do s-Flame** para evitar perturbação do campo de chama esférica (ACME Engineering p. 12).
* **Hardware de Voo Real:** Apenas o *Far Array* (`S1101MFA1609`) e os termopares de 200 mm (`S1101MFA1623` e `1627`) voaram.
* **Geometria dos Sensores:**
  * Estação 1: $r = 45\text{ mm}$ (Termopar Tipo B, luva de alumina `S1101MFD1619`)
  * Estação 2: $r = 60\text{ mm}$ (Termopar Tipo B, luva de alumina `S1101MFD1620`)
  * Estação 3: $r = 100\text{ mm}$ (Termopar Tipo B, luva de alumina `S1101MFD1621`)
  * Estação 4: $r = 100\text{ mm}$ ortogonal (Termopar Tipo K, luva de alumina `S1101MFD1621`)
  * Sensores de Campo Distante: $r = 200\text{ mm}$ no lado do ignitor (`1623`) e no lado do relé com ponta dobrada em $30^\circ$ (`1627`).

---

### 5. Metodologia Híbrida: Automação vs. Engenharia Humana

| Subsistema / Peça | Abordagem Primária | Justificativa Técnica |
| :--- | :---: | :--- |
| Tubos de Suporte e Flanges Cilíndricas | **Automação (Python + Inventor API)** | Geometrias axisimétricas padronizadas, perfis circulares concêntricos e extrusões diretas. |
| Parafusos e Elementos de Fixação | **Automação (Python + Inventor API)** | Aplicação de tabelas NAS/MS e furação paramétrica com roscas UNRF. |
| Manga com Rebaixo Assimétrico (`S1101MFD1237`) | **Manual Especializada (Emerson B. J.)** | Paredes de $0,016"$, rasgos de chaveta assimétricos e tolerâncias de posição estritas. |
| Tela Perfurada e Alinhador Alumina (`S1101MFD1238/1239`) | **Manual Especializada (Emerson B. J.)** | Matriz com centenas de canais microscópicos e furos passantes para sondas em tolerância mícron. |
| Conjunto da Base e Vedação O-ring (`S1101MFA1200`) | **Manual Especializada (Emerson B. J.)** | Sobreposição de tolerâncias de compressão dos O-rings e encaixe concêntrico das buchas isolantes. |
| Cinemática 4-Barras do Ignitor (`S1101MFA1300`) | **Manual Especializada (Emerson B. J.)** | Resolução precisa dos centros de rotação e batentes físicos do mecanismo no espaço restrito do insert. |

---

### 6. Ferramental Desenvolvido e Entregáveis

1. **`scripts/inventor_cad_automation.py`:** Módulo de automação em Python para Autodesk Inventor.
2. **`scripts/verify_kinematics.py`:** Rotina de verificação matemática da cinemática e folgas do ignitor.
3. **`scripts/generate_pecas_catalog.py`:** Gerador automatizado dos catálogos de peças.
4. **`pecas_faltantes.html`:** Dashboard interativo com busca em tempo real e links diretos para PDFs e STEPs.
5. **`pecas_faltantes.xlsx`:** Matriz Excel com 202 hiperlinks ativos e formatação condicional de status.
6. **`assets/distribuicao_pecas_cad.png`:** Infográfico em alta resolução (300 DPI) com o inventário completo.
