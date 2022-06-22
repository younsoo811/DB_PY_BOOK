import pymssql
import tkinter


# conn = pymssql.connect(host="127.0.0.1", database='학사관리시스템', user='younsoo', password='carloveff35',  charset='utf8')
# cursor = conn.cursor()
# tt=cursor.execute('SELECT * FROM Student;')
# tt=cursor.fetchone()
# while tt :
#     print(tt[0])
#     tt=cursor.fetchone()
# conn.close()

window=tkinter.Tk()

window.title("도서 대여 관리 시스템")
window.geometry("640x400+100+100")
window.resizable(False, False)

window.mainloop()