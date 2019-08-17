import gen_questions as gq
import datamodel as dm
import configparser
from datetime import date


def test_gen_failsafe_question(config):
    template_path = config['templateDir']['questions'] + 'no-trip-detected-question.json'
    test_citizen = dm.Citizen.get_by_id(config['test']['test_citizen_id'])
    test_date = date(2019,8,15)
    trip_number = 0
    q = gq.gen_failsafe_question(template_path,test_citizen,test_date,trip_number)
    print(test_date)
    print(q)


def main():
    config = configparser.ConfigParser()
    config.read('./test-config.ini')
    dm.db.init(config['db']['dbPath'])

    test_gen_failsafe_question(config)

if __name__ == "__main__": main()
