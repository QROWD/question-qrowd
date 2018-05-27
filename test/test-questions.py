import sys
import os
sys.path.append('/home/ldig/Research/QROWD/question-qrowd/')

import datamodel as dm
import question_asker as qa
import question_gen as qg
import configparser
import test_data as td

def test_segment_question(config):
    td.clear_data()
    test_citizen = td.insert_test_citizen(config,collection_mode='CONTINUOUS',question_preference='SEGMENT')
    test_trip = td.insert_test_trip(test_citizen)
    qa.process_questions(config)

def test_points_question(config):
    td.clear_data()
    test_citizen = td.insert_test_citizen(config,collection_mode='CONTINUOUS',question_preference='POINTS')
    test_trip = td.insert_test_trip(test_citizen)
    qa.process_questions(config)

def main():
    dm.initialize('test-questions.sqlite')
    config = configparser.ConfigParser()
    #TODO: Unwire below
    config.read('../question-config.ini')

    #test_segment_question(config)
    test_points_question(config)


if __name__ == "__main__": main()
