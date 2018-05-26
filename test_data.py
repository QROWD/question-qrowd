import datamodel as dm
import configparser
from datetime import datetime

def clear_data():
    del_questions = dm.Question.delete()
    del_questions.execute()

    del_trips = dm.Trip.delete()
    del_trips.execute()

    del_citizens = dm.Citizen.delete()
    del_citizens.execute()

def insert_test_citizen(config):
    """Test citizen comes from config. It needs to be linked to a test mobile phone
    """
    test_citizen = dm.Citizen(citizen_id=config['test']['test_citizen_id'],collection_mode='CONTINUOUS',question_preference='SEGMENT')
    test_citizen.save(force_insert=True)
    return test_citizen

def insert_test_trip(test_citizen):
    """ Inserts fake trip to citizen
    """
    test_trip = dm.Trip(citizen_id=test_citizen,start_coordinate='[46.041332, 11.137968]',
            start_address = 'Via Southampton', stop_coordinate = '[46.066857,11.150428]',
            stop_address = 'Via Leipzig',start_timestamp = datetime.strptime('2018-04-12 12:11:50','%Y-%m-%d %H:%M:%S'),
            stop_timestamp=datetime.strptime('2018-04-12 12:21:50','%Y-%m-%d %H:%M:%S'))
    test_trip.save()

def main():
    config = configparser.ConfigParser()
    config.read('question-config.ini')
    clear_data()
    test_citizen = insert_test_citizen(config)
    insert_test_trip(test_citizen)


if __name__ == "__main__": main()
