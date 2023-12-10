import streamlit as st
import pandas as pd
from random import randint


# ---------------------------Funções----------------------------

def rolar(faces):
    """Retorna um valor sorteado por um dado."""

    return randint(1, faces)


def jogo(dados):
    """Retorna a soma de valores sorteado por um conjunto de dados."""

    soma = 0
    for dado_face in dados:
        soma += rolar(dado_face)

    return soma


def produzir_amostra(dados, n):
    """Produz uma amostra a partir de n rolls do conjunto de dados fornecido."""

    soma_min = len(dados)
    soma_max = sum(dados)
    somas_possiveis = list(range(soma_min, soma_max + 1))

    freq_lista = [0] * len(somas_possiveis)
    for _ in range(n):
        freq_lista[jogo(ss.dados) - soma_min] += 1

    df = pd.DataFrame(
        {
            "Soma": somas_possiveis,
            "Frequência": freq_lista
        }
    )

    return df


# -----------------------Variáveis de sessão----------------------

ss = st.session_state

if 'dados' not in ss:
    ss.dados = []

# ----------------------------Início------------------------------

st.header("Jogos de dados", anchor=False)
st.divider()

# ----------------------------Inputs----------------------------

dado_input = st.number_input("Informe o número de lados", min_value=2, step=1, value=6)

add, clear = st.columns(2)

with add:  # Adiciona um dado ao conjunto de dados
    st.button("add", on_click=ss.dados.append, args=[dado_input], use_container_width=True)

with clear:  # Limpa o conjunto de dados
    st.button("clear", on_click=ss.dados.clear, use_container_width=True)

st.write(ss.dados)

n_rolls = st.slider("Número de rolls", min_value=0, max_value=10000, step=10)

# -----------------------------Preparando-------------------------------

amostra = produzir_amostra(ss.dados, n_rolls)
if st.button("roll", use_container_width=True):
    amostra = produzir_amostra(ss.dados, n_rolls)

st.divider()

# ------------------------Desenhando o gráfico--------------------------

st.bar_chart(amostra, x="Soma", y="Frequência")
