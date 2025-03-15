import customtkinter as ctk
import requests
import re

# Configuração da API do Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Modelos disponíveis
MODELS = ["gemma3:1b", "gemma3:12b", "deepseek-r1:7b", "deepseek-r1:14b"]

# Configuração do tema
tema_escuro = "dark"
ctk.set_appearance_mode(tema_escuro)
ctk.set_default_color_theme("dark-blue")

# Histórico de conversas
historicos = {}
modelo_selecionado = None

# Criar a janela principal
janela = ctk.CTk()
janela.title("Chatbot")
janela.geometry("800x500")

# Frame esquerdo para histórico e seleção de IA
frame_lateral = ctk.CTkFrame(janela, width=200, corner_radius=10, fg_color="#111111")
frame_lateral.pack(side="left", fill="y", padx=5, pady=5)

# Label do título
titulo_ia = ctk.CTkLabel(frame_lateral, text="Modelos de IA", fg_color="#111111")
titulo_ia.pack(pady=5)

# Lista de modelos disponíveis
botoes_modelos = []
def selecionar_modelo(modelo):
    global modelo_selecionado, historicos
    modelo_selecionado = modelo

    if modelo not in historicos:
        historicos[modelo] = []
    chat_area.configure(state="normal")
    chat_area.delete("1.0", ctk.END)

    for msg in historicos[modelo]:
        exibir_mensagem(msg["content"], msg["role"])
    chat_area.configure(state="disabled")
    
    for botao in botoes_modelos:
        if botao.cget("text") == modelo:
            botao.configure(fg_color="#235284")
        else:
            botao.configure(fg_color="#222222")

def criar_botoes_modelos():
    for modelo in MODELS:
        botao = ctk.CTkButton(frame_lateral, text=modelo, command=lambda m=modelo: selecionar_modelo(m), fg_color="#222222")
        botao.pack(pady=2, fill="x")
        botoes_modelos.append(botao)
criar_botoes_modelos()

# Botão de novo chat
def novo_chat():
    global historicos

    if modelo_selecionado:
        historicos[modelo_selecionado] = []

    chat_area.configure(state="normal")
    chat_area.delete("1.0", ctk.END)
    chat_area.configure(state="disabled")

botao_novo_chat = ctk.CTkButton(frame_lateral, text="New Chat", command=novo_chat)
botao_novo_chat.pack(pady=5, fill="x")

# Frame do chat
frame_chat = ctk.CTkFrame(janela, corner_radius=10, fg_color="#222222")
frame_chat.pack(padx=10, pady=10, fill="both", expand=True)

# Área de chat
chat_area = ctk.CTkTextbox(frame_chat, wrap="word", fg_color="#222222", text_color="#FFFFFF", state="disabled")
chat_area.pack(padx=10, pady=10, fill="both", expand=True)

# Frame da entrada
frame_entrada = ctk.CTkFrame(janela, corner_radius=10, fg_color="#333333")
frame_entrada.pack(padx=10, pady=10, fill="x")

# Entrada de texto
entrada_usuario = ctk.CTkEntry(frame_entrada, fg_color="#555555", text_color="#FFFFFF", placeholder_text="Digite aqui")
entrada_usuario.pack(side="left", padx=10, pady=10, fill="both", expand=True)

# Função para formatar a resposta e remover tags desnecessárias
def formatar_resposta(texto):
    texto = re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL)  # Remove <think>...</think>
    return texto.strip()

# Função para exibir mensagens no chat
def exibir_mensagem(texto, remetente="user"):
    chat_area.configure(state="normal")

    if remetente == "user":
        tag_nome = "user_tag"
        alinhamento = "right"
        cor_fundo = "#444444"
        cor_texto = "#FFFFFF"
    else:
        tag_nome = "bot_tag"
        alinhamento = "left"
        cor_fundo = "#333333"
        cor_texto = "#DDDDDD"

    chat_area.insert(ctk.END, f"\n{texto}\n", tag_nome)
    chat_area.tag_config(tag_nome, justify=alinhamento, background=cor_fundo, foreground=cor_texto, lmargin1=10, rmargin=10, spacing1=5, spacing3=5)
    chat_area.yview(ctk.END)
    chat_area.configure(state="disabled")

# Função para enviar mensagem
def enviar_mensagem():
    global historicos, modelo_selecionado

    if not modelo_selecionado:
        return
    user_input = entrada_usuario.get().strip()

    if not user_input:
        return  
    
    exibir_mensagem("Você: " + user_input, "user")
    historicos[modelo_selecionado].append({"role": "user", "content": user_input})
    data = {"model": modelo_selecionado, "prompt": "\n".join([msg["content"] for msg in historicos[modelo_selecionado]]), "stream": False}

    try:
        response = requests.post(OLLAMA_API_URL, json=data)

        if response.status_code == 200:
            resposta = response.json().get("response", "Nenhuma resposta recebida.")

            resposta_formatada = formatar_resposta(resposta)

            historicos[modelo_selecionado].append({"role": "assistant", "content": resposta_formatada})
            exibir_mensagem("Ollama: " + resposta_formatada, "bot")
        else:
            exibir_mensagem(f"Erro na requisição: {response.status_code}", "bot")

    except requests.exceptions.RequestException as e:
        exibir_mensagem(f"Erro de conexão: {e}", "bot")

    entrada_usuario.delete(0, ctk.END)
    chat_area.yview(ctk.END)

# Botão de enviar
botao_enviar = ctk.CTkButton(frame_entrada, text="Enviar", command=enviar_mensagem, fg_color="#666666", hover_color="#235284")
botao_enviar.pack(side="right", padx=10, pady=10)

janela.mainloop()
