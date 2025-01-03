import sqlite3
import psycopg2
from database.exam import Exam
from database.students import Student
from database.room_assignment import RoomAssignment
from database.PostgreSQL.college import PostgerCollege
from database.PostgreSQL.department import PostgerDepartment
from database.PostgreSQL.student import PostgerStudent

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def __init__(self, db_name='exam_proctoring.db', postgername='postgres'):
        self.db_name = db_name
        self.student_db = Student(db_name)
        self.exam_db = Exam(db_name)
        self.room_assignment_db = RoomAssignment(db_name)
        # postgersql
        self.use_postgresql = self.create_database_if_not_exists()
        self.postger_college = PostgerCollege(postgername)
        self.postger_department = PostgerDepartment(postgername)
        self.postger_student = PostgerStudent(postgername)

    def connect(self):
        if self._connection is None:
            try:
                if self.use_postgresql:
                    # Connect to PostgreSQL
                    self._connection = psycopg2.connect(dbname='postgres', user='root', password='', host='localhost', port='5432')
                    print("PostgreSQL Database connection successful")

                # SQLite does not require a host or user/password, just the db file.
                self._connection = sqlite3.connect(self.db_name)
                print("Database connection successful")
            except sqlite3.Error as err:
                print(f"Database connection error: {err}")
                self._connection = None
        return self._connection

    def create_tables(self):
        if self.use_postgresql:
            self.postger_college.create_table()
            self.postger_department.create_table()
            self.postger_student.create_table()

        # Create all tables by calling the create_table method for each class.
        self.student_db.create_table()
        self.exam_db.create_table()
        self.room_assignment_db.create_table()
        print("All tables created if not exist")

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            print("Database connection closed")

    def create_database_if_not_exists(self):
        try:
            connection = psycopg2.connect(dbname='postgres', user='postgres', password='12345678', host='localhost', port='5432')
            connection.autocommit = True  # Enable autocommit for database creation
            cursor = connection.cursor()
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.db_name}'")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f"CREATE DATABASE {self.db_name}")
                print(f"Database {self.db_name} created successfully!")
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"Error creating database: {e}")
            return True
            
# # Example usage
# if __name__ == '__main__':
#     db_manager = DatabaseManager()
#     db_manager.connect()
#     db_manager.create_tables()

#     # Insert some data into the students table
#     # db_manager.student_db.create(StudentName="Ahmed", Number="22160028", College="Computer Science", Level="4", Specialization="CS", ImagePath="/images/ahmed.jpg")
#     # db_manager.student_db.create(StudentName="Ahmed", Number="22160029", College="Computer Science", Level="4", Specialization="CS", ImagePath="/images/ahmed.jpg")
#     # db_manager.student_db.create(StudentName="Ahmed", Number="22160030", College="Computer Science", Level="4", Specialization="CS", ImagePath="/images/ahmed.jpg")
#     # db_manager.student_db.create(StudentName="Ahmed", Number="22160031", College="Computer Science", Level="4", Specialization="AI", ImagePath="/images/ahmed.jpg")

#     # Fetch all students
#     students = db_manager.student_db.last()
#     print("student ",students)

#     # Insert an exam
#     db_manager.exam_db.create(Date="2024-12-06", TimeSlot="10:00 - 12:00", Period="First", Level="2", Specialization="AI", Duration="02:00:00", StudentCount=50)
#     db_manager.exam_db.create(Date="2024-12-07", TimeSlot="10:00 - 12:00", Period="First", Level="4", Specialization="CS", Duration="02:00:00", StudentCount=50)
#     db_manager.exam_db.create(Date="2024-12-08", TimeSlot="10:00 - 12:00", Period="First", Level="3", Specialization="CS", Duration="02:00:00", StudentCount=50)
#     db_manager.exam_db.create(Date="2024-12-09", TimeSlot="10:00 - 12:00", Period="First", Level="2", Specialization="CS", Duration="02:00:00", StudentCount=50)
#     db_manager.exam_db.create(Date="2024-12-10", TimeSlot="10:00 - 12:00", Period="First", Level="1", Specialization="CS", Duration="02:00:00", StudentCount=50)

#     # Fetch all exams
#     exams = db_manager.exam_db.all()
#     print(exams)

#     db_manager.close()
