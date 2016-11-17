from pymongo import *
from bson.son import SON
import datetime

# MongoDB Connection with PyMongo
class Model:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.daily_planet_db
        
    def getSixFeed(self, inicio):
        save = list(self.db.articulos.aggregate([{ '$sort': {'fecha':1} },{'$project':{ '_id':1, 'imagen':1, 'nombre':1, 'resumen':1 }}]))
        array = list() 
        
        for i in range(inicio, inicio+6):
            if len(save) == i:
                break
            else:
                array.append(save[i])
        return array
        
    def getSingle(self, _id_):
        return self.db.articulos.aggregate([ {'$match': {'_id': {'$eq':_id_}}} ,{ '$project':{'_id':1, 'autor':1, 'fecha':1, 'comentarios':1, 'nombre':1, 'cuerpo':1, 'categoria':1, 'imagen':1} }, {'$lookup':{ 'from':'usuarios', 'localField':'autor', 'foreignField':'_id', 'as':'autor_' }},  {'$project':{'_id':1, 'autor':'$autor_.nombre', 'fecha':1, 'comentarios':1, 'nombre':1, 'cuerpo':1, 'categoria':1, 'imagen':1  }}, { '$unwind': '$autor' } ])
        #return self.db.articulos.find_one({'_id':{'$eq':_id_}})
        #db.articulos.aggregate([ {'$match': {'_id': {'$eq':1}}} ,{ '$project':{'autor':1, 'fecha':1, 'comentarios':1, 'nombre':1, 'cuerpo':1, 'categoria':1} }, {'$lookup':{ 'from':'usuarios', 'localField':'autor', 'foreignField':'_id', 'as':'autor_' }},  {'$project':{'autor':'$autor_.nombre', 'fecha':1, 'comentarios':1, 'nombre':1, 'cuerpo':1, 'categoria':1  }} ])
        
        
    def get_image_username(self,name):
        data = self.db.usuarios.find_one({'nombre':{'$eq':name}},{'_id':0,'avatar':1})
        return data['avatar']
        
    def upload_comentario(self,id_articulo,id_usuario,comentario):
        nombre = self.db.usuarios.find_one({'_id':{'$eq':id_usuario}})['nombre']
        _idcomment = int (self.db.articulos.find_one({'_id':{'$eq':id_articulo}})['n_comment']) + 1
        self.db.articulos.update({'_id':id_articulo},{ '$inc': { 'n_comment': _idcomment }})
        data = {'_id':_idcomment,'nombre':nombre,'cuerpo':comentario,'fecha':datetime.datetime.now(),'respuestas':[] }
        self.db.articulos.update({'_id':id_articulo},{'$push':{'comentarios':data}})
        print(data)
        return data