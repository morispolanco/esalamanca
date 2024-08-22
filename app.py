import streamlit as st
import requests
import json

# Configuración de las API keys
together_api_key = st.secrets["TOGETHER_API_KEY"]
serper_api_key = st.secrets["SERPER_API_KEY"]

# Lista de autores de la Escuela de Salamanca
autores = [
    "Arias Piñel (1512-1563)", "Antonio de Padilla y Meneses (-1580)", "Bartolomé de Albornoz (1519-1573)",
    "Bartolomé de Medina (1527-1581)", "Diego de Chaves (1507-1592)", "Diego de Covarrubias (1512-1577)",
    "Diego Pérez de Mesa (1563-1632)", "Domingo Báñez (1528-1604)", "Domingo de Soto (1494-1560)",
    "Fernán Pérez de Oliva (1494-1531)", "Francisco de Vitoria (1492-1546)", 
    "Francisco Sarmiento de Mendoza (1525-1595)", "Francisco Suárez (1548-1617)", 
    "Gregorio de Valencia (1549-1603)", "Jerónimo Muñoz (1520-1591)", 
    "Juan de Horozco y Covarrubias (1540-1610)", "Juan de la Peña (1513-1565)", "Juan de Matienzo (1520-1579)",
    "Juan de Ribera (1532-1611)", "Juan Gil de la Nava (-1551)", "Leonardus Lessius (1554-1623)",
    "Luis de León (1527-1591)", "Martín de Azpilcueta (1492-1586)", "Martín de Ledesma (1509-1574)",
    "Melchor Cano (1509-1560)", "Pedro de Sotomayor (1511-1564)", "Tomás de Mercado (1523-1575)",
    "Alonso de la Vera Cruz (1507-1584)", "Cristóbal de Villalón (-1588)", 
    "Fernando Vázquez de Menchaca (1512-1569)", "Francisco Cervantes de Salazar (1513/18-1575)",
    "Juan de Lugo y Quiroga (1583-1660)", "Juan de Salas (1553-1612)", "Luis de Molina (1535-1600)",
    "Pedro de Aragón (1545/46-1592)", "Pedro de Valencia (1555-1620)", "Antonio de Hervías (-1590)",
    "Bartolomé de Carranza (1503-1576)", "Bartolomé de las Casas (1484-1566)", 
    "Cristóbal de Fonseca (1550-1621)", "Domingo de Salazar (1512-1594)", 
    "Domingo de Santo Tomás (1499-1570)", "Gabriel Vásquez (1549-1604)", "Gómez Pereira (1500–1567)",
    "Juan de Mariana (1536-1624)", "Juan de Medina (1489-1545)", "Juan Pérez de Menacho (1565-1626)",
    "Luis de Alcalá (1490-1549)", "Luis Saravia de la Calle (?)", "Miguel Bartolomé Salón (1539-1621)",
    "Pedro de Fonseca (1528-1599)", "Pedro de Oñate (1567-1646)", "Rodrigo de Arriaga (1592-1667)"
]

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

def answer_question(question, authors):
    authors_str = ", ".join(authors)
    search_results = search_serper(f"{authors_str} {question} Escuela de Salamanca")
    context = "\n".join([result['snippet'] for result in search_results.get('organic', [])])
    
    prompt = f"""
    Basándote en la siguiente información, responde a la pregunta "{question}" dirigida a {authors_str} de la Escuela de Salamanca.
    Asegúrate de citar las fuentes, incluyendo cualquier texto en latín si está disponible.
    Si la pregunta se dirige a varios autores, intenta incluir las perspectivas de cada uno de ellos en la respuesta.
    
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

st.title("Escuela de Salamanca: Generador de Tesis y Preguntas a Autores")

tab1, tab2 = st.tabs(["Generador de Tesis", "Preguntas a Autores"])

with tab1:
    st.header("Generador de Tesis")
    thesis_prompt = st.text_input("Introduce un tema o concepto para generar una tesis:")
    if st.button("Generar Tesis", key="generate_thesis"):
        with st.spinner("Generando tesis..."):
            thesis = generate_thesis(thesis_prompt)
            st.write(thesis)

with tab2:
    st.header("Preguntas a Autores")
    selected_authors = st.multiselect("Selecciona uno o varios autores:", autores)
    question = st.text_area("Tu pregunta para los autores seleccionados:")
    if st.button("Buscar Respuesta", key="search_answer"):
        if selected_authors and question:
            with st.spinner("Buscando respuesta..."):
                answer = answer_question(question, selected_authors)
                st.write(answer)
        else:
            st.warning("Por favor, selecciona al menos un autor y escribe una pregunta.")
