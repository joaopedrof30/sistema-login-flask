from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import json
import os
import pandas as pd

app = Flask(__name__)

ARQUIVO_DADOS = 'usuarios.json'

# Função para ler o arquivo JSON (Nosso Banco de Dados sem erro)
def ler_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# Função para salvar no arquivo JSON
def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        # LOGIN DO ADMIN (Acesso Seguro)
        if email == 'admin@gmail.com' and senha == '1234':
            return redirect(url_for('admin'))

        # CADASTRO DE USUÁRIO COMUM
        usuarios = ler_dados()
        usuarios.append({"email": email, "senha": senha})
        salvar_dados(usuarios)
        return "<h1>Sucesso!</h1><p>Cadastro realizado. Acesse /admin para ver os dados.</p>"

    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# --- API PARA O JAVASCRIPT ---
@app.route('/api/usuarios')
def api_usuarios():
    return jsonify(ler_dados())

# --- EXPORTAR PARA EXCEL ---
@app.route('/exportar')
def exportar_excel():
    usuarios = ler_dados()
    if not usuarios:
        return "Nenhum dado para exportar!", 400
    
    df = pd.DataFrame(usuarios)
    caminho_excel = "relatorio_usuarios.xlsx"
    df.to_excel(caminho_excel, index=False)
    return send_file(caminho_excel, as_attachment=True)

# --- DELETAR USUÁRIO ---
@app.route('/deletar/<int:id>')
def deletar(id):
    usuarios = ler_dados()
    if 0 <= id < len(usuarios):
        usuarios.pop(id)
        salvar_dados(usuarios)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)