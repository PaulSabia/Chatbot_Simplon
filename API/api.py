from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from connecteur import Connecteur
import json

#pip install aiofiles

api = FastAPI()

#Autorise les transfert de fichier avec Javascript
api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Récupère toute la data de la base
@api.get('/chatbot/get_all_data')
async def get_all_data():
    data = Connecteur.get_all_data()
    return jsonable_encoder(data)

#Récupère un document en fonction du tag
@api.get('/chatbot/get_data')
async def get_data(tag: str=None):
    data = Connecteur.get_data(tag)
    return jsonable_encoder(data)

@api.get('/chatbot/get_output_dic')
async def get_output_dic():
    output_dic = Connecteur.get_output_dic()
    return jsonable_encoder(output_dic)

@api.get('/chatbot/get_tag_output_dic')
async def get_tag_output_dic(tag: str=None):
    data = Connecteur.get_tag_output_dic(tag)
    return jsonable_encoder(data)

#Modèle
@api.get('/chatbot/model')
async def get_model():
    json_model = json.load(open("./modeljs_final/model.json"))
    return jsonable_encoder(json_model)

#Poids du modèle
@api.get('/chatbot/group1-shard1of1.bin')
async def load_shards():
    path_file = f"./modeljs_final/group1-shard1of1.bin"
    return FileResponse(path=path_file)

#Si upload=False insère un nouveau document doc avec un nouveau tag
#Si upload=True ajoute un ou plusieurs nouveaux input et output (variables de type liste) au document avec le tag désiré
@api.post('/chatbot/post_data')
async def insert_data(tag: str=None, input_bot: list=None, ouput_bot: list=None, upload: bool=True):
    if upload==True:
        response = Connecteur.add_data(tag, input_bot, ouput_bot)
    else:
        response = Connecteur.insert_data(tag, input_bot, ouput_bot)
    return jsonable_encoder(response)

if __name__ == '__main__':
    uvicorn.run('api:api', host="127.0.0.1", port=5000, reload=True)