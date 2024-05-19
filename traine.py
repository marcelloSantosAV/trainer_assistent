import openai
from dotenv import load_dotenv, find_dotenv
import streamlit as st
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv(find_dotenv())

# Configurar a API da OpenAI com a chave API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para gerar respostas usando a API da OpenAI
def gerar_resposta(mensagens):
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=mensagens
    )
    return resposta['choices'][0]['message']['content'].strip()

# Interface do Usuário com Streamlit
st.title("Assistente Personal Trainer")

# Variáveis de sessão para armazenar o estado da conversa
if 'mensagens' not in st.session_state:
    st.session_state['mensagens'] = [{"role": "system", "content": "Você é um assistente personal trainer."}]
if 'historico' not in st.session_state:
    st.session_state['historico'] = []
if 'nome' not in st.session_state:
    st.session_state['nome'] = ""
if 'input_key' not in st.session_state:
    st.session_state['input_key'] = "input_1"

# Mostrar o nome do usuário
if st.session_state['nome']:
    st.write(f"Olá, {st.session_state['nome']}!")

# Mostrar histórico da conversa
for chat in st.session_state['historico']:
    st.write(f"{chat['role']}: {chat['content']}")

# Entrada do usuário
def enviar_mensagem():
    entrada_usuario = st.session_state['mensagem']
    if entrada_usuario:
        # Adicionar a mensagem do usuário ao histórico
        st.session_state['mensagens'].append({"role": "user", "content": entrada_usuario})
        st.session_state['historico'].append({"role": "Você", "content": entrada_usuario})
        
        # Gerar resposta do assistente
        resposta = gerar_resposta(st.session_state['mensagens'])
        
        # Adicionar a resposta do assistente ao histórico
        st.session_state['mensagens'].append({"role": "assistant", "content": resposta})
        st.session_state['historico'].append({"role": "Assistente", "content": resposta})
        
        # Extrair o nome do usuário se ainda não foi feito
        if not st.session_state['nome']:
            st.session_state['nome'] = entrada_usuario
        
        # Resetar o input
        st.session_state['mensagem'] = ""

# Configurar o input para enviar a mensagem ao clicar no botão
mensagem = st.text_input(f"Olá, {st.session_state['nome']}, digite aqui:")
enviar = st.button("Enviar")
if enviar:
    st.session_state['mensagem'] = mensagem
    enviar_mensagem()

# Inicializar a conversa
if 'iniciado' not in st.session_state:
    st.session_state['mensagens'].append({"role": "assistant", "content": "Olá, sou seu Personal Trainer. Qual é o seu nome?"})
    st.session_state['historico'].append({"role": "Assistente", "content": "Olá, sou seu Personal Trainer. Qual é o seu nome?"})
    st.session_state['iniciado'] = True
