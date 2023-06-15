import streamlit as st
from streamlit_chat import message
import json
import boto3
from streamlit_extras.colored_header import colored_header
from io import StringIO
import yaml

#setting up boto3 client and reading the endpoint name
client = boto3.client('sagemaker-runtime')
with open(r'../endpoint_config.yaml') as file:
    endpoint_config = yaml.safe_load(file)


st.set_page_config(
    page_title="MyBank Call centre agent assist",
    page_icon=":robot:"
)

st.header("AnyBank Call centre agent assist")

st.sidebar.title("Sidebar")

uploaded_file = st.sidebar.file_uploader("Upload a recent call centre transcription file(txt files only)", type=["txt"])


if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm call centre agent assist, How may I help you?"]

if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

if 'context' not in st.session_state:
    st.session_state['context'] = ''


colored_header(label='', description='', color_name='orange-30')
response_container = st.container()
input_container = st.container()



# Response output Function for taking user prompt as input
# followed by producing AI generated responses

def generate_response(context, query):
    prompt = f'{context}\n{query}'

    # hyperparameters for llm
    prompt_with_config = {
        "inputs": prompt,
        "parameters": {
            "do_sample": True,
            "top_p": 0.9,
            "temperature": 0.4,
            "max_new_tokens": 1024,
            "repetition_penalty": 1.03
        }
    }

    # send request to endpoint
    payload = json.dumps(prompt_with_config).encode('utf-8')

    response = client.invoke_endpoint(EndpointName=endpoint_config['endpoint_name'],
                                      ContentType='application/json',
                                      Body=payload)
    model_predictions = json.loads(response['Body'].read())

    # print assistant respond
    return model_predictions[0]["generated_text"][len(prompt):]



# Applying the user input box
with input_container:
    # user_input = get_text()
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')
        # st.sidebar.write("Here is the uploaded transcript:\n")
        # st.sidebar.text(st.session_state['context'])

    if submit_button and user_input:
        response = generate_response(st.session_state['context'], user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(response)
        st.sidebar.write("Here is the uploaded transcript:\n")
        st.sidebar.text(st.session_state['context'])
    elif uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.session_state['context'] = stringio.read()
        st.session_state['past'].append('Can you confirm that you have read the trascript?')
        st.session_state['generated'].append('Yes, I have read the transcript. Ask me anything about it.')
        st.sidebar.write("Here is the uploaded transcript:\n")
        st.sidebar.text(st.session_state['context'])
         
        
# Conditional display of AI generated responses as a function of user provided prompts

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))



