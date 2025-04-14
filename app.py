from flask import Flask, request, jsonify, render_template_string
from transformers import LlamaTokenizer, LlamaForCausalLM

app = Flask(__name__)

# Carregar o Tokenizer e o Modelo LLaMA
tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")

# Função para gerar texto com o modelo LLaMA
def gerar_texto(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs['input_ids'], max_length=50)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Rota principal para servir a interface HTML
@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Interface Cyberpunk</title>

      <!-- Anime.js -->
      <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>

      <!-- Fonte estilo digital -->
      <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet" />

      <style>
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        body {
          font-family: 'Orbitron', sans-serif;
          background: linear-gradient(135deg, #2B0E12, #0d0907);
          color: #ff3c00;
          overflow: hidden;
        }

        /* Primeira transição - digitação */
        #transition-screen {
          position: fixed;
          width: 100vw;
          height: 100vh;
          background: linear-gradient(135deg, #2B0E12, #0d0907);
          display: flex;
          align-items: center;
          justify-content: center;
          flex-direction: column;
          z-index: 9999;
          font-size: 1.2rem;
        }

        .type-line {
          opacity: 0;
          margin: 5px 0;
          white-space: pre;
        }

        /* Segunda transição - sistema ligando */
        #boot-animation {
          position: fixed;
          width: 100vw;
          height: 100vh;
          background-color: #0d0907;
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 9998;
          opacity: 0;
        }

        .boot-line {
          width: 0;
          height: 2px;
          background: #ff3c00;
        }

        /* Conteúdo do Chat */
        #main-content {
          display: none;
          padding: 40px;
          text-align: center;
          z-index: 1;
        }

        .chat-box {
          background-color: rgba(0, 0, 0, 0.3);
          border: 1px solid #ff3c00;
          padding: 20px;
          border-radius: 10px;
          margin-top: 30px;
          max-width: 600px;
          margin-left: auto;
          margin-right: auto;
        }

        .message {
          text-align: left;
          margin-bottom: 10px;
        }

        .message.user {
          text-align: right;
        }

        input, button {
          background: #0d0907;
          color: #ff3c00;
          border: 1px solid #ff3c00;
          padding: 10px;
          font-family: 'Orbitron', sans-serif;
          width: 70%;
          margin-top: 15px;
        }

        button {
          width: 20%;
          margin-left: 5px;
          cursor: pointer;
        }
      </style>
    </head>
    <body>

      <!-- Primeira Transição (hack digitando) -->
      <div id="transition-screen">
        <div class="type-line" id="line1"></div>
        <div class="type-line" id="line2"></div>
        <div class="type-line" id="line3"></div>
      </div>

      <!-- Segunda Transição (boot) -->
      <div id="boot-animation">
        <div class="boot-line"></div>
      </div>

      <!-- Conteúdo final com Chat -->
      <div id="main-content">
        <h1>🤖 Interface Neural Conectada</h1>
        <div class="chat-box" id="chat-box">
          <div class="message ia">IA: Conexão estabelecida. Estou ouvindo.</div>
        </div>
        <div>
          <input type="text" id="userInput" placeholder="Digite sua mensagem..." />
          <button onclick="sendMessage()">Enviar</button>
        </div>
      </div>

      <script>
        // Digitação da primeira transição
        const lines = [
          { id: "line1", text: "> Estabelecendo conexão segura..." },
          { id: "line2", text: "> Decodificando firewall..." },
          { id: "line3", text: "> Acesso concedido." }
        ];

        function typeLine(index) {
          if (index >= lines.length) {
            setTimeout(() => showBoot(), 800);
            return;
          }

          const { id, text } = lines[index];
          const el = document.getElementById(id);
          el.style.opacity = 1;
          let i = 0;
          const typing = setInterval(() => {
            if (i < text.length) {
              el.textContent += text.charAt(i);
              i++;
            } else {
              clearInterval(typing);
              setTimeout(() => typeLine(index + 1), 500);
            }
          }, 50);
        }

        typeLine(0);

        // Segunda transição (boot)
        function showBoot() {
          const transition = document.getElementById("transition-screen");
          const boot = document.getElementById("boot-animation");
          const bootLine = document.querySelector(".boot-line");

          transition.style.display = 'none';
          boot.style.opacity = 1;

          anime({
            targets: bootLine,
            width: ['0%', '100%'],
            duration: 1000,
            easing: 'easeInOutExpo',
            complete: () => {
              anime({
                targets: bootLine,
                height: ['2px', '100vh'],
                duration: 800,
                easing: 'easeInOutExpo',
                complete: () => {
                  boot.style.display = 'none';
                  document.getElementById("main-content").style.display = 'block';
                }
              });
            }
          });
        }

        // Função para enviar a mensagem e obter resposta da IA
        function sendMessage() {
          const input = document.getElementById("userInput");
          const msg = input.value.trim();
          if (msg === "") return;

          const chat = document.getElementById("chat-box");

          // Exibe a mensagem do usuário
          const userMsg = document.createElement("div");
          userMsg.className = "message user";
          userMsg.textContent = "Você: " + msg;
          chat.appendChild(userMsg);

          // Faz a requisição para o Flask
          fetch('/gerar', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: msg })
          })
          .then(response => response.json())
          .then(data => {
            // Exibe a resposta da IA
            const iaMsg = document.createElement("div");
            iaMsg.className = "message ia";
            iaMsg.textContent = "IA: " + data.resposta;
            setTimeout(() => {
              chat.appendChild(iaMsg);
              chat.scrollTop = chat.scrollHeight;
            }, 500);
          })
          .catch(error => {
            const iaMsg = document.createElement("div");
            iaMsg.className = "message ia";
            iaMsg.textContent = "IA: Erro ao processar a solicitação.";
            chat.appendChild(iaMsg);
          });

          input.value = "";
        }
      </script>

    </body>
    </html>
    """
    return render_template_string(html_content)

# Rota para gerar a resposta da IA
@app.route('/gerar', methods=['POST'])
def gerar():
    prompt = request.json.get('prompt')
    if prompt:
        resposta = gerar_texto(prompt)
        return jsonify({'resposta': resposta})
    return jsonify({'error': 'Prompt não fornecido!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
