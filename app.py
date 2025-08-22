# app.py
from flask import Flask, render_template, request, jsonify
import json
import openai
import os

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        message = request.json['message']
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            max_tokens=150
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def load_data():
    with open('static/data/content.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/contact', methods=['POST'])
def contact():
    try:
        name = request.form['name']
        email = request.form['email']
        subject = request.form.get('subject', '')
        message = request.form['message']
        print(f"[Contato] {name} ({email}) - Assunto: {subject} | Mensagem: {message[:50]}...")
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        message = request.json['message']
        # Simulação de resposta (substitua por OpenAI em produção)
        response = f"Você perguntou: '{message}'. Estou aprendendo a responder melhor!"
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # Configura a geralçao do codigo nos projetos
openai.api_key = "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"

def gerar_descricao(codigo):
    """Usa IA para gerar descrição, título e tags de um projeto"""
    prompt = f"""
    Analise o seguinte código e me dê um resumo:
    Código:
    {codigo[:1000]}  # limita para evitar excesso
    Responda no formato JSON:
    {{
      "title": "Título do projeto",
      "description": "Resumo curto do projeto",
      "tags": ["tag1", "tag2", "tag3"],
      "code": "Pequeno trecho representativo do código"
    }}
    """
    
    resposta = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    
    try:
        return eval(resposta["choices"][0]["message"]["content"])
    except:
        return {
            "title": "Projeto Desconhecido",
            "description": "Não foi possível gerar descrição.",
            "tags": ["AI"],
            "code": "..."
        }

def carregar_projetos():
    projetos = []
    pasta = "static/projects"
    
    for projeto in os.listdir(pasta):
        caminho = os.path.join(pasta, projeto)
        if os.path.isdir(caminho):
            arquivos = os.listdir(caminho)
            imagem = next((f"projects/{projeto}/{f}" for f in arquivos if f.endswith((".png", ".jpg", ".jpeg"))), "")
            arquivo_codigo = next((os.path.join(caminho, f) for f in arquivos if f.endswith((".py", ".js", ".html", ".css"))), "")
            
            codigo = ""
            if arquivo_codigo:
                with open(arquivo_codigo, "r", encoding="utf-8") as f:
                    codigo = f.read()
            
            dados = gerar_descricao(codigo)
            dados["image"] = imagem
            dados["link"] = f"/static/projects/{projeto}/"
            
            projetos.append(dados)
    
    return projetos

@app.route("/")
def index():
    projetos = carregar_projetos()
    return render_template("index.html", data={"projects": projetos})


if __name__ == '__main__':
    app.run(debug=True)