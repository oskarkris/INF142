import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
import certifi
import csv

# Get you password from .env file
password = os.environ.get("password")
username = "okr014"
clusterName = "INFO142-cluster"
#print(password,username,clusterName)

# Connect to you cluster
client = MongoClient('mongodb+srv://' + username + ':' + password + '@' + clusterName + '.ziczy.mongodb.net/INF142DB?retryWrites=true&w=majority',tlsCAFile=certifi.where())
database = client['Team_Network_Tactics']
champ_collection = database['Champions']
game_history_collection = database['Game_History']

for x in champ_collection.find({},{'_id': 0}):
    print(x)
#importing from csv file to mongodb
def manage_db_champs():
    with open('some_champs.txt', 'r') as csvfile:
        header = ['Name', 'Rock', 'Paper', 'Scissor']
        reader = csv.reader(csvfile)
        for row in reader:
            doc={}
            for n in range(0,len(header)):
                doc[header[n]] = row[n]
            champ_collection.delete_one(doc)
            champ_collection.insert_one(doc)
