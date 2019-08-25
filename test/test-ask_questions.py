import ask_questions as aq
import datamodel as dm
import configparser


def test_ask_practice_question(config,citizen): 
    aq.ask_practice_question(config,citizen)

def test_ask_trip_question(config,citizen):
    pass

def test_ask_no_trip_question(config,citizen):
    pass

def main():
    config = configparser.ConfigParser()
    config.read('./test-config.ini')
    dm.db.init(config['db']['dbPath'])

    test_citizen = dm.Citizen.get_by_id(config['test']['test_citizen_id'])
    print(test_citizen.citizen_id)

    test_ask_practice_question(config,test_citizen)





if __name__ == "__main__": main()
