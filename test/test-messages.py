import sys
import os
sys.path.append('/home/ldig/Research/QROWD/question-qrowd/')

import datamodel as dm
import question_asker as qa
import configparser
import test_data as td

def test_continuous_machine_failure(config):
    td.clear_data()
    test_citizen = td.insert_test_citizen(config,collection_mode='CONTINUOUS')
    test_citizen_data = [
            {
            'tablename': 'locationeventpertime', 
            'presence': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            }, 
            {'tablename': 'accelerometerevent', 
                'presence': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            }, 
            {'tablename': 'gyroscopeevent', 
                'presence': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }
        ]
    test_message = qa.instantiate_message(test_citizen,test_citizen_data,config)
    print(test_message.message_json)
    resp = qa.send_message(test_citizen,test_message,config['iLog'])
    print(resp)

def test_continuous_collection_failure(config):
    td.clear_data()
    test_citizen = td.insert_test_citizen(config,collection_mode='CONTINUOUS')
    test_citizen_data = [
            {
            'tablename': 'locationeventpertime', 
            'presence': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1]
            }, 
            {'tablename': 'accelerometerevent', 
            'presence': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1]
            }, 
            {'tablename': 'gyroscopeevent', 
                'presence': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }
        ]
    test_message = qa.instantiate_message(test_citizen,test_citizen_data,config)
    print(test_message.message_json)
    resp = qa.send_message(test_citizen,test_message,config['iLog'])
    print(resp)

def test_onoff_machine_failure(config):
    td.clear_data()
    test_citizen = td.insert_test_citizen(config,collection_mode='ON-OFF')
    test_citizen_data = [
            {
            'tablename': 'locationeventpertime', 
            'presence': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }, 
            {'tablename': 'accelerometerevent', 
            'presence': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }, 
            {'tablename': 'gyroscopeevent', 
                'presence': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }
        ]
    test_message = qa.instantiate_message(test_citizen,test_citizen_data,config)
    print(test_message.message_json)
    resp = qa.send_message(test_citizen,test_message,config['iLog'])
    print(resp)

def test_onoff_collection_failure(config):
    td.clear_data()
    test_citizen = td.insert_test_citizen(config,collection_mode='ON-OFF')
    test_citizen_data = [
            {
            'tablename': 'locationeventpertime', 
            'presence': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }, 
            {'tablename': 'accelerometerevent', 
            'presence': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }, 
            {'tablename': 'gyroscopeevent', 
                'presence': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }
        ]
    test_message = qa.instantiate_message(test_citizen,test_citizen_data,config)
    print(test_message.message_json)
    resp = qa.send_message(test_citizen,test_message,config['iLog'])
    print(resp)

def main():
    dm.initialize('test-messages.sqlite')
    config = configparser.ConfigParser()
    #TODO: Unwire below
    config.read('../question-config.ini')

    #test_continuous_machine_failure(config)
    #test_continuous_collection_failure(config)
    #test_onoff_machine_failure(config)
    test_onoff_collection_failure(config)


if __name__ == "__main__": main()
