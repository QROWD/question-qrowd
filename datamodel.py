from peewee import *

db = SqliteDatabase('test2.sqlite')

class Citizen(Model):
    citizen_id = CharField(primary_key=True)
    collection_mode = CharField() #CONTINUOUS or ON-OFF
    question_preference = CharField(null=True) #SEGMENT or POINTS

class Trip(Model):
    trip_id = IntegerField(primary_key=True)
    citizen_id = ForeignKeyField(Citizen, backref = 'citizens')
    start_coordinate = CharField()
    start_address = CharField()
    stop_coordinate = CharField()
    stop_address = CharField()
    start_timestamp = DateTimeField()
    stop_timestamp = DateTimeField()
    transportation_mode = CharField(null=True)
    path = TextField(null=True)
    multimodal_trip_id = IntegerField(null=True)

    class Meta:
        database = db

class Stop_answer(Model):
    stop_answer_id = IntegerField(primary_key=True)
    label_machine = CharField()
    label_en = CharField()
    label_it = CharField()

    @classmethod
    def get_machine_label(cls,human_label):
        #TODO: Make indepdendent of number of labels
        result = cls.select().where((cls.label_en == human_label) | cls.label_it == human_label)
        return result


    class Meta:
        database = db

class Question(Model):
    question_id = AutoField(primary_key=True)
    citizen_id = ForeignKeyField(Citizen, backref = 'citizens')
    task_id = CharField()
    trip_id = ForeignKeyField(Trip, backref='questions')
    #All the JSON
    question_json = TextField()
    mode_answer = CharField(null=True)
    start_answer = CharField(null=True)
    stop_answer = ForeignKeyField(Stop_answer,backref='stop-answers',null=True)
    #stop_answer = CharField(null=True)
    question_type = CharField(null=True)

    class Meta:
        database = db

class Transport_mode(Model):
    transport_mode_id = IntegerField(primary_key=True)
    label_en = CharField()
    label_it = CharField()

    class Meta:
        database = db


def main():
    db.connect()
    db.create_tables([Citizen,Trip,Question,Stop_answer,Transport_mode])
    db.close()


if __name__ == "__main__": main()
