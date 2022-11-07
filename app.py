import sqlite3
from flask import Flask, redirect, url_for, request, render_template, jsonify, make_response

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
mydb = sqlite3.connect('agenda.db', check_same_thread=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/sucess/<name>/<empresa>/<telefone>/<email>')
def sucess(name, empresa, telefone, email):
    return render_template('sucess.html', name=name, empresa=empresa, telefone=telefone, email=email)



@app.route('/consulta', methods=['POST', 'GET'])
def consulta():
    contatos = []
    if request.method == 'POST':
        nome = request.form['nome']
        empresa = request.form['empresa']
        telefone = request.form['telefone']
        email = request.form['email']
        my_cursor = mydb.cursor()
        if request.form['nome-r'] == '1':
            my_cursor.execute(f"SELECT * FROM tb_contatos where nome like '%{nome}%'")
        elif request.form['nome-r'] == '2':
            my_cursor.execute(f"SELECT * FROM tb_contatos where empresa like '%{empresa}%'")
        elif request.form['nome-r'] == '3':
            my_cursor.execute(f"SELECT * FROM tb_contatos where telefone like '%{telefone}%'")
        elif request.form['nome-r'] == '4':
            my_cursor.execute(f"SELECT * FROM tb_contatos where email like '%{email}%'")

        agenda = my_cursor.fetchall()

        for i in agenda:
            id = i[0]
            name = i[1]
            empresa = i[2]
            telefone = i[3]
            email = i[4]
            data = {'id': id, 'name': name, 'empresa': empresa, 'telefone': telefone, 'email': email}
            contatos.append(data)

        return make_response(
            jsonify(contatos), 200
        )


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        mydb = sqlite3.connect('agenda.db', check_same_thread=False)
        nome = request.form['nome']
        empresa = request.form['empresa']
        telefone = request.form['telefone']
        email = str(request.form['email'])
        my_cursor = mydb.cursor()
        my_cursor.execute(
            f"INSERT INTO tb_contatos (nome, empresa, telefone, email) VALUES (?,?,?,?)",
            (nome, empresa, telefone, email))
        mydb.commit()
        agenda = my_cursor.fetchall()
        mydb.close()
        return redirect(url_for('sucess', name=nome, empresa=empresa, telefone=telefone, email=email))


if __name__ == '__main__':
    app.run()

# app.run(host='0.0.0.0', port=81)
