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


---

## [2026-11-09] Decisao de Arquitetura de Simulacao Multifisica: Substituicao de Suportes de Termometria Distante por Sondas Virtuais Pontuais (X, Y, Z no Ansys Fluent)

### 1. Racional da Fisica e Dinamica dos Fluidos em Microgravidade
Durante a estruturacao do dominio tridimensional do Gemeo Digital e da malha volumetrica no Ansys Fluent, foi estabelecida a substituicao das geometrias mecanicas complexas de sustentacao dos termopares distantes por **Sondas Virtuais Pontuais (Point Probes)** nas coordenadas espaciais exatas $(X, Y, Z)$ dos sensores.

1. **Escala Espacial e Regime Hidrodinamico**:
   * O raio visivel da chama esferica em microgravidade ($\mu\text{g} \approx 10^{-6}\,\text{g}$) e de $r_{\text{flame}} \approx 10\,\text{a}\,15\,\text{mm}$, centrada na origem $(0, 0, 0)$ da esfera porosa.
   * Os sensores termicos do pente Far Rake operam a raios $r \in [45, 60, 100]\,\text{mm}$, e os termopares de campo distante operam a $r = 200\,\text{mm}$.
   * Em microgravidade pura, na ausencia de empuxo termico natural ($\text{Gr} \to 0$), a conveccao a distancias $r > 30\,\text{mm}$ e desprezivel ($u \approx 0\,\text{m/s}$, numero de Peclet $\text{Pe} \ll 1$). O transporte de calor nessa regiao externa e governado puramente por conducao molecular e radiacao termica no gas confinador da camara CIR ($83\,\text{L}$).

2. **Evitacao de Singularidades de Malha e Economia Computacional**:
   * A inclusao dos corpos fisicos dos bracos mecanicos articulados (`S1101MFA1612`, `S1101MFD1614`), suportes de montagem (`S1101MFD1615`, `S1101MFA1624/1628/1640`), tubos ceramicos de alumina ($\varnothing 1{,}5\,\text{mm}$) e fios de termopar ($\varnothing 0{,}20\,\text{mm}$) introduziria arestas vivas, folgas submilimetricas e elevado *skewness* a centenas de milimetros da chama.
   * A discretizacao solida desses elementos forcaria o refinamento de prismas de camada limite em uma regiao com velocidade nula, inflando a contagem de celulas da malha em $2{,}5 \times 10^6$ a $4{,}0 \times 10^6$ elementos sem nenhum ganho na precisao da combustao.
   * A adocao de sondas pontuais virtuais desacopla a malha de fluidos dos suportes inertes, garantindo convergencia estavel do solver e acelerando o tempo de iteracao do Ansys Fluent.

---

### 2. Mapeamento das Sondas Virtuais Pontuais no Ansys Fluent
Em substituicao aos solidos CAD, foram mapeadas as 6 sondas virtuais pontuais com monitoramento termico continuo ($125\,\text{Hz}$):

| ID Sonda | Sensor de Voo | Subconjunto NASA | Raio Radial ($r$) | Tipo de Termopar | Papel no Gemeo Digital & Validacao |
|---|---|---|---|---|---|
| **P1** | **TCA** | `* S1101MFA1609` (Pos 1) | $45{,}0\,\text{mm}$ | Tipo B ($\varnothing 0{,}20\,\text{mm}$, gota $\ge 0{,}40\,\text{mm}$) | Ressuscitado analiticamente em $31{,}1^\circ\text{C}$ (ACME-DEV-026) |
| **P2** | **TCB** | `* S1101MFA1609` (Pos 2) | $60{,}0\,\text{mm}$ | Tipo B ($\varnothing 0{,}20\,\text{mm}$, gota $\ge 0{,}40\,\text{mm}$) | Ressuscitado analiticamente em $24{,}0^\circ\text{C}$ (ACME-DEV-026) |
| **P3** | **TCC** | `* S1101MFA1609` (Pos 3) | $100{,}0\,\text{mm}$ | Tipo B ($\varnothing 0{,}20\,\text{mm}$, gota $\ge 0{,}40\,\text{mm}$) | Temperatura do gas de campo intermediario |
| **P4** | **TCD** | `* S1101MFA1609` (Pos 4) | $100{,}0\,\text{mm}$ | Tipo K ($\varnothing 0{,}25\,\text{mm}$, gota $\ge 0{,}50\,\text{mm}$) | **Holdout Cego de Validacao** ($\text{RMSE} = 0{,}12\,\text{K}$) |
| **P5** | **TC200A** | `* S1101MFA1623` | $200{,}0\,\text{mm}$ | Tipo K (Igniter Side) | Temperatura de contorno distante (lado do ignitor) |
| **P6** | **TC200B** | `* S1101MFA1627` | $200{,}0\,\text{mm}$ | Tipo K (Relay Side) | Ponta de $5\,\text{mm}$ dobrada em $30^\circ$ (Fig. 66) |

