from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
#prueba de datos sin servidor
#app.config

#SqlServerAzure
#app.config['SQLALCHEMY_DATABASE_URI'] = (
#    'mssql+pyodbc://<username>:<password>@<server_name>.database.windows.net/<database_name>?driver=ODBC+Driver+17+for+SQL+Server'
#)
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# MYSQL TEST LOCAL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/api_ingreso'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postIdentifier = db.Column(db.Integer)
    commentName = db.Column(db.String(255))
    commentBody = db.Column(db.String(1000))


def obtener_datos():
    api = 'https://jsonplaceholder.typicode.com/comments'
    response = requests.get(api)
    data = response.json()
    campos = ['name','postId','body']
    data = [{clave: valor[clave] for clave in campos} for valor in data]

    data_filtrada = []
    for valor in data:
        nuevo_valor = {}
        for clave in campos:
            nuevo_nombre = ('commentName' if clave == 'name'
                             else 'postIdentifier' if clave == 'postId'
                             else 'commentBody' if clave == 'body'
                             else clave 
                            )
            nuevo_valor[nuevo_nombre] = valor[clave]
        data_filtrada.append(nuevo_valor)

    return data_filtrada



@app.route('/subir_datos', methods=['GET'])
def subir_datos():

    datos = obtener_datos()
    db.create_all()

    for comentario in datos:
        db.session.add(Comment(**comentario))

    db.session.commit()

    return jsonify({"datos obtenidos":datos})
    



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

