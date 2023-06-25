import sqlite3

class Database:
    def __init__(self, db_name="notes.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                project_id INTEGER,
                content TEXT,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            )
        ''')
        self.conn.commit()

    def load_projects(self):
        self.cursor.execute('''
            SELECT id, name FROM projects
        ''')
        return self.cursor.fetchall()
    
    def get_note(self, project_id):
        self.cursor.execute('''
            SELECT content FROM notes WHERE project_id = ?
        ''', (project_id,))
        row = self.cursor.fetchone()
        return row[0] if row is not None else ""

    def add_project(self, project_name):
        self.cursor.execute('''
            INSERT INTO projects (name) VALUES (?)
        ''', (project_name,))
        self.conn.commit()

    def add_note(self, project_id, note_content):
        self.cursor.execute('''
            SELECT * FROM notes WHERE project_id = ?
        ''', (project_id,))
        
        result = self.cursor.fetchone()

        if result is None:
            self.cursor.execute('''
                INSERT INTO notes (project_id, content) VALUES (?, ?)
            ''', (project_id, note_content))
        else:
            self.cursor.execute('''
                UPDATE notes SET content = ? WHERE project_id = ?
            ''', (note_content, project_id))
        self.conn.commit()

    def delete_project(self, project_id):
        self.cursor.execute('''
            DELETE FROM projects WHERE id = ?
        ''', (project_id,))
        self.cursor.execute('''
            DELETE FROM notes WHERE project_id = ?
        ''', (project_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()