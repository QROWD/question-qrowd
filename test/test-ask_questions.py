import ask_questions as aq
import datamodel as dm
import configparser
from datetime import datetime


def test_ask_practice_question(config,citizen): 
    aq.ask_practice_question(config,citizen)

def test_ask_failsafe_question(config,citizen,dt): 
    aq.ask_failsafe_question(config,citizen,dt)

def test_create_db_question(config):
    test_trip = dm.Trip.get_by_id(2) 
    question = aq.create_db_question(config,test_trip)
    print(question)
    # Assert
    q = dm.Question.get_or_none(dm.Question.trip_id==test_trip.trip_id)
    print(q)
    

def test_ask_trip_question_alt(config,citizen):
    pass

def test_ask_no_trip_question(config,citizen):
    pass

def main():
    config = configparser.ConfigParser()
    config.read('./test-config.ini')
    dm.db.init(config['db']['dbPath'])

    test_citizen = dm.Citizen.get_by_id(config['test']['test_citizen_id'])
    print(test_citizen.citizen_id)

    #test_ask_practice_question(config,test_citizen)
    test_ask_failsafe_question(config,test_citizen,datetime(2019,8,15))

    #test_create_db_question(config)





if __name__ == "__main__": main()
