import pandas as pd
import numpy as np
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForQuestionAnswering
)
from data_processing import clear_answers, remove_duplications
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
import torch
import json
import re

# ========== PARSE THE ATLAS ==========

# read species
f = open("species.txt", "r")
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
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
qa_model_name = "deepset/xlm-roberta-large-squad2"
qa_model = pipeline(
    "question-answering",
    model=qa_model_name,
    device=0
)
# cossim_model_name = "paraphrase-multilingual-MiniLM-L12-v2"
# cossim_model = SentenceTransformer(cossim_model_name)

# compile a CSV
daf = pd.DataFrame([], columns=[
    'name',
    'area',
    'soil',
    'timings',
    'chemicals',
    'medicine'
])
# for ix in tqdm(range(len(split_index) - 1)):
for ix in tqdm(range(10)):
    context = atlas_raw[split_index[ix]:split_index[ix+1]]
    # data preprocessing
    context = context.replace("- ", "")
    context_arr = [x for x in context.split("\n") if not x.startswith("• ")]
    context = ' '.join(context_arr)

    # pre-encode by cossim
    # cossim_preencoded = cossim_model.encode(context_arr, convert_to_tensor=True)

    # question answering
    result = {
        "name": species[ix]
    }
    top_k = 2
    for prompt_group in prompts:
        group_name = prompt_group['group_name']
        text_response = ""

        # QA results
        for question_pair in prompt_group['question_pairs']:
            answers = qa_model(question=question_pair['question'], context=context, top_k=top_k)

            # full result for debugging
            # for x in answers:
            #     st.markdown(f"* [{x['score']:.2f}] [{x['answer']}]")

            # filter out non-relevant versions
            answers = [x['answer'] for x in answers if x['score'] > 0.2]
            answers = remove_duplications(answers)
            if len(answers) > 0:
                joined_answers = ', '.join([x for x in answers])
                text_response = text_response + question_pair['answer'].replace("<placeholder>", joined_answers)

        # CosSim results
        # for cossim_pair in prompt_group['cossim_pairs']:
        #     question_cossim = cossim_model.encode(cossim_pair['question'])
        #     st.markdown(cossim_pair['question'])
        #     cossim_result = util.pytorch_cos_sim(cossim_preencoded, question_cossim)
        #     index = np.argmax(cossim_result)
        #     max_value = torch.max(cossim_result).item()
        #     st.markdown(f"* [{max_value}] [{context_arr[index]}]")

        # combining results
        result[group_name] = text_response
    daf = daf.append(result, ignore_index=True)
daf.to_csv("data/result.csv", index=False)