*Equacao de Acoplamento Termico da Gota (Pos-Processamento 0D)*:
A temperatura real medida pela juncao esferica ($T_b$) e reconstruida a partir da temperatura do gas ($T_g$) obtida na sonda virtual via balanco transiente de energia:
$$\rho_b c_{p,b} V_b \frac{dT_b}{dt} = h_b A_b (T_g - T_b) - \epsilon_b \sigma A_b \left(T_b^4 - T_{\text{wall}}^4\right)$$

---

### 3. Inventario de Componentes Marcados com Asterisco `*` (Dispensados de CAD)
Total de **18 componentes/montagens** marcados oficialmente com `*` na planilha `pecas_faltantes.xlsx`:

1. `* S1101MFA1609` — Thermocouple Far Array Assembly
2. `* S1101MFA1610` — Thermocouple Far Rake Assembly
3. `* S1101MFA1612` — TC Far Mounting Arm Assembly
4. `* S1101MFD1619` — Far TC Sleeve, Pos 1 (45mm)
5. `* S1101MFD1620` — Far TC Sleeve, Pos 2 (60mm)
6. `* S1101MFD1621` — Far TC Sleeve, Pos 3 & 4 (100mm)
7. `* S1101MFA1623` — 200mm Thermocouple Assembly (Igniter Side)
8. `* S1101MFA1627` — 200mm Thermocouple Assembly (Relay Side)
9. `* S1101MFD1625` — 200mm TC Ceramic Sleeve (Igniter Side)
10. `* S1101MFD1626` — 200mm TC Ceramic Sleeve (Relay Side)
11. `* S1101MFA1624` — 200mm TC Igniter Side Mounting Bracket
12. `* S1101MFA1628` — 200mm TC Relay Side Mounting Bracket
13. `* S1101MFA1640` — 200mm TC Cover Assembly
14. `* S1101EFA1611` — TC Far Rake Harness Assembly
15. `* S1101MFD1614` — TC Rake Arm
16. `* S1101MFD1615` — TC Rake Arm Bracket
17. `* S1101MFD1629` — 200mm TC Arm
18. `* S1101MFD1630` — 200mm TC Arm Base Bracket

---

