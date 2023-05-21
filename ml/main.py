import streamlit as st
import pandas as pd
import numpy as np
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForQuestionAnswering
)
from data_processing import clear_answers, remove_duplications
from sentence_transformers import SentenceTransformer, util
import torch
import json
import re

# ========== PARSE THE ATLAS ==========

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
qa_model_name = "mrm8488/bert-multi-cased-finetuned-xquadv1"
qa_model = pipeline(
    "question-answering",
    model=qa_model_name
)
cossim_model_name = "paraphrase-multilingual-MiniLM-L12-v2"
cossim_model = SentenceTransformer(cossim_model_name)

# ========== STREAMLIT ==========
st.title('Информация о растениях')

index = st.slider("Select index", 0, 180, 5)
context = st.text_area('Введите информацию о растении', atlas_raw[split_index[index]:split_index[index+1]], height=200)

questions = st.text_area('Задайте вопросы')
questions = questions.split("\n")
questions = [x for x in questions if len(x) > 1]

# data preprocessing
context = context.replace("- ", "")
context_arr = [x for x in context.split("\n") if not x.startswith("• ")]
context = ' '.join(context_arr)

# pre-encode by cossim
cossim_preencoded = cossim_model.encode(context_arr, convert_to_tensor=True)

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
                st.markdown(f"* [{x['score']:.2f}] [{x['answer']}]")

            # filter out non-relevant versions
            answers = [x['answer'] for x in answers if x['score'] > 0.2]
            answers = remove_duplications(answers)
            if len(answers) > 0:
                joined_answers = ', '.join([x for x in answers])
                text_response = text_response + question_pair['answer'].replace("<placeholder>", joined_answers)

        # CosSim results
        for cossim_pair in prompt_group['cossim_pairs']:
            question_cossim = cossim_model.encode(cossim_pair['question'])
            st.markdown(cossim_pair['question'])
            cossim_result = util.pytorch_cos_sim(cossim_preencoded, question_cossim)
            index = np.argmax(cossim_result)
            print(torch.argmax(cossim_result))
            max_value = torch.max(cossim_result).item()
            st.markdown(f"* [{max_value}] [{context_arr[index]}]")

        # combining results
        st.markdown(f"Result: {text_response}")

    for question in questions:
        st.subheader(question)
        answer = qa_model(question=question, context=context, top_k=top_k)
        for x in answer:
            st.markdown(f"* [{x['score']:.2f}] {x['answer']}")
