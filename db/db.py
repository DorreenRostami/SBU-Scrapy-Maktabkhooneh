import os
import sqlite3
from sqlite3 import Error

sql_create_course_table = """ CREATE TABLE IF NOT EXISTS course (
                                        id integer PRIMARY KEY,
                                        title text,
                                        duration text,
                                        instructor text,
                                        organizer text,
                                        price text,
                                        link text,
                                        satisfaction text,
                                        description text
                                    ); """


class DB:
    def __init__(self, db_addr):
        database = os.path.join(db_addr)
        self.conn = self.create_connection(database)
        with self.conn:
            self.create_table(sql_create_course_table)
            self.delete_everything()

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            self.conn.commit()
        except Error as e:
            print(e)

    def create_course(self, course):
        sql = ''' INSERT INTO course(id, title, duration, instructor, organizer, price, link, satisfaction, description)
                  VALUES(?''' + ', ?' * 8 + ')'
        try:
            cur = self.conn.cursor()
            cur.execute(sql, course)
            self.conn.commit()
            return cur.lastrowid
        except Error as e:
            print(e)
            return None

    def update_course(self, course):
        sql = ''' UPDATE course
                    title = ?,
                    duration = ?,
                    instructor = ?,
                    organizer = ?,
                    price = ?,
                    link = ?,
                    satisfaction = ?,
                    description = ?
                 WHERE id = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, course)
        self.conn.commit()

    def delete_everything(self):
        self.conn.cursor().execute('delete from course')
        self.conn.commit()
