from pymongo import MongoClient

# 1. Conectar ao servidor do MongoDB
client = MongoClient("mongodb://root:example@localhost:27017")
db = client["analise_ambiental"]
collection = db["resultados_modelo"]

# 2. Consultar todos os documentos da coleção
documentos = collection.find()

# 3. Exibir todos os documentos encontrados
for documento in documentos:
    print(documento)
