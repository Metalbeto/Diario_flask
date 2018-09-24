from peewee import *

db = SqliteDatabase('students.db')

class Student(Model):
    username = CharField(max_length=255, unique=True)
    points   = IntegerField(default=0)

    #Sirve para indicar a
    # peewee a que base de
    # datos pertenece nuestro modelo
    class Meta:
        database = db

students = [
    {'username': 'aldo',
     'points':5},
    {'username': 'pedro',
     'points':8},
    {'username': 'panchita',
     'points':7},
    {'username': 'chonchita',
     'points':9},
    {'username': 'paquita',
     'points':5},
]

def add_students():
    for student in students:
        try:
            Student.create(username=student['username'],
                            points=student['points'])
        except IntegrityError:
            student_record = Student.get(username=student['username'])
            student_record.points = student['points']
            student_record.save()

def top_student():
    student = Student.select().order_by( Student.points.desc() ).get()
    return student

if __name__ == '__main__':
    db.connect()
    db.create_tables([Student], safe=True)
    #add_students()
    print('El mejor estudiante fue: {} con {}'.format( top_student().username, top_student().points ))
