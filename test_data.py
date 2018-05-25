import datamodel as dm
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('question-config.ini')

test_citizen = dm.Citizen(citizen_id=config['test']['test_citizen_id'],collection_mode='CONTINUOUS',question_preference='SEGMENT')

print(test_citizen.save(force_insert=True))

test_trip = dm.Trip(citizen_id=test_citizen,start_coordinate='[46.041332, 11.137968]',
        start_address = 'Via Southampton', stop_coordinate = '[46.066857,11.150428]',
        stop_address = 'Via Leipzig',start_timestamp = datetime.strptime('2018-04-12 12:11:50','%Y-%m-%d %H:%M:%S'),
        stop_timestamp=datetime.strptime('2018-04-12 12:21:50','%Y-%m-%d %H:%M:%S'))
print(test_trip.save())

