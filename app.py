import streamlit as st
import requests
import json

# Configuración de las API keys
together_api_key = st.secrets["TOGETHER_API_KEY"]
serper_api_key = st.secrets["SERPER_API_KEY"]

def generate_thesis(prompt):
    url = "https://api.together.xyz/inference"
    headers = {
        "Authorization": f"Bearer {together_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "togethercomputer/llama-2-70b-chat",
        "prompt": f"Genera una tesis interesante para desarrollar sobre la Escuela de Salamanca: {prompt}",
        "max_tokens": 200,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['output']['choices'][0]['text']

def search_serper(query):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    data = {
        "q": query
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def answer_question(question, author):
    search_results = search_serper(f"{author} {question} Escuela de Salamanca")
    context = "\n".join([result['snippet'] for result in search_results.get('organic', [])])
    
    prompt = f"""
    Basándote en la siguiente información, responde a la pregunta "{question}" sobre {author} de la Escuela de Salamanca.
    Asegúrate de citar las fuentes, incluyendo cualquier texto en latín si está disponible.
    
    Contexto:
    {context}
    
    Respuesta:
    """
    
    url = "https://api.together.xyz/inference"
    headers = {
        "Authorization": f"Bearer {together_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "togethercomputer/llama-2-70b-chat",
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.3
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['output']['choices'][0]['text']

st.title("Escuela de Salamanca: Generador de Tesis y Preguntas")

tab1, tab2 = st.tabs(["Generador de Tesis", "Preguntas sobre Autores"])

with tab1:
    st.header("Generador de Tesis")
    thesis_prompt = st.text_input("Introduce un tema o concepto para generar una tesis:")
    if st.button("Generar Tesis"):
        with st.spinner("Generando tesis..."):
            thesis = generate_thesis(thesis_prompt)
            st.write(thesis)

with tab2:
    st.header("Preguntas sobre Autores")
    author = st.text_input("Nombre del autor de la Escuela de Salamanca:")
    question = st.text_area("Tu pregunta sobre el autor:")
    if st.button("Buscar Respuesta"):
        with st.spinner("Buscando respuesta..."):
            answer = answer_question(question, author)
            st.write(answer)
