import os
import chromadb

from dotenv import load_dotenv

load_dotenv('.env')

def get_client():
  storage_path = os.getenv('CHROMADB_PATH')
  return chromadb.PersistentClient(path=storage_path)

def add_document(document):
  client = get_client()
  collection = client.get_or_create_collection(name="coverletters")

  try:
    document = client.get_document(document_id=document['id'])
  except chromadb.ChromaClient.DocumentNotFoundError:
    collection.add(document)