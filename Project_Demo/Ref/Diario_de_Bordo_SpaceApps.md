# 📓 Diário de Bordo: NASA Space Apps - ACME s-Flame

**Data/Hora Inicial:** 29/09/2026 - 16:30 
**Missão:** Projeto Flame in Freefall - Previsão Termodinâmica de Chamas em Microgravidade

## 📅 Entrada 1: Limpeza da Estação de Trabalho
O repositório local do computador estava caótico com dezenas de ZIPs gigantescos e metadados irrelevantes do repositório PSI-23. Foi executada uma "higienização" de pastas com scripts automatizados. 
* Todos os arquivos soltos com sufixos (1), (2) (duplicatas de download do navegador) foram expurgados.
* A raiz de trabalho foi consolidada em pastas estanques: CAD_References, Data_Processing, Dataset e Metadata.
* Criamos a documentação oficial (ACME_sFlame_Project_Resources.md) padronizando o linguajar para o painel de juízes.

## 📅 Entrada 2: A Tabela Experimental e a Triagem de Combustíveis
Fizemos a leitura e o parse do arquivo mestre PSI-23_Experimental table_ACME s-Flame.csv. Descobrimos o cronograma exato de 18 dias de testes na ISS, totalizando 276 ignições bem-sucedidas.
Escolhemos cirurgicamente as 3 rodadas que servirão de base (Condições de Contorno / Boundary Conditions) para alimentar o **Ansys Fluent**:
1. **19304:** A Linha de Base (45% $) - Queima limpa. Condições de contorno perfeitas para calibrar o modelo CFD contra a física terrestre padrão.
2. **19352:** A Instabilidade Pura (100% $) - Chama pulsante e caótica (baixo número de Lewis). O desafio máximo para a Inteligência Artificial prever.
3. **20176:** O Estresse Radiativo (30% $) - Fuligem extrema (sooty flame). Como a fumaça não sobe no espaço, a radiação térmica domina toda a transferência de calor na câmara.

*Ação Tomada:* O diretório gigantesco Dataset com mais de 500 arquivos soltos foi fatiado e organizado fisicamente nestes 3 IDs vitais, separando a telemetria brura (.csv e .txt) de forma categorizada.

## 📅 Entrada 3: A Ausência do Raio Geométrico e a Pivotagem de Escopo
**Data/Hora:** 29/09/2026 - 20:00
*A Crise:* Ao analisar o arquivo de telemetria bruto 19304A1_data.csv, confirmamos que a NASA **não** fornece uma coluna de "Raio da Chama" ou "Tamanho" pré-calculada para os analistas. Os cálculos dimensionais precisariam ser extraídos diretamente das centenas de gigabytes de vídeo da ISS (formato .hobj).

*A Resolução Técnica (Brainstorming):* Duas opções foram postadas no fórum de discussão:
1. **O Atalho de Ouro (Plano A):** Ao invés de usar o SVR (Support Vector Regression) para prever o raio da chama em centímetros, treinar a I.A. para prever a **Assinatura Termodinâmica**. Usaríamos medidas substitutas (Proxys) puramente numéricas, como o PMT (intensidade de luz emitida) e a Radiação máxima do Termopar. 
2. **Trabalho Sujo (Plano B):** Criar uma mega-pipeline em Visão Computacional (OpenCV em Python) para ler frame-a-frame dos vídeos da NASA, encontrar a borda luminosa, converter para milímetros e gerar o Dataset do zero.

*A Decisão (Pivotagem):* Optamos pela inteligência e eficiência! Adotamos um derivado genial do Plano A: Uma refinaria que extrai a assinatura termodinâmica (Pressão, Termopar do Queimador e Radiômetros).

## 📅 Entrada 4: Construindo a Refinaria de Dados (Pipeline)
**Data/Hora:** 30/09/2026 - 07:50
A equipe projetou e reescreveu o script 
asa_psi_pipeline.py. Ele atua como um trator de dados: varre todos os CSVs soltos do Dataset, infere automaticamente qual o combustível daquele teste baseando-se nas datas que mapeamos e comprime milhões de linhas em uma tabela espartana de Resultados_Treinamento_ML.csv.
* **Features (Entradas):** Pressão e Fluxo médio injetados. (Também servem perfeitamente como Boundary Conditions pro Ansys!)
* **Targets (Saídas da I.A.):** Temperatura Máxima (TCBurner) e Radiação Térmica Pura (Radiometer+60).

A infraestrutura de Inteligência Artificial acabou de nascer!

A Prova de Conceito (Proof of Concept - PoC) com Amostragem.

Não baixe 700 GB: Baixe apenas UM vídeo curto do teste de Metano (o Caso 1, que é limpo e fácil da IA enxergar).

Script de Visão Rápido (OpenCV): Usem Python com a biblioteca OpenCV (que roda leve até no processador). Escrevam um código que pega esse único vídeo, detecta a borda luminosa da chama e plota um círculo dinâmico ao redor dela frame a frame, calculando o raio em pixels.

O Pitch Matador: Na hora de apresentar para a NASA, vocês mostram o XGBoost rodando rápido com a telemetria (que é o sistema principal) e colocam o vídeo processado do lado dizendo: "Também desenvolvemos um módulo de Visão Computacional secundário. Nossa prova de conceito rodou perfeitamente em 1 vídeo. Com acesso aos servidores da agência ou nuvem AWS, esse script escalaria para os 700 GB, retroalimentando nosso modelo preditivo com precisão milimétrica."