from pymongo import MongoClient

class Connecteur:

    @classmethod
    def connexion(self):
        self.client = MongoClient('mongodb+srv://user:user@promessededon.sw4vx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
        self.db = self.client.Chatbot
        self.col = self.db.Reponses 

    @classmethod
    def deconnexion(cls):
        cls.client.close()

    #Récupère le corpus
    @classmethod
    def get_all_data(cls):
        dic = dict()
        cls.connexion()
        data = list(cls.col.find({}, {'_id': 0}))
        cls.deconnexion()
        dic['intents'] = data
        return dic

    #Insère un nouveau document doc avec un nouveau tag
    @classmethod
    def insert_data(cls, tag, liste_input:list, liste_output:list):
        dic = {}
        dic['tag'] = tag
        dic['liste_input'] = liste_input
        dic['liste_output'] = liste_output
        cls.connexion()
        cls.col.insert_one(dic)
        cls.deconnexion()
        response = {'code': 200, 'message': 'Nouvelles entrées insérées'}
        return response

    #Récupère un document en fonction du tag
    @classmethod
    def get_data(cls, tag):
        cls.connexion()
        data = cls.col.find_one({'tag': tag}, {'_id': 0})
        cls.deconnexion()
        return data

    #Ajoute un ou plusieurs nouveaux input et output (variables de type liste) au document avec le tag désiré
    @classmethod
    def add_data(cls, tag, liste_input:list, liste_output:list):
        cls.connexion()
        if liste_input != None:
            cls.col.update_one({'tag': tag}, {'$push': {'liste_input': {'$each': liste_input}}})
        if liste_output != None:
            mongo_output = cls.col.find_one({'tag': tag})['liste_output']
            if mongo_output[0] == "":
                cls.col.update_one({'tag': tag, 'liste_output': ''}, {'$set': {'liste_output.$': liste_output[0]}})
                if len(liste_output) > 1:
                    cls.col.update_one({'tag': tag}, {'$push': {'liste_output': {'$each': liste_output[1:]}}})
            else:
                cls.col.update_one({'tag': tag}, {'$push': {'liste_output': {'$each': liste_output}}})
        cls.deconnexion()
        response = {'code': 200, 'message': 'Nouvelles entrées insérées'}
        return response

    #Supprime une ou plusieurs input et/ou output du tag désiré (variables de type liste)
    @classmethod
    def delete_in_out_elem(cls, tag, in_elem_to_del:list, out_elem_to_del:list):
        cls.connexion()
        cls.col.update_one({'tag': tag}, {'$pull': {'liste_input': {'$in': in_elem_to_del}, 'liste_output': {'$in': out_elem_to_del}}})
        print('ok')
        cls.deconnexion()
        return 'Suppressions effectuées'


    #Récupère le dictionnaire avec le tag en clé et l'ouput en valeur
    @classmethod
    def get_output_dic(cls):
        cls.connexion()
        data = list(cls.col.find({}, {'_id':0, 'liste_input': 0}))
        cls.deconnexion()
        output_dic = dict()
        for elem in data:
            output_dic[elem['tag']] = elem['liste_output']
        return output_dic

    #Récupère le dictionnaire avec le tag en clé et l'ouput en valeur sur un tag précis
    @classmethod
    def get_tag_output_dic(cls, tag):
        cls.connexion()
        data = cls.col.find_one({'tag': tag}, {'_id':0, 'liste_input': 0})
        cls.deconnexion()
        return data 

# test_add_data = Connecteur.add_data('affirmation', ['test1'], ['test1', 'test2', 'test3'])
#test_delete_in_out_elem = Connecteur.delete_in_out_elem('affirmation', [], ['test1'])
