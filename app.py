from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_flash_messages'

# Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))

# --- CONFIGURAÇÃO DO ADMIN ---
ADMIN_EMAIL = "admin@email.com"
ADMIN_SENHA = "123"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Salva a tentativa no banco (como você queria)
        novo = Usuario(email=email, senha=senha)
        db.session.add(novo)
        db.session.commit()
        
        # Verifica se é o Admin tentando entrar
        if email == ADMIN_EMAIL and senha == ADMIN_SENHA:
            return redirect(url_for('admin'))
        
        return "Login realizado! (Usuário comum)"
    
    return render_template('index.html')

@app.route('/admin')
def admin():
    # Aqui pegamos todos do banco para exibir na tabela
    todos = Usuario.query.all()
    return render_template('admin.html', usuarios=todos)

@app.route('/exportar')
def exportar():
    usuarios = Usuario.query.all()
    dados = [{"Email": u.email, "Senha": u.senha} for u in usuarios]
    df = pd.DataFrame(dados)
    df.to_excel("relatorio_admin.xlsx", index=False)
    return "Excel Gerado na pasta do projeto!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)