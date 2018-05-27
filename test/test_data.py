import datamodel as dm
import configparser
from datetime import datetime

def clear_data():
    del_messages = dm.Message.delete()
    del_messages.execute()

    del_questions = dm.Question.delete()
    del_questions.execute()

    del_trips = dm.Trip.delete()
    del_trips.execute()

    del_citizens = dm.Citizen.delete()
    del_citizens.execute()


def insert_test_citizen(config,collection_mode='CONTINUOUS',question_preference='SEGMENT'):
    """Test citizen comes from config. It needs to be linked to a test mobile phone
    """
    test_citizen = dm.Citizen(citizen_id=config['test']['test_citizen_id'],collection_mode=collection_mode,question_preference=question_preference)
    test_citizen.save(force_insert=True)
    return test_citizen

def insert_test_trip(test_citizen):
    """ Inserts fake trip to citizen
    """
    test_trip = dm.Trip(citizen_id=test_citizen,start_coordinate='[46.041332, 11.137968]',
            start_address = 'Via Southampton', stop_coordinate = '[46.066857,11.150428]',
            stop_address = 'Via Leipzig',start_timestamp = datetime.strptime('2018-04-12 12:11:50','%Y-%m-%d %H:%M:%S'),
            stop_timestamp=datetime.strptime('2018-04-12 12:21:50','%Y-%m-%d %H:%M:%S'),
            path = "[ [46.041332, 11.137968], [46.039488, 11.137673], [46.038703, 11.138460], [46.039078, 11.140378], [46.040171, 11.141608], [46.042424, 11.140969], [46.043892, 11.140526], [46.048023, 11.142985], [46.054645, 11.148740], [46.063045, 11.150149], [46.066857, 11.150428] ]")
 
    test_trip.save()

def main():
    config = configparser.ConfigParser()
    config.read('question-config.ini')
    clear_data()
    test_citizen = insert_test_citizen(config)
    insert_test_trip(test_citizen)


if __name__ == "__main__": main()
