from flask import Flask, render_template, url_for, request, jsonify, session
import requests
from clean_message import Pretreatment
from logs.historique import Historisation
import json
from urllib.parse import unquote # nécessite un PIP install en prod

import datetime # pour générer les timestamps de chatlogs
import uuid # créer des strings aléatoires pour les noms des fichiers de chatlogs
import csv # pour créer les fichiers de chatlogs

message_cleaner = Pretreatment()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ChatbotApplication'

@app.route('/')
def index():
    #Chargement de l'historique si il existe
    if 'username' in session:
        historique_chat = Historisation.load_historique(session)
        return render_template('index.html', historique_chat=historique_chat) #Pour le chatbot seul
        # return render_template('index_test.html', historique_chat=historique_chat) #Pour le chatbot intégré au site

    #Créer un fichier historique sinon
    else:
        Historisation.create_historique(session)
        return render_template('index.html') #Pour le chatbot seul
        # return render_template('index_test.html') #Pour le chatbot intégré au site

@app.route('/pretreatment', methods=['GET','POST'])
def pretreatment():
    if request.method == 'POST':
        message = request.form['jsdata']
        message = unquote(message)

        # Envoi de la réponse de user au chatlog :
        Historisation.save_message(session, 'user', message)

        processed_message = message_cleaner.pretreatment(message)
        return json.dumps(processed_message.tolist())


@app.route('/get_tag', methods=['GET', 'POST'])
def get_tag():
    if request.method == 'POST':
        output_int = int(request.form['jsdata'])
        print(output_int)
        tag = message_cleaner.inverse_labelencoding(output_int)

        url = f"http://api:5000/chatbot/get_tag_output_dic?tag={tag}"  #Pour Docker
        # url = f"http://localhost:5000/chatbot/get_tag_output_dic?tag={tag}" #Sans Docker 

        output_reponse = requests.get(url).json()['liste_output'][0]
        
        # Envoi de la réponse du chatbot au chatlog :
        if output_reponse != None :
            Historisation.save_message(session, 'chatbot', output_reponse)

        return json.dumps(output_reponse) 


if __name__ == '__main__':
    app.run(port=5001, debug=True)



