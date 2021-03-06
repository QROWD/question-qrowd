import gen_questions as gq
import datamodel as dm
import configparser
from datetime import date


def test_gen_failsafe_question(config):
    template_path = config['templateDir']['questions'] + 'no-trip-detected-question-alt.json'
    test_citizen = dm.Citizen.get_by_id(config['test']['test_citizen_id'])
    test_date = date(2019,8,15)
    q = gq.gen_failsafe_question(template_path,'/journeys/ql6/test_trips',test_citizen,test_date)
    print(q)

def test_gen_missing_question(config):
    template_path = config['templateDir']['questions'] + 'missing-trip-question.json'
    test_citizen = dm.Citizen.get_by_id(config['test']['test_citizen_id'])
    test_date = date(2019,8,15)
    q = gq.gen_failsafe_question(template_path,'/journeys/ql6/test_trips',test_citizen,test_date)
    print(q)

def test_gen_trip_question(config):
    template_path = config['templateDir']['questions'] + 'trip-detected-question.json'
    tui_url = config['tui']['tui_url']
    #test_citizen = dm.Citizen.get_by_id(config['test']['test_citizen_id'])
    test_trip = dm.Trip.get_by_id(2) 
    q = gq.gen_trip_question(template_path,tui_url,test_trip)
    print(q)

def test_gen_trip_question_alt(config):
    template_path = config['templateDir']['questions'] + 'trip-detected-question-alt.json'
    tui_url = config['tui']['tui_url']
    #test_citizen = dm.Citizen.get_by_id(config['test']['test_citizen_id'])
    # Set trip id manually from DB
    test_trip = dm.Trip.get_by_id(2) 
    q = gq.gen_trip_question_alt(template_path,tui_url,test_trip)
    print(q)

def main():
    config = configparser.ConfigParser()
    config.read('./test-config.ini')
    dm.db.init(config['db']['dbPath'])

    test_gen_failsafe_question(config)
    test_gen_missing_question(config)
    #test_gen_trip_question_alt(config)

if __name__ == "__main__": main()
