import sqlite3


class Database:

    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()
        
    def get_user_subjects(self, user_id):
            data = self.select(
                'SELECT * FROM subjects WHERE userId=? ORDER BY subjectId ASC', [user_id])
            return [{
                'subjectId': d[0],
                'subjectName': d[1],
                'description': d[2]
            } for d in data]
            
    def get_user_num_subjects(self, user_id):
        data = self.select('SELECT COUNT(*) FROM subjects WHERE userId=?',[user_id])
        return data[0][0]
  

    def create_user(self, name, username, encrypted_password):
        self.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                     [name, username, encrypted_password])
        
    def delete_subject(self, subject_id):
        print(subject_id)
        self.execute('DELETE FROM subjects WHERE subjectId = ?',[subject_id])
        
    def create_subject(self, subjectName, description, userId, isUserCreated):
        self.execute('INSERT INTO subjects (subjectName, description, userId, isUserCreated) VALUES (?, ?, ?, ?)',
                     [subjectName, description, userId, isUserCreated])

    def get_user(self, email):
        data = self.select('SELECT * FROM users WHERE email=?', [email])
        if data:
            d = data[0]
            return {
                'id':d[0],
                'name': d[1],
                'email': d[2],
                'password': d[3]
            }
        else:
            return None
        
    def get_subject(self, subject_id):
        data = self.select(
            'SELECT * FROM subjects WHERE subjectId=?', [subject_id])
        if data:
            d = data[0]
            return {
                'subjectId': d[0],
                'subjectName': d[1],
                'description': d[2]
            }
        else:
            return None
        
    def create_subject_notes(self, question, answer, subject_id):
        self.execute('INSERT INTO notes (question, answer, subjectId) VALUES (?, ?, ?)',
                     [question, answer, subject_id])

    def delete_note(self, note_id):
        self.execute('DELETE FROM notes WHERE notetId = ?', [note_id])

    def get_subject_notes(self, subject_id):
        data = self.select(
            'SELECT * FROM notes WHERE subjectId=? ORDER BY notetId ASC', [subject_id])
        return [{
            'notetId': d[0],
            'question': d[1],
            'answer': d[2],
            'subjectId': d[3]
        } for d in data]

    def close(self):
        self.conn.close()
