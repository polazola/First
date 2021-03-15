from operator import __add__

from db_executer import Db_executer

db_name = r"C:\Users\cp24\Desktop\Akademia Kodu\Project2\clinic.db"
db = Db_executer(db_name)
print(db.select_all_tasks("patients"))
db.close_conn()  # to w try except


print(__name__)
print(__add__(1, 2))
