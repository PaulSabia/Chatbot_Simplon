import datetime
from urllib.parse import unquote
import csv
import uuid
import codecs

class Historisation:

    @classmethod
    def create_historique(cls, session):
        print('Création de l\'historique...')
        session['username'] = "user"
        session["random_code"] = str(uuid.uuid4())

        # Le code associé à la session utilisateur doit être libre pour créer un nouveau fichier log avec
        code_libre = False
        while code_libre == False :
            path = "./logs/"+session["random_code"]+".csv"
            try :
                with open(path, "r") as f: # Si pas d'erreur à l'ouverture, c'est qu'il y a déjà un log à ce nom
                    print("fichier déjà pris")
                session["random_code"] = str(uuid.uuid4()) # on régénère le code

            except IOError as e: # Si erreur IO, alors le fichier à ce nom n'existe pas et on peut poursuivre
                code_libre = True
        return 'Historique créé'

    @classmethod
    def load_historique(cls, session):
        path = "./logs/"+session["random_code"]+".csv"
        historique_chat = []
        try: 
            with open(path, newline='') as csvfile:  #encoding='ISO-8859-1', 
                reader = csv.reader(csvfile, delimiter='§')
                for rows in reader:
                    historique_chat.append(rows)
        except IOError as e: # Si erreur IO, alors le fichier à ce nom n'existe pas et on peut poursuivre
            print("erreur = ", e)
        print("historique = ", historique_chat)
        return historique_chat

    @classmethod
    def save_message(cls, session, auteur, message):
        list_valid_auteur = ['user', 'chatbot']
        if auteur not in list_valid_auteur:
            raise ValueError("Argument 'auteur' non valide")
        
        message = unquote(message)
        path = "./logs/"+session["random_code"]+".csv"
        with open(path, "a") as f:
            message = message.replace("§","")
            log = str(datetime.datetime.now(tz=None)) + "§" + auteur + "§" + message
            f.write(log+"\n")

        return 'Message enregistré'