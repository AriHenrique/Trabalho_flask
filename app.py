import sqlite3
from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
mydb = sqlite3.connect('agenda.db', check_same_thread=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/delete_sucess')
def delete_sucess():
    return render_template('Remove_sucess.html'), 200


@app.route('/delete_error')
def deleteerror_sucess():
    return render_template('error404_sucess.html'), 400


@app.route('/visualizar_remove/<id>/<nome>/<empresa>/<telefone>/<email>')
def visualizar_remove(id, nome, empresa, telefone, email):
    return render_template('remover_visual.html', id=id, nome=nome, empresa=empresa, telefone=telefone, email=email)


@app.route('/visualizar_update/<id>/<name>/<empresa>/<telefone>/<email>')
def visualizar_update(id, name, empresa, telefone, email):
    return render_template('update_visual.html', id=id, nome=name, empresa=empresa, telefone=telefone, email=email)


@app.route('/sucess/<name>/<empresa>/<telefone>/<email>')
def sucess(name, empresa, telefone, email):
    return render_template('sucess.html', name=name, empresa=empresa, telefone=telefone, email=email)


@app.route('/delete', methods=["POST", "DELETE"])
def delete():
    id = request.form['id']
    try:
        cursor = mydb.cursor()
        comando_sql = f"DELETE FROM tb_contatos WHERE id = {id}"
        cursor.execute(comando_sql)
        mydb.commit()
        return redirect(url_for('delete_sucess'))
    except IndexError:
        return redirect(url_for('delete_error'))


@app.route("/update", methods=["POST", "PUT"])
def update():
    id = request.form['id']
    nome = request.form['nome']
    empresa = request.form['empresa']
    telefone = request.form['telefone']
    email = request.form['email']
    cursor = mydb.cursor()
    comando_sql = f"UPDATE tb_contatos SET nome = '{nome}', empresa = '{empresa}', telefone = '{telefone}', email = '{email}' WHERE id = {id}"
    cursor.execute(comando_sql)
    mydb.commit()
    return render_template('update_sucess.html', id=id, name=nome, empresa=empresa, telefone=telefone, email=email)


@app.route('/check_remove', methods=['POST'])
def check_remove():
    mydb = sqlite3.connect('agenda.db', check_same_thread=False)
    id = request.form['id']
    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT * FROM tb_contatos where id like {id}")
    contatos = my_cursor.fetchall()
    if not contatos:
        return render_template('error404_sucess.html'), 400
    else:
        id = contatos[0][0]
        nome = contatos[0][1]
        empresa = contatos[0][2]
        telefone = contatos[0][3]
        email = contatos[0][4]
        return redirect(url_for('visualizar_remove', id=id, nome=nome, empresa=empresa, telefone=telefone, email=email))


@app.route('/check_update', methods=['POST'])
def check_update():
    mydb = sqlite3.connect('agenda.db', check_same_thread=False)
    id = request.form['id']
    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT * FROM tb_contatos where id like {id}")
    contatos = my_cursor.fetchall()
    if not contatos:
        return render_template('error404_sucess.html'), 400
    else:
        id = contatos[0][0]
        nome = contatos[0][1]
        empresa = contatos[0][2]
        telefone = contatos[0][3]
        email = contatos[0][4]
        return redirect(url_for('visualizar_update', id=id, name=nome, empresa=empresa, telefone=telefone, email=email))


@app.route('/consulta', methods=['POST', 'GET'])
def consulta():
    contatos = []
    if request.method == 'POST':
        id = request.form['id']
        nome = request.form['nome']
        empresa = request.form['empresa']
        telefone = request.form['telefone']
        email = request.form['email']
        my_cursor = mydb.cursor()
        if request.form['nome-r'] == '1':
            my_cursor.execute(f"SELECT * FROM tb_contatos where id = {id}")
        elif request.form['nome-r'] == '2':
            my_cursor.execute(f"SELECT * FROM tb_contatos where nome like '%{nome}%'")
        elif request.form['nome-r'] == '3':
            my_cursor.execute(f"SELECT * FROM tb_contatos where empresa like '%{empresa}%'")
        elif request.form['nome-r'] == '4':
            my_cursor.execute(f"SELECT * FROM tb_contatos where telefone like '%{telefone}%'")
        elif request.form['nome-r'] == '5':
            my_cursor.execute(f"SELECT * FROM tb_contatos where email like '%{email}%'")

        agenda = my_cursor.fetchall()
        if not agenda:
            return render_template('error404_sucess.html'), 400
        else:
            lista = []
            for i in agenda:
                id = i[0]
                name = i[1]
                empresa = i[2]
                telefone = i[3]
                email = i[4]
                lista.append([id, name, empresa, telefone, email])

            return render_template('consulta_resultado.html', lista=lista)


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
        return redirect(url_for('sucess', name=nome, empresa=empresa, telefone=telefone, email=email))


if __name__ == '__main__':
    app.run()

# app.run(host='0.0.0.0', port=81)
