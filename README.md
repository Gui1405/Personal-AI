# Chatbot com CustomTkinter e Ollama API

## Descrição
Este projeto é um chatbot desenvolvido com a biblioteca **CustomTkinter** para interface gráfica e utiliza a **API do Ollama** para processar as respostas da IA. 

### 🎯 Objetivos e Facilidades
- Interface gráfica moderna e responsiva com **CustomTkinter**.
- Suporte a múltiplos modelos de IA, permitindo a seleção de diferentes modelos diretamente na interface.
- Histórico de conversa separado para cada modelo.
- Envio de mensagens e exibição estruturada das respostas.
- Formatação automática para remover tags indesejadas nas respostas da IA.

---

## 📌 Requisitos
Antes de executar o projeto, certifique-se de ter instalado os seguintes pacotes:

```sh
pip install customtkinter requests
```

Além disso, é necessário ter o **servidor da API do Ollama** rodando localmente. Por padrão, o projeto faz requisições para:

```
http://localhost:11434/api/generate
```

Também é necessário garantir:
1. **Ollama instalado no PC** - Baixe e instale em: [https://ollama.com](https://ollama.com)
2. **Modelos de IA desejados baixados** via Ollama. Exemplo:
   ```sh
   ollama pull gemma3:12b
   ```

---

## 🚀 Como Executar
1. Clone este repositório ou copie o código para um arquivo Python.
2. Instale as dependências listadas acima.
3. **Inicie o servidor do Ollama** antes de rodar o programa:
   ```sh
   ollama serve
   ```
4. Execute o arquivo Python:
   ```sh
   python personal_ai.py
   ```
5. Selecione um modelo de IA na interface e comece a interagir com o chatbot.

---

## 📂 Estrutura do Projeto
- `OLLAMA_API_URL`: Define o endpoint para a comunicação com a API da IA.
- `MODELS`: Lista de modelos de IA disponíveis.
- `selecionar_modelo(modelo)`: Atualiza o modelo de IA selecionado e carrega o histórico da conversa.
- `novo_chat()`: Reinicia a conversa do modelo atual.
- `enviar_mensagem()`: Envia uma mensagem para a API da IA e exibe a resposta no chat.
- `formatar_resposta(texto)`: Formata a resposta para remover tags indesejadas.

---

## 🛠 Melhorias Futuras
- Implementação de suporte a mais modelos de IA.
- Opção para salvar e carregar históricos de conversa.
- Melhorias na interface gráfica para maior usabilidade.

---

## 🐜 Licença
Este projeto é open-source e pode ser modificado livremente.

---

## 👤 Autor
Desenvolvido por **Guilherme Barroso Costa**.
