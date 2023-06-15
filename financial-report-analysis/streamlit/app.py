from requests.auth import HTTPBasicAuth
from cohere_sagemaker import Client
import streamlit as st
import requests
import boto3
import json
import yaml
import re
import ai21



TEXT_EMBEDDING_ENDPOINT_NAME = 'huggingface-textembedding-gpt-j-6b-fp16-1685703520'
TEXT_GENERATION_ENDPOINT_NAME = 'j2-jumbo-instruct'

sagemaker_client = boto3.client('runtime.sagemaker')


with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

es_username = config['credentials']['username']
es_password = config['credentials']['password']

domain_endpoint = config['domain']['endpoint']
domain_index = config['domain']['index']

URL = f'{domain_endpoint}/{domain_index}/_search'

# --------------------------------- STREAMLIT APP --------------------------------- 

st.subheader('Natwest Annual report assistant')

# Receive user input from the chat UI
prompt = st.text_input('Question: ', placeholder='Ask me anything about Natwest Annual Report 2022...', key='input')


def clean_text(text):
    # Use regular expression to match and remove any trailing characters after the last period.
    cleaned_text = re.sub(r'\.[^\.]*$', '.', text)
    return cleaned_text


if st.button('Submit', type='primary'):
    st.markdown('----')
    payload = {'text_inputs': [prompt]}
    payload = json.dumps(payload).encode('utf-8')
    response = sagemaker_client.invoke_endpoint(EndpointName=TEXT_EMBEDDING_ENDPOINT_NAME, 
                                                ContentType='application/json', 
                                                Body=payload)
    body = json.loads(response['Body'].read())
    embedding = body['embedding'][0]

    K = 1  # Retrieve Top 3 matching context

    query = {
        'size': K,
        'query': {
            'knn': {
                'embedding': {
                    'vector': embedding,
                    'k': K
                }
            }
        }
    }

    response = requests.post(URL, auth=HTTPBasicAuth(es_username, es_password), json=query)
    response_json = response.json()
    hits = response_json['hits']['hits']

    res_box = st.empty()
    
    
    
    command = """Below is some text:"""
    context_question_separator = "##"
    
    if not hits:
        res_box.write("Sorry! I couldn't find an answer to your question")

    for hit in hits:
        score = hit['_score']
        passage = hit['_source']['passage']
        doc_id = hit['_source']['doc_id']
        passage_id = hit['_source']['passage_id']
        # qa_prompt = f'Context: {passage}\nQuestion: {prompt}\nAnswer:'
        instruction = f'{command}\n{passage}\n\n{context_question_separator}\n\n{prompt}'

        report = []
        res_box = st.empty()
        
        response = ai21.Completion.execute(sm_endpoint=TEXT_GENERATION_ENDPOINT_NAME,
                                       prompt=instruction,
                                       maxTokens=100,
                                       temperature=0.2,
                                       numResults=1)
        
        answer = response['completions'][0]['data']['text']
        answer = clean_text(answer)
        
        if len(answer) > 0:
            res_box.markdown(f'**Answer:**\n*{answer}*')

        res_box = st.empty()
        res_box.markdown(f'**Reference**:\n*Document = {doc_id} | Passage = {passage_id} | Score = {score}*')
        res_box = st.empty()
        st.markdown('----')