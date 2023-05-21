import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForQuestionAnswering
)
# from data_processing import clear_answers, remove_duplications
from sentence_transformers import SentenceTransformer, util
import numpy as np
import torch
import json
import re

def clear_answers(source_string):
    source_string.strip()

    unwanted_prefixes = [
        "в ",
        "В ",
        "на ",
        "На ",
        ", ",
        "; "
    ]

    if source_string[-1] in [
        ".",
        ";",
        ","
    ]:
        source_string = source_string[:-1]
    return source_string


def remove_duplications(source_strings):
    return list(np.unique(source_strings))


st.set_page_config(
    page_title="Поиск",
    page_icon="🌍"
)

st.markdown("# Информация о растении")
st.sidebar.header("Mapping Demo")
st.write(
    """This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data."""
)

specie = st.text_input("Название растения", placeholder="Введите название растения")

# read species
f = open("data/atlas_species.txt", "r")
species = f.readlines()
species = [x.replace("\n", "") for x in species]

# read file
f = open("input.txt", "r")
atlas_raw = ''.join(f.readlines())

split_index = []
for specie in species:
    occasions = [m.start() for m in re.finditer(specie, atlas_raw)]
    split_index.append(occasions[0])

# prompts
f = open('data/prompts.json')
prompts = json.load(f)

# ========== INITIALIZE THE MODEL ==========
qa_model_name = "deepset/xlm-roberta-large-squad2"
qa_model = pipeline(
    "question-answering",
    model=qa_model_name
)
# cossim_model_name = "paraphrase-multilingual-MiniLM-L12-v2"
# cossim_model = SentenceTransformer(cossim_model_name)

# ========== STREAMLIT ==========
index = 5
context = st.text_area('Введите информацию о растении', atlas_raw[split_index[index]:split_index[index+1]], height=200)

questions = st.text_area('Задайте вопросы')
questions = questions.split("\n")
questions = [x for x in questions if len(x) > 1]

# data preprocessing
context = context.replace("- ", "")
context_arr = [x for x in context.split("\n") if not x.startswith("• ")]
context = ' '.join(context_arr)

# pre-encode by cossim
# cossim_preencoded = cossim_model.encode(context_arr, convert_to_tensor=True)

# question answering
top_k = 2
if st.button('Обработать'):
    for prompt_group in prompts:
        st.subheader(prompt_group['title'])
        text_response = ""

        # QA results
        for question_pair in prompt_group['question_pairs']:
            answers = qa_model(question=question_pair['question'], context=context, top_k=top_k)

            # full result for debugging
            st.markdown(question_pair['question'])
            for x in answers:
                st.markdown(f"* [{x['score']:.2f}] [{clear_answers(x['answer'])}]")

            # filter out non-relevant versions
            answers = [x['answer'] for x in answers if x['score'] > 0.1]
            answers = [clear_answers(x) for x in answers]
            answers = remove_duplications(answers)
            if len(answers) > 0:
                joined_answers = ', '.join([x for x in answers])
                text_response = text_response + question_pair['answer'].replace("<placeholder>", joined_answers)
        # combining results
        st.markdown(f"Result: {text_response}")

    for question in questions:
        st.subheader(question)
        answer = qa_model(question=question, context=context, top_k=top_k)
        for x in answer:
            st.markdown(f"* [{x['score']:.2f}] {x['answer']}")
