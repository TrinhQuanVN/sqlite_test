import sqlite3
from sqlite3 import Error
import Extension as ex
class data_access:
    def __init__(self,norm_path=None,work_path=None) -> None:
        self.norm_path = norm_path
        self.work_path = work_path
        
        
    def create_database(self):
        try:
            conn = sqlite3.connect(self.norm_path)
            cur = conn.cursor()
            
            # create tables
            cur.execute("""CREATE TABLE IF NOT EXISTS norm (
                        id text PRIMARY KEY,
                        name text,
                        unit text
                        )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS worker (
                        id text PRIMARY KEY,
                        name text,
                        unit text
                        )""")            
            cur.execute("""CREATE TABLE IF NOT EXISTS machine (
                        id text PRIMARY KEY,
                        name text,
                        unit text
                        )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS material (
                        id text PRIMARY KEY,
                        name text,
                        unit text
                        )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS worker_norm (
                        id text,
                        norm_id text,
                        amount real,
                        FOREIGN KEY (id) REFERENCES worker (id),
                        FOREIGN KEY (norm_id) REFERENCES norm (id)                       
                        )""") 
            cur.execute("""CREATE TABLE IF NOT EXISTS machine_norm (
                        id text,
                        norm_id text,
                        amount real,
                        FOREIGN KEY (id) REFERENCES machine (id),
                        FOREIGN KEY (norm_id) REFERENCES norm (id)                        
                        )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS material_norm (
                        id text,
                        norm_id text,
                        amount real,
                        FOREIGN KEY (id) REFERENCES material (id),
                        FOREIGN KEY (norm_id) REFERENCES norm (id) 
                        )""") 
            conn.commit()   
            conn.close()                                           
        except Error as e:
            print(f"Error occurred in {self.__class__.__name__}.create_database: {e}")
            if conn:
                conn.close()
                
    def insert_norm(self, norm):
        try:
            conn = sqlite3.connect(self.norm_path)
            cur = conn.cursor()
            cur.execute("INSERT INTO norm(id, name, unit) VALUES(?,?,?)", norm) 
            conn.commit()
            conn.close()
        except Error as e:
            print(f"Error occurred in {self.__class__.__name__}.insert_norm: {e}")
            if conn:
                conn.close()
            return 0
        
    def get_norm(self, id=None):
        
        try:
            conn = sqlite3.connect(self.norm_path)
            cur = conn.cursor()
            if not id:
                cur.execute("SELECT * FROM norm")
                rows = cur.fetchall()
            else:
                cur.execute("SELECT * FROM norm where id=?", (id,))
                rows = cur.fetchone()
            conn.close()
            if rows:
                return rows
        except Error as e:
            print(f"Error occurred in {self.__class__.__name__}.select_norm: {e}")
            if conn:
                conn.close()
            return 0        

    def delete_norm(self, id):
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

    # def get_item(self, table,select=['*'], **kwargs) -> tuple:
    #     """_summary_

    #     Args:
    #         table (str): what table to get
    #         like = True : select with like if True if False select with =
    #         select = [] : what parameter to select in sql query
    #         key = [] key to search
    #         value = () go with key
    #     Returns:
    #         _type_: tuple
    #     """
    #     if 'key' in kwargs:
    #         sql = 'SELECT {} FROM {} WHERE '.format(','.join(select),table)
    #         for key in kwargs['key']:
    #             sql += f'{key} = ? and '
    #         sql = sql[:-4]
    #     else:
    #         sql = 'SELECT {} FROM {}'.format(','.join(select),table)
    #     try:
    #         conn = sqlite3.connect(self.norm_path)
    #         cur = conn.cursor()
    #         cur.execute(sql, kwargs['value']) 
    #         rows = cur.fetchone()
    #         conn.close()
    #         if rows:
    #             return rows
    #     except Error as e:
    #         print(f"Error occurred in {self.__class__.__name__}.get_item: {e}")
    #         if conn:
    #             conn.close()
    #         return 0 

def main():
    db = data_access('norm.db')
    db.create_database()
    # db.insert_norm(('AB.12345','cong viec nay tao lam','m3'))
    # db.insert_norm(('AB.11111','cong viec nay tao lam 2 ','m3'))  
    # norm = db.get_norm('AB.11111')
    # print(norm)
    # db.update_norm('AB.12345',{'name': 'trinh tien quan','unit': 'person'}) 
    # db.insert_norm(('AB.12345','cong viec nay tao lam','m3'))
    # values = ex.read_excel('D:\Python\QuanProject\qlcl project git\qlcl_project\PLHĐ nha thanh tra Kim Bang 2022.xls')
    # for row in values:
    #     if db.get_norm(row[0]):
    #         continue
    #     if ex.is_norm(row[1]):
    #         db.insert_norm(row[1:4])

        # if ex.is_worker(row[1]):
        #     if not db.get_norm('worker') or not db.get_norm('worker',id=row[1]):
        #         db.insert_norm('worker',Models.worker(*row[1:4]))
        #     db.insert_norm('worker_norm',Models.worker_norm(row[0],row[1],row[-1]))
            
        # elif ex.is_norm(row[0]) and ex.is_machine(row[1]) or ex.is_dif_machine(row[1]):
        #     if not db.get_norm('machine') or not db.get_norm('machine',id=row[1]):
        #         db.insert_norm('machine',Models.machine(*row[1:4]))
        #     db.insert_norm('machine_norm',Models.machine_norm(row[0],row[1],row[-1]))

        # elif ex.is_norm(row[0]) and ex.is_material(row[1]) or ex.is_dif_material(row[1]):
        #     if not db.get_norm('material') or not db.get_norm('material',id=row[1]):
        #         db.insert_norm('material',Models.material(*row[1:4]))
        #     db.insert_norm('material_norm',Models.material_norm(row[0],row[1],row[-1]))
    # a = db.get_item('norm',select=['name','unit'],key=['id','name'],value=('AB.12345','trinh tien quan'))
    # print(a)
    a = db.get_norm()
    print(a)
if __name__ == "__main__":
    main()

