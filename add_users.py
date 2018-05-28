import datamodel as dm
from peewee import IntegrityError
import csv
import configparser

config = configparser.ConfigParser()
config.read('question-config.ini')

dm.db.init(config['db']['dbPath'])
#TODO: User file as script parameter
with open('users.csv', newline='') as csvfile:
    userreader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
    for user in userreader:
        try:
            dm.Citizen.create(citizen_id = user['citizen_id'],
                    question_preference=user['question_type'],
                    collection_mode=user['collection_preference'])
            print(user['citizen_id'] + " correctly inserted")
        except IntegrityError:
            print("Citizen "+user['citizen_id']+ " already exists")
            continue






