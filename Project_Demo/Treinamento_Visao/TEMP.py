import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Carrega a telemetria do ensaio 19304A1
caminho_csv = r"D:\NASA\dataset\19304\A1\19304A1_data.csv"
df = pd.read_csv(caminho_csv, skiprows=1)

# Converte a coluna inteira para a dimensão de Tempo (Datetime)
tempo_real = pd.to_datetime(df['Time'], format="%H:%M:%S:%f")

# Cria o espaço do gráfico
plt.figure(figsize=(14, 7))

# === EIXO Y PRIMÁRIO (Temperatura e Gás) ===
ax1 = plt.gca()
ax1.plot(tempo_real, df['TCA'], color='red', label='Temperatura TCA (C)', linewidth=2)
# Multiplicamos o metano por 100 para ele ficar visível ao lado da temperatura (que é bem maior)
ax1.plot(tempo_real, df['MFCA3FuelFlow'] * 100, color='blue', label='Fluxo de Metano (x100)', linestyle='--') 

ax1.set_xlabel('Linha do Tempo (NASA)', fontsize=12)
ax1.set_ylabel('Temperatura (C) / Fluxo', fontsize=12)
ax1.tick_params(axis='y')

# Formata o eixo X para exibir as horas, minutos, segundos e milissegundos perfeitos
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S.%f"))

# === EIXO Y SECUNDÁRIO (Sensor Físico da Chama) ===
ax2 = ax1.twinx()
ax2.plot(tempo_real, df['IonCurrent'], color='purple', alpha=0.5, label='Ion Current (Combustão)', linewidth=2)
ax2.set_ylabel('Corrente Iônica (V)', fontsize=12)

# === TÍTULOS E ESTÉTICA ===
plt.title('Comportamento Termodinâmico - ACME s-Flame 19304 A1', fontsize=16)
fig = plt.gcf()
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9), fontsize=10)

plt.grid(True, alpha=0.3)
plt.tight_layout()

# Abre a janela interativa
plt.show()
