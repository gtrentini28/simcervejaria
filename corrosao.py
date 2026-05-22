import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página
st.set_page_config(page_title="Simulação: Corrosão CUI vs Proteção", layout="centered")

st.title("Simulação CUI: Inox 304L vs Alumínio")
st.markdown("Arraste o controle de tempo e alterne o método para visualizar a física da corrosão.")

# Controles na barra lateral
st.sidebar.header("Parâmetros do Sistema")
metodo = st.sidebar.radio("Método de Proteção:", ["Sem Proteção (Tubo Nu)", "Envelopado com Alumínio"])
tensao = st.sidebar.checkbox("Aplicar Tensão (Área de Solda)", value=True)
tempo = st.sidebar.slider("Tempo / Ataque de Cloretos (%)", 0, 100, 0)

# Configuração do Gráfico
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# 1. Desenhando a Malha de Aço (Fe e C)
x_fe = []
y_fe = []
colors_fe = []

for i in range(1, 10):
    for j in range(1, 5):
        # Lógica de quebra (Fissuração - SCC)
        if metodo == "Sem Proteção (Tubo Nu)" and tempo > 40:
            if tensao and (i == 5 or i == 6) and j > (5 - (tempo/20)): 
                continue # Pula o desenho do átomo (simula o buraco/trinca)
            if not tensao and (i == 5) and j == 4 and tempo > 70:
                continue # Pite superficial
                
        # Tensão afasta os átomos do centro
        offset = 0
        if tensao and i < 5: offset = -0.2
        if tensao and i >= 5: offset = 0.2
            
        x_fe.append(i + offset)
        y_fe.append(j)
        colors_fe.append('darkgray')

ax.scatter(x_fe, y_fe, s=300, c=colors_fe, edgecolors='black', label='Átomos de Ferro (Fe)')

# 2. Desenhando a Camada Passiva
if metodo == "Sem Proteção (Tubo Nu)" and tempo > 30:
    ax.plot([0, 4.5], [4.5, 4.5], color='lime', linewidth=3)
    ax.plot([5.5, 10], [4.5, 4.5], color='lime', linewidth=3)
else:
    ax.plot([0, 10], [4.5, 4.5], color='lime', linewidth=3, label='Camada Passiva (Óxido de Cromo)')

# 3. Desenhando a Folha de Alumínio (Se ativado)
if metodo == "Envelopado com Alumínio":
    espessura_al = 8.0 - (tempo * 0.03) # Alumínio afina com o tempo (sacrifício)
    if espessura_al > 4.6:
        ax.fill_between([0, 10], 4.6, espessura_al, color='silver', alpha=0.9, label='Folha de Alumínio (Ânodo)')
        
        # Íons de alumínio se soltando
        if tempo > 10:
            ax.scatter(np.random.uniform(1, 9, int(tempo/5)), 
                       np.random.uniform(espessura_al, 9.5, int(tempo/5)), 
                       s=50, c='yellow', marker='^', label='Íons Al3+ (Sacrifício)')

# 4. Desenhando o Eletrólito e Cloretos (Cl-)
ax.fill_between([0, 10], max(5.0, espessura_al if metodo == "Envelopado com Alumínio" else 5.0), 10, color='lightblue', alpha=0.3, label='Água quente (CIP)')
num_cloretos = int(tempo / 2)
if num_cloretos > 0:
    # Cloretos descem para a trinca se não houver proteção
    y_cl = np.random.uniform(5, 9.5, num_cloretos)
    x_cl = np.random.uniform(0.5, 9.5, num_cloretos)
    
    if metodo == "Sem Proteção (Tubo Nu)" and tempo > 50 and tensao:
        for k in range(min(15, num_cloretos)):
            x_cl[k] = np.random.uniform(4.5, 5.5)
            y_cl[k] = np.random.uniform(1.5, 4.0) # Cl- dentro da trinca
            
    ax.scatter(x_cl, y_cl, s=80, c='red', label='Cloretos (Cl-)')

# Legenda e Exibição
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small')
st.pyplot(fig)

st.caption("Nota Técnica: O alumínio age como ânodo de sacrifício, protegendo a malha de aço 304L contra cloretos a quente.")