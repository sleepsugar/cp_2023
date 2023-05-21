import streamlit as st
import time
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="База данных",
    page_icon="📈"
)

st.markdown("# Данные о растениях")


# ========== READ THE DATA ==========

# species
f = open("data/atlas_species.txt", "r")
species = [x.replace("\n", "") for x in f.readlines()]

# collected CSV
daf_path = "data/result.csv"
daf = pd.read_csv(daf_path)

# ==============================

search_query = st.text_input("Поиск по базе данных", placeholder="Поиск по базе данных")
for ix, specie in enumerate([x for x in species if search_query.lower() in x.lower()]):
    row = daf[daf['name'] == specie]
    if row.shape[0] == 0:
        continue
    row = row.iloc[0]

    # st.markdown(f"**{specie}**")
    with st.expander(f"**{specie}**"):
        st.markdown(f"**Поизрастает:** {row['area']}")
        st.markdown(f"**Почва:** {row['soil']}")
        st.markdown(f"**Время:** {row['timings']}")
        st.markdown(f"**Время:** {row['chemicals']}")
        st.markdown(f"**Время:** {row['medicine']}")