### 4. Demarcacao Rigorosa dos Componentes com CAD Obrigatorio (`PRECISA FAZER`)
Para evitar qualquer simplificacao indevida na fisica de combustao, permanecem como **CAD Obrigatorio (Fila Prioritaria de Modelagem)**:
1. **`S1101EFA1215` (Termopar Embutido `TCBurner`)**: Fica cravado a $0{,}76 - 1{,}0\,\text{mm}$ na matriz de bronze poroso. Faz parte da conducao interna do queimador e fornece a condicao de contorno de temperatura da casca ($T_s$). **NAO PODE ser virtual**.
2. **`S1101MFD1270` e `S1101MFD1210` (Suporte de $1/4"$ e Colar)**: Causa perda condutiva de $h_q = 48{,}7\,\text{W/m}^2\text{K}$ no polo sul e assimetria dipolar (+53,4% em INTNS $\text{CH}^*$). Geometria solida indispensavel.
3. **`S1101MFD1269` (Burner Stem Cover)**: Veda o rasgo inferior da base e evita vortices espurios de recirculacao sob a chama.
4. **`S1101MFA1319` / `1339` e `S1101MFD1320` (Ponta do Ignitor e Isolador Ceramico)**: Penetra a zona de reacao durante o ciclo de ignicao e causa perturbacao hidrodinamica durante o atraso de retracao de $0{,}6\,\text{s}$ (ACME-DEV-050).
5. **`S1101MFD1523` (Abertura Optica do Radiometro)**: Define os angulos de visao FOV ($120{,}4\,\text{mm}$ e $120{,}2\,\text{mm}$) no ray-tracing de radiacao.
6. **`UML1/2/4/5` (Tampas de Janela Nao Reflexivas)**: Definem a emissividade radiativa das paredes da camara (ACME-WAI-048).
7. **`CIR-CHAMBER-83L` (Vaso de Pressao de 83L)**: Fecha a compressao isocorica em queimas de longa duracao ($> 40\,\text{s}$).


---

## 5. Atualizacao de Modelos CAD Inspecionados e Aprovados (10/11/2026)

Inspecao tecnica rigorosa dos arquivos STEP exportados/baixados na raiz de Downloads, validando integridade topologica (manifold solid brep / closed shell), dimensional e aderencia aos desenhos oficiais da NASA GRC / ZIN Technologies:

### 1. Modelos Aprovados e Armazenados nos Repositorios Oficiais
1. **`S1101MFA1216_E.step` (Queimador Esferico de Voo de 1/4" - 6,35 mm)**:
   - **Localizacao Oficial:** `CADs_Nosso/Burner/Montagens/S1101MFA1216_E.step`
   - **Validacao Dimensional:** Raio da esfera porosa R = 3.175 mm (Diametro 6.35 mm = 1/4"). Centro da esfera fixado com precisao em Z = 177.80 mm (7.0"), perfeitamente alinhado com o eixo optico da camara CIR. Topo da esfera em Z = 180.97 mm.
   - **Componentes Integrados:** Placa base `S1101MFD1201`, haste de suporte `S1101MFD1270` (OD = 1.83 mm), colar de retencao `S1101MFD1210` e sonda de termopar `92420308-705` a 55 graus.
   - **Status na Planilha:** Atualizado de `PRECISA FAZER` para **`JÁ MODELADO`**.

2. **`s1101efa1215_FULL.stp` (Burner Harness Assembly - Chicote Eletrico)**:
   - **Localizacao Oficial:** `CADs_Nosso/Burner/Serie_1100_a_1109/s1101efa1215_FULL.stp`
   - **Validacao Dimensional:** Comprimento total X = 244.47 mm (aderente a 9.5 +/- 0.5" do desenho NASA `S1101EFA1215`). Inclui o plugue Glenair circular e conectores olhais de aterramento.
   - **Status na Planilha:** Atualizado para **`JÁ MODELADO`**.

3. **`s1101mfa1339_ponteira_ignitor.stp` (Igniter Tip Assembly - Coiled)**:
   - **Localizacao Oficial:** `CADs_Nosso/Igniter/Pecas/s1101mfa1339_ponteira_ignitor.stp`
   - **Validacao:** Ponta do atuador de ignicao com filamento de aquecimento em espiral (Coil), correspondente a montagem `S1101MFA1339`.
   - **Status na Planilha:** Atualizado para **`JÁ MODELADO`**.

4. **`S1101MFD1320.stp` (Igniter Tip Insulator)**:
   - **Localizacao Oficial:** `CADs_Nosso/Igniter/Pecas/S1101MFD1320.stp`
   - **Validacao:** Isolador ceramico cilindrico usinado em alumina (4.75 x 13.46 mm).

5. **`S1101MFA1606.stp` (Near Rake Thermocouple Assembly)**:
   - **Localizacao Oficial:** `CADs_Nosso/Thermocouples/Montagens/S1101MFA1606.stp`
   - **Validacao:** Suporte arqueado de termopares proximos (188.13 x 136.08 x 7.53 mm) reconstruido 1:1 com base no desenho `S1101MFA1606`.

6. **`s1101mfa1609_1609_OPER.stp` (Far Rake Array Assembly)**:
   - **Localizacao Oficial:** `CADs_Nosso/Thermocouples/Montagens/s1101mfa1609_1609_OPER.stp`
   - **Nota de Engenharia:** Embora no Ansys Fluent os termopares distantes sejam tratados como sondas virtuais pontuais (X,Y,Z), o modelo CAD foi aprovado e arquivado para rastreabilidade de interferencia estrutural.

7. **Conjunto Optico de Janelas e Tampas Nao-Reflexivas da Camara CIR (Waiver ACME-WAI-048)**:
   - **Localizacao Oficial:** `CADs_Nosso/CIR_Chamber/`
   - **Arquivos:** `cir_anel_8_janelas_e_tampas_ansys.stp`, `cir_window_cover_SFLAME.stp`, `cir_window_cover_FIG56.stp`, `cir_window_cover_FIG57.stp`, `cir_window_cover_SINGLE.stp`, `uml_window_cover_individual.stp`.
   - **Finalidade:** Definicao exata dos contornos de radiacao no modelo DO (Discrete Ordinates) do Ansys Fluent com absortividade alpha = 0.92 nas posicoes UML1, UML2 e UML5.

### 2. Arquivos Mantidos na Pasta Downloads (Pendentes / Duplicatas)
- **`S1101MFA1216_E (1).step`**: Versao intermediaria onde o topo da esfera ficou em Z = 182.56 mm (heranca da cota de 3/8"). Mantido em Downloads sem migracao para evitar sobrescrever a versao final correta (`S1101MFA1216_E.step` com Z_max = 180.97 mm).
- **`S1101EFA1215_B.step`**: Contem apenas o solido da plaqueta de identificacao (label de 4.5 x 6.8 mm), sendo substituido com sucesso pelo arquivo completo `s1101efa1215_FULL.stp`.
