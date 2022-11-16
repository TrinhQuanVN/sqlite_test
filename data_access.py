import time
import sqlite3
from sqlite3 import Error
import Extension as ex
import pandas as pd
import itertools

class data_access:
    def __init__(self,norm_path=None,work_path=None) -> None:
        self.norm_path = norm_path
        self.work_path = work_path
        
    def success(self,check, if_success_print, if_not):
        if check:
            print(if_success_print)
            return
        print(if_not)

    def execute(self, sql, parameter=None):
        try:
            conn = sqlite3.connect(self.norm_path)
            cur = conn.cursor()
            if isinstance(sql, str):
                # if parameter:
                cur.execute(sql, parameter)  
                # else: cur.execute(sql)
            else:
                for i in range(len(sql)):
                    cur.execute(sql[i], parameter[i]) if parameter else cur.execute(sql[i])
            conn.commit()
            conn.close()
            return 1
        except Error as e:
            print(f"Error occurred in {self.__class__.__name__}.execute: {e}")
            if conn:
                conn.close()
            return 0

    def excecutemany(self, sql, data:tuple):
        try:
            conn = sqlite3.connect(self.norm_path)
            cur = conn.cursor()
            cur.executemany(sql, data)
            conn.commit()
            conn.close()
            return 1
        except Error as e:
            print(f"Error occurred in {self.__class__.__name__}.executemany: {e}")
            if conn:
                conn.close()
            return 0      

    def fetchall(self, sql, parameter=None) -> tuple:
        try:
            conn = sqlite3.connect(self.norm_path)
            cur = conn.cursor()
            if parameter:
                cur.execute(sql, parameter)
            else: cur.execute(sql)
            rows = cur.fetchall()
            conn.close()
            return rows
        except Error as e:
            print(f"Error occurred in {self.__class__.__name__}.fetchall: {e}")
            if conn:
                conn.close()
            return 0 

    def create_database(self):
        sql = ("""CREATE TABLE IF NOT EXISTS norm (
                        id text PRIMARY KEY,
                        name text,
                        unit text
                )""",
                """CREATE TABLE IF NOT EXISTS worker (
                id text PRIMARY KEY,
                name text,
                unit text
                )""",
                """CREATE TABLE IF NOT EXISTS machine (
                        id text PRIMARY KEY,
                        name text,
                        unit text
                )""",
                """CREATE TABLE IF NOT EXISTS material (
                        id text PRIMARY KEY,
                        name text,
                        unit text
                )""",
                """CREATE TABLE IF NOT EXISTS worker_norm (
                        norm_id text,
                        id text,
                        amount real,
                        UNIQUE(norm_id, id),
                        FOREIGN KEY (id) REFERENCES worker (id),
                        FOREIGN KEY (norm_id) REFERENCES norm (id)                       
                )""",
                """CREATE TABLE IF NOT EXISTS machine_norm (
                        norm_id text,
                        id text,
                        amount real,
                        UNIQUE(norm_id, id),
                        FOREIGN KEY (id) REFERENCES machine (id),
                        FOREIGN KEY (norm_id) REFERENCES norm (id)                        
                )""",
                """CREATE TABLE IF NOT EXISTS material_norm (
                        norm_id text,
                        id text,
                        amount real,
                        UNIQUE(norm_id, id),
                        FOREIGN KEY (id) REFERENCES material (id),
                        FOREIGN KEY (norm_id) REFERENCES norm (id) 
                )""",
                        )
        self.success(self.execute(sql),'database created!','Error on da.create_database')


    def insert_norms(self, norms):
        self.success(self.excecutemany('INSERT OR IGNORE INTO norm VALUES(?,?,?)', norms),
                    'norms inserted success','error on da.insert_norms')
                
    def insert_norm(self, norm):
        self.success(self.execute("INSERT OR IGNORE INTO norm(id, name, unit) VALUES(?,?,?)",norm),
                    'norm is inserted', 'error on da.insert_norm')
        
    def get_norm(self, id=None):
        if not id:
            return self.fetchall("SELECT * FROM norm")
        return self.fetchall("SELECT * FROM norm WHERE id = ?", (id,))
                
    def delete_norm(self, id):
        sql = ""
        try:
            conn = sqlite3.connect(self.norm_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM norm WHERE id=?", (id,)) 
            conn.commit()
            conn.close()
            return 1
        except Error as e:
            print(f"Error occurred in {self.__class__.__name__}.delete_norm: {e}")
            if conn:
                conn.close()
            return 0
    
    def update_norm(self, id, norm):
        try:
            conn = sqlite3.connect(self.norm_path)
            cur = conn.cursor()
            cur.execute("UPDATE norm SET name = ?, unit= ? WHERE id=?", (norm['name'], norm['unit'], id)) 
            conn.commit()
            conn.close()
            return 1
        except Error as e:
            print(f"Error occurred in {self.__class__.__name__}.delete_norm: {e}")
            if conn:
                conn.close()
            return 0
        
    def is_norm_exist(self, id):
        if self.get_norm(id):
            return 1
        return 0      

    def get_norm_id(self):
        result = self.fetchall("SELECT id from norm")
        if not result:
            return
        return list(itertools.chain(*result))


    def _insert_norm_from_DataFrame(self,cur,df:pd.DataFrame):
        # từ dự toán lấy ra norm
        dt_norm = df[df.iloc[:,1].map(ex.is_norm)] # cột thứ 1 tìm xem có phải là id_norm
        # insert norm to db
        cur.executemany('INSERT OR IGNORE INTO norm VALUES(?,?,?)',dt_norm.iloc[:,1:-1].values)
        
        # từ dự toán lấy ra worker
        dt_worker = df[df.iloc[:,1].map(ex.is_worker)].drop_duplicates(subset=[df.columns[1]])
        # insert worker to db
        cur.executemany('INSERT OR IGNORE INTO worker VALUES(?,?,?)',dt_worker.iloc[:,1:-1].values)
        
        # từ dự toán lấy ra machine
        dt_machine = df[df.iloc[:,1].map(ex.is_machine)].drop_duplicates(subset=[df.columns[1]])
        # insert worker to db
        cur.executemany('INSERT OR IGNORE INTO machine VALUES(?,?,?)',dt_machine.iloc[:,1:-1].values)    
        
        # từ dự toán lấy ra material
        dt_material = df[df.iloc[:,1].map(ex.is_material)].drop_duplicates(subset=[df.columns[1]])
        # insert worker to db
        cur.executemany('INSERT OR IGNORE INTO material VALUES(?,?,?)',dt_material.iloc[:,1:-1].values)
        
        # từ dự toán lấy ra worker_norm
        dt_worker_norm = df[df.iloc[:,1].map(ex.is_worker)]
        # insert worker_norm to db
        cur.executemany('INSERT OR IGNORE INTO worker_norm VALUES(?,?,?)',dt_worker_norm.iloc[:,[0,1,-1]].values)    
        
        # từ dự toán lấy ra machine_norm
        dt_machine_norm = df[df.iloc[:,1].map(ex.is_machine)]
        # insert machine_norm to db
        cur.executemany('INSERT OR IGNORE INTO machine_norm VALUES(?,?,?)',dt_machine_norm.iloc[:,[0,1,-1]].values)     
        
        # từ dự toán lấy ra material_norm
        dt_material_norm = df[df.iloc[:,1].map(ex.is_material)]
        # insert material_norm to db
        cur.executemany('INSERT OR IGNORE INTO material_norm VALUES(?,?,?)',dt_material_norm.iloc[:,[0,1,-1]].values)             

    def insert_norm_from_excel_path(self,path):
        df = ex.read_excel(path)
        try:
            conn = sqlite3.connect(self.norm_path)
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) from norm')
            last_norm_count = cur.fetchone()
            
            self._insert_norm_from_DataFrame(cur,df)
            
            cur.execute('SELECT COUNT(*) from norm')
            
            print('lastest norm count= ',last_norm_count,' and newest norm count= ',cur.fetchone())
            
            conn.commit()
            conn.close()
            return 1
        except Error as e:
            print(f"Error occurred in {self.__class__.__name__}.insert_norm_from_excel_path: {e}")
            if conn:
                conn.close()
            return 0

def main():
    db = data_access('norm.db')
    db.create_database()
    db.insert_norm_from_excel_path(r'C:\Users\trinh\OneDrive\195 Company\2021\Kim Bảng\Hành chính công\TD_Mot cua huyen.xls')
    

if __name__ == "__main__":
    start = time.time()
    main()
    print('time exe: ', round((time.time()-start)*10**3,2),' ms')

