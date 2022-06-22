from asyncio.windows_events import NULL
import pymssql
import tkinter
import tkinter.ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import datetime
import tkinter.font
today = datetime.date.today()
etday=datetime.timedelta(days=14)

def Msgadd():
    tkinter.messagebox.showinfo("등록 완료", "정상적으로 등록되었습니다.)")

def Msgdel():
    tkinter.messagebox.showinfo("삭제 완료", "삭제가 완료되었습니다.)")

def Msgup():
    tkinter.messagebox.showinfo("수정 완료", "정상적으로 수정되었습니다.)")

def Msgbox():
    tkinter.messagebox.showinfo("찾을 수 없음", "검색 내용을 찾을 수 없습니다\n(다시 입력해주세요)")

def MsgErr():
    tkinter.messagebox.showerror("대여 할 수 없음", "대여 불가능한 고객입니다\n(고객 정보 확인해주세요)")

def MsgErr2():
    tkinter.messagebox.showerror("등록 할 수 없음", "이미 등록된 학번입니다\n(고객 정보 확인해주세요)")

def MsgErr3():
    tkinter.messagebox.showerror("삭제 할 수 없음", "삭제가 불가능한 고객입니다\n(고객 정보 확인해주세요)")

def calc():
    ck=0
    conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
    cursor = conn.cursor()
    stn=entry.get()

    treeview.delete(*treeview.get_children())
    cursor.execute('SELECT stNum, r_startdate, r_enddate, b_num FROM rent;')
    for infom in cursor.fetchall():
        if stn == infom[0]:
            treeview.insert('','end', text="", values=infom, iid="info")
            ck+=1
    if ck==0:
        Msgbox()

    conn.close() 

def del_calc(): #엔트리 입력 초기화
    treeview.delete(*treeview.get_children())
    entry.delete(0, 'end') 
    bookentry.delete(0, 'end')
    conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
    cursor = conn.cursor()

    cursor.execute('SELECT stNum, r_startdate, r_enddate, b_num FROM rent;')

    for infom in cursor.fetchall():
        treeview.insert('','end', text="", values=infom, iid=infom)
        
    conn.close()


#--------------------------반납, 대여-----------------------------

def delete():
    cd=0
    conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
    dcursor = conn.cursor()
    stn=entry.get()
    bstn=bookentry.get()
    print(stn)

    dcursor.execute('SELECT b_rent FROM book WHERE b_num = %s;' , bstn)
    for tt in dcursor.fetchone():
        result = int(str(tt))+1
        cd+=1

    sql="UPDATE book SET b_rent = %s WHERE b_num = %s;"
    val=(str(result), bstn)
    dcursor.execute(sql , val)

    #고객정보 수정, 대여가능 도서수 1 증가
    dcursor.execute('SELECT pos_rent FROM customer WHERE stNum = %s;' , stn)
    for tt in dcursor.fetchone():
        result = int(str(tt))+1
        cd+=1

    sql2="UPDATE customer SET pos_rent=%s WHERE stNum = %s;"
    val2=(str(result), stn)
    dcursor.execute(sql2 , val2)

    #고객정보 수정, 대여 정지 수정(연체일의 2배 정지)
    sql5="SELECT r_overdate FROM rent WHERE stNum=%s and b_num = %s;"
    val5=(stn, bstn)
    dcursor.execute(sql5 , val5)
    for tt in dcursor.fetchone():
        result = int(str(tt))*2
        cd+=1

    sql3="UPDATE customer SET ban_rent=%s WHERE stNum = %s;"
    val3=(str(result), stn)
    dcursor.execute(sql3 , val3)

    #고객번호와 도서코드가 일치하는 대여 항목 지우기
    sql4="DELETE FROM rent WHERE stNum=%s and b_num=%s;"
    val4=(stn, bstn)
    dcursor.execute(sql4 , val4)
    
    conn.commit()
    if cd==3:
        Msgdel()
    else:
        MsgErr3()
    conn.close()


def add():
    conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
    acursor = conn.cursor()
    stn=entry.get()
    btn=bookentry.get()
    sdate=today
    edate=today + etday

    sql="INSERT INTO rent(r_startdate, r_enddate, r_overdate, r_counter, r_counter_ip, stNum, b_num) VALUES(%s, %s, %s, %s, %s, %s, %s);"
    val=(sdate, edate, "0", "4층 대출 반납", "220.66.60.225", stn, btn)
    
    acursor.execute('SELECT pos_rent FROM customer WHERE stNum = %s;' , stn)
    for tt in acursor.fetchone():
        result = int(str(tt))
    acursor.execute('SELECT ban_rent FROM customer WHERE stNum = %s;' , stn)
    for tt in acursor.fetchone():
        result2 = int(str(tt))
    
    #잔여 대여가능 횟수가 있고, 대출금지자가 아니어야지만 도서 대여 가능
    if result>0 and result2==0:
        acursor.execute(sql , val)
        
        #고객의 잔여 대여가능 횟수 1 감소
        acursor.execute('SELECT pos_rent FROM customer WHERE stNum = %s;' , stn)
        for tt in acursor.fetchone():
            result = int(str(tt))-1

        sql2="UPDATE customer SET pos_rent=%s WHERE stNum = %s;"
        val2=(str(result), stn)
        acursor.execute(sql2 , val2)

        #도서의 대여 가능 수량 1 감소
        acursor.execute('SELECT b_rent FROM book WHERE b_num = %s;' , btn)
        for tt in acursor.fetchone():
            result = int(str(tt))-1
            print(result)

        sql="UPDATE book SET b_rent = %s WHERE b_num = %s;"
        val=(str(result), btn)
        acursor.execute(sql , val)

        conn.commit()
        Msgadd()
    else:
        MsgErr()
    conn.close()


#--------------------------------------------------------------------------------
#----------------------------연체자 관리 윈도우-----------------------------------
#--------------------------------------------------------------------------------
def ban_cust():

    def del_cust():  #연체자 정보 보기
        conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()
        
        Rtreeview.delete(*Rtreeview.get_children())
        cursor.execute('SELECT c.stNum, c.c_name, c.phone, c.email, c.ban_rent, r.r_overdate FROM customer as c, rent as r WHERE c.stNum = r.stNum and r.r_overdate <> 0;')
         
        for infom in cursor.fetchall():
            Rtreeview.insert('','end', text="", values=infom, iid=infom)
                
        conn.close()

    def ban_cust2():  #대여 금지자 정보 보기    
        conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()

        cursor.execute('SELECT stNum, c_name, phone, email, ban_rent FROM customer as a WHERE EXISTS (SELECT * FROM customer as b WHERE a.stNum=b.stNum and ban_rent <> 0);')
        
        Rtreeview.delete(*Rtreeview.get_children())
        for infom in cursor.fetchall():
            Rtreeview.insert('','end', text="", values=infom, iid=infom)
                
        conn.close()
    
    def clear():
        Rtreeview.delete(*Rtreeview.get_children())


    global new
    new=Toplevel()

    new.title("연체자 관리")
    new.geometry("700x500+600+500")
    new.resizable(False, False)
    
    new.configure(bg='red')
    dlabel=tkinter.Label(new, text="", width=98, height=33, bg="grey97")
    dlabel.place(x=4, y=5)

    font3=tkinter.font.Font(family="맑은 고딕", size=25, weight="bold")

    mainlf=tkinter.Label(new, text="연체 관리", width=700, height=2, fg="red", bg='grey87', font=font3)
    mainlf.pack(side="top")

    buttonban = tkinter.Button(new, text="연체자 검색", overrelief="solid", width=15, height=2, command=del_cust)
    buttonban.place(x=45, y=385)

    buttonban = tkinter.Button(new, text="대여 금지 고객 검색", overrelief="solid", width=18, height=2, command=ban_cust2)
    buttonban.place(x=200, y=385)

    buttonban = tkinter.Button(new, text="리스트 초기화", overrelief="solid", width=15, height=2, command=clear)
    buttonban.place(x=540, y=385)

    #---------------------------표 만들기---------------------------------------

    Rtreeview=tkinter.ttk.Treeview(new, columns=["1", "2", "3", "4", "5", "6"], displaycolumns=["1", "2", "3", "4", "5", "6"])
    Rtreeview.place(x=40, y=109)

    Rtreeview.column("1", width=90, anchor="center")
    Rtreeview.heading("1", text="고객번호", anchor="center")

    Rtreeview.column("2", width=80, anchor="center")
    Rtreeview.heading("2", text="고객명", anchor="center")

    Rtreeview.column("3", width=120, anchor="center")
    Rtreeview.heading("3", text="연락처", anchor="center")

    Rtreeview.column("4", width=190, anchor="center")
    Rtreeview.heading("4", text="이메일", anchor="center")

    Rtreeview.column("5", width=80, anchor="center")
    Rtreeview.heading("5", text="대여 금지일", anchor="center")

    Rtreeview.column("6", width=60, anchor="center")
    Rtreeview.heading("6", text="연체일", anchor="center")

    Rtreeview["show"]="headings"


#--------------------------------------------------------------------------------
#---------------------------도서 목록 검색 윈도우----------------------------------
#--------------------------------------------------------------------------------
def bookInfo():
    def bif():  #원하는 도서 검색하기
        ck=0
        conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()
        stnum=Bentry.get()
        stn=Bnamen.get()

        Btreeview.delete(*Btreeview.get_children())
        
        cursor.execute('SELECT b_num, b_name, g_num, b_rent FROM book;')
        for infom in cursor.fetchall():
            if stn == infom[1] or stnum == infom[0]:
                gnum=infom[2]
                real=infom
                ck+=1
        if ck==0:
            Msgbox()
            return 0
        else:
            print(gnum)
            Btreeview.insert('','end', text="", values=real, iid=real)

            sql="SELECT g_num, g_name, g_location FROM genre WHERE g_num=%s;"
            val=(gnum)
            cursor.execute(sql, val)
            kk=cursor.fetchall()
            for isa in kk:
                blf3.config(text=str(isa))

        conn.close()

    def re_info():  #도서 전체 목록 다시 보기
        conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()
        cursor.execute('SELECT b_num, b_name, g_num, b_rent FROM book ORDER BY g_num ASC, b_name ASC;')

        Btreeview.delete(*Btreeview.get_children())
        
        for infom in cursor.fetchall():
            Btreeview.insert('','end', text="", values=infom, iid=infom)
        
        blf3.config(text="('장르번호', '장르명', '도서위치')")
                
        conn.close()

    def bookadd():
        count=0
        conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()  
        bnum=Bentry.get()
        bname=Bnamen.get()
        wname=Bentry2.get()
        countB=Bentry3.get()
        genr=Bentry4.get()

        sql="INSERT INTO book(b_num, b_name, b_writer, g_num, b_rent) VALUES(%s, %s, %s, %s, %s);"
        val=(bnum, bname, wname, genr, countB)

        sql2="SELECT b_num FROM book;"
        cursor.execute(sql2)
        num=cursor.fetchone()

        #같은 도서번호가 이미 존재하는지 확인 (중복 등록 방지)
        for con in num:
            if bnum == con:
                count+=1
        if count == 0:
            cursor.execute(sql , val)
            conn.commit()
            Msgadd()
        else:
            MsgErr2()

        conn.close()

    def bdelete():
        conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
        dcursor = conn.cursor()
        bnum=Bentry.get()
        bname=Bnamen.get()

        sql="DELETE FROM book WHERE b_num = %s or b_name = %s;"
        val=(bnum, bname)

        sql2="SELECT b_rent FROM book WHERE b_num = %s or b_name = %s;"
        dcursor.execute(sql2 , val)
        ban=dcursor.fetchone()
        for bren in ban:
            print(bren)
        
        #삭제 가능한 도서가 있는지 확인
        if bren != "0":
            dcursor.execute(sql , val)
            conn.commit()
            Msgdel()
        else:
            Msgbox()

        conn.close()

    def bupdate():
        conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()
        bnum=Bentry.get()
        bname=Bnamen.get()
        wname=Bentry2.get()
        countB=Bentry3.get()
        genr=Bentry4.get()

        cursor.execute('SELECT b_num FROM book;')
        sel=cursor.fetchone()

        #도서번호를 입력하지 않았거나, 이미 존재하는 동일한 도서번호를 입력하면 업데이트 불가 메시지 출력
        if bnum=="" or bnum==sel:
            Msgbox()
        else:
            sql="UPDATE book SET b_num = %s, b_name = %s, b_writer = %s, g_num = %s, b_rent = %s WHERE b_num = %s;"
            val=(bnum, bname, wname, genr, countB, bnum)              
            cursor.execute(sql , val)
            conn.commit()
            Msgup()
        conn.close()
            
    global new
    new=Toplevel()

    new.title("도서 검색")
    new.geometry("700x500+500+400")
    new.resizable(False, False)

    font3=tkinter.font.Font(family="맑은 고딕", size=25, weight="bold")

    mainlf=tkinter.Label(new, text="도서 관리", width=700, height=2, bg='grey87', font=font3)
    mainlf.pack(side="top")

    mainlf2=tkinter.Label(new, text="- 도서 검색은 '도서 번호' 또는 '도서명' 입력을 필요로 합니다 -", bg='grey87')
    mainlf2.place(x=350, y=70)

    Blabelf=tkinter.LabelFrame(new, text="도서 목록 검색", padx=5, pady=20)
    Blabelf.place(x=420, y=100)

    Bstnum=tkinter.Label(Blabelf, text="도서 번호 입력")
    Bstnum.grid(row=0, column=0, sticky="w", pady=5)

    Bentry=tkinter.Entry(Blabelf)
    Bentry.grid(row=0, column=1, pady=5)

    Bstnam=tkinter.Label(Blabelf, text="도서명 입력")
    Bstnam.grid(row=1, column=0, sticky="w", pady=5)

    Bnamen=tkinter.Entry(Blabelf)
    Bnamen.grid(row=1, column=1, pady=5)
    
    Bstnum2=tkinter.Label(Blabelf, text="작가명 입력")
    Bstnum2.grid(row=2, column=0, sticky="w", pady=5)

    Bentry2=tkinter.Entry(Blabelf)
    Bentry2.grid(row=2, column=1, pady=5)

    Bstnum3=tkinter.Label(Blabelf, text="도서 수량 입력")
    Bstnum3.grid(row=3, column=0, sticky="w", pady=5)

    Bentry3=tkinter.Entry(Blabelf)
    Bentry3.grid(row=3, column=1, pady=5)

    Bstnum4=tkinter.Label(Blabelf, text="장르 번호 입력")
    Bstnum4.grid(row=4, column=0, sticky="w", pady=5)

    Bentry4=tkinter.Entry(Blabelf)
    Bentry4.grid(row=4, column=1, pady=5)
    
    Bbutton = tkinter.Button(Blabelf, text="검색", overrelief="solid", width=15, command=bif)
    Bbutton.grid(row=10, column=1, sticky="e", pady=5)

    Bbutton2 = tkinter.Button(Blabelf, text="목록 전체보기", overrelief="solid", width=15, command=re_info)
    Bbutton2.grid(row=10, column=0, pady=5)
    
    nullb=tkinter.Label(Blabelf, text="", height=3)
    nullb.grid(row=11, column=0, sticky="w", pady=5)

    blf=tkinter.Label(new, text="도서 정보 수정 (등록, 삭제, 수정 선택)", width=37, height=2, bg='grey87', relief="ridge")
    blf.place(x=423, y=345)

    blf2=tkinter.Label(new, text=" 도서 위치 정보:                    ", width=20, height=2, bg='grey87', relief="ridge", anchor="w", padx=10)
    blf2.place(x=110, y=105)

    blf3=tkinter.Label(new, text="('장르번호', '장르명', '도서위치')", width=25, height=2, bg='white', relief="ridge", anchor="w", padx=10)
    blf3.place(x=214, y=105)
    
    blf4=tkinter.Label(new, text="총 도서 수: ", width=8, height=2, bg='grey87', relief="ridge", anchor="w", padx=10)
    blf4.place(x=5, y=105)

    blf5=tkinter.Label(new, text="", width=2, height=2, bg='white', relief="ridge", anchor="w", padx=10)
    blf5.place(x=80, y=105)

    b1 = tkinter.Button(Blabelf, text='등록', overrelief="solid", width=15, command=bookadd)
    b1.grid(row=12, column=1, sticky="se")
    b2 = tkinter.Button(Blabelf, text='삭제', overrelief="solid", width=15, command=bdelete)
    b2.grid(row=12, column=0, sticky="se")
    b3 = tkinter.Button(Blabelf, text='수정', overrelief="solid", width=15, command=bupdate)
    b3.grid(row=13, column=1, sticky="se", pady=5)

    #---------------------------표 만들기---------------------------------------

    Btreeview=tkinter.ttk.Treeview(new, columns=["zero", "one", "two", "tree"], displaycolumns=["zero", "one", "two", "tree"], height=15)
    Btreeview.place(x=5, y=145)

    Btreeview.column("zero", width=100, anchor="center")
    Btreeview.heading("zero", text="도서코드", anchor="center")

    Btreeview.column("one", width=135, anchor="center")
    Btreeview.heading("one", text="도서명", anchor="center")

    Btreeview.column("two", width=80, anchor="center")
    Btreeview.heading("two", text="장르번호", anchor="center")

    Btreeview.column("tree", width=90, anchor="center")
    Btreeview.heading("tree", text="잔여 도서 수", anchor="center")

    Btreeview["show"]="headings"

    conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
    cursor = conn.cursor()

    cursor.execute('SELECT b_num, b_name, g_num, b_rent FROM book ORDER BY g_num ASC, b_name ASC;')

    for infom in cursor.fetchall():
        Btreeview.insert('','end', text="", values=infom, iid=infom)


    sql="SELECT count(distinct b_name) FROM book;"
    cursor.execute(sql)
    kk=cursor.fetchone()
    for isa in kk:
        blf5.config(text=str(isa))
    
    conn.close()


#--------------------------------------------------------------------------------
#--------------------------------고객 목록 윈도우-----------------------------------
#--------------------------------------------------------------------------------
def custlist():
    def cif():  #원하는 고객 검색하기
        ck=0
        conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()
        stname=Cnamen.get() #이름 정보 가져오기
        stnum=Centry.get()  #학번 정보 가져오기

        Ctreeview.delete(*Ctreeview.get_children())
        cursor.execute('SELECT stNum, c_name, phone, pos_rent FROM customer;')
        for infom in cursor.fetchall():
            if stnum == infom[0] or stname == infom[1]:
                real=infom
                ck+=1
        if ck==0:
            Msgbox()
            return 0
        
        Ctreeview.insert('','end', text="", values=real, iid="cust_info")
        conn.close()

    def cre_info():  #고객 전체 목록 다시 보기
        conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()
        cursor.execute('SELECT stNum, c_name, phone, pos_rent FROM customer;')

        Ctreeview.delete(*Ctreeview.get_children())
        for infom in cursor.fetchall():
            Ctreeview.insert('','end', text="", values=infom, iid=infom)
    
        Centry.delete(0, 'end')
        Cnamen.delete(0, 'end')
        phonen.delete(0, 'end')
        mailen.delete(0, 'end')
                
        conn.close()

    def cdelete():
        conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
        dcursor = conn.cursor()
        stnum=Centry.get()
        stname=Cnamen.get()

        sql="DELETE FROM customer WHERE stNum = %s or c_name = %s;"
        val=(stnum, stname)

        sql2="SELECT ban_rent FROM customer WHERE stNum = %s or c_name = %s;"
        dcursor.execute(sql2 , val)
        ban=dcursor.fetchone()
        for bren in ban:
            print(bren)
        sql3="SELECT pos_rent FROM customer WHERE stNum = %s or c_name = %s;"
        dcursor.execute(sql3 , val)
        boolr=dcursor.fetchone()
        for boren in boolr:
            print(boren)
        
        #연체자 혹은 도서대여중인 고객인지 확인
        if bren == "0" and (boren == "5" or boren == "20"):
            dcursor.execute(sql , val)
            Msgdel()
        else:
            MsgErr3()

        conn.commit()
        conn.close()

    def cadd():
        count=0

        conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()
        stnum=Centry.get()
        stname=Cnamen.get()
        phone=phonen.get()
        mail=mailen.get()

        sql="INSERT INTO customer(stNum, c_name, phone, email, ban_rent, pos_rent) VALUES(%s, %s, %s, %s, %s, %s);"
        val=(stnum, stname, phone, mail, "0", "5")

        sql2="SELECT stNum FROM customer;"
        cursor.execute(sql2)
        num=cursor.fetchone()

        #같은 학번이 이미 존재하는지 확인 (중복 등록 방지)
        for con in num:
            if stnum == con:
                count+=1
        if count == 0:
            cursor.execute(sql , val)
            conn.commit()
            Msgadd()
        else:
            MsgErr2()

        conn.close()

    def cupdate():
        conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()
        stnum=Centry.get()
        stname=Cnamen.get()
        phone=phonen.get()
        mail=mailen.get()

        sql="UPDATE customer SET c_name = %s, phone = %s, email = %s WHERE stNum = %s;"
        val=(stname, phone, mail, stnum)
        cursor.execute(sql , val)

        conn.commit()
        Msgup()
        conn.close()

    global new
    new=Toplevel()

    new.title("고객 검색")
    new.geometry("700x500+500+300")
    new.resizable(False, False)

    font3=tkinter.font.Font(family="맑은 고딕", size=25, weight="bold")
    font4=tkinter.font.Font(size=12, weight="bold")

    mainlf=tkinter.Label(new, text="고객 관리", width=700, height=2, bg='grey87', font=font3)
    mainlf.pack(side="top")

    mainlf2=tkinter.Label(new, text="- 고객 검색은 '고객 번호' 또는 '고객 이름' 입력을 필요로 합니다 -", bg='grey87')
    mainlf2.place(x=340, y=70)

    Clabelf=tkinter.LabelFrame(new, text="고객 목록 검색", padx=10, pady=20)
    Clabelf.place(x=395, y=100)

    Cstnum=tkinter.Label(Clabelf, text="고객 번호 입력 ")
    Cstnum.grid(row=0, column=0, sticky="w", pady=5)

    Centry=tkinter.Entry(Clabelf)
    Centry.grid(row=0, column=1, pady=5)

    Cnamelb=tkinter.Label(Clabelf, text="고객 이름 입력 ")
    Cnamelb.grid(row=1, column=0, sticky="w", pady=5)

    Cnamen=tkinter.Entry(Clabelf)
    Cnamen.grid(row=1, column=1, pady=5)

    phonelb=tkinter.Label(Clabelf, text="전화번호  입력 ")
    phonelb.grid(row=2, column=0, sticky="w", pady=5)

    phonen=tkinter.Entry(Clabelf)
    phonen.grid(row=2, column=1, pady=5)

    maillb=tkinter.Label(Clabelf, text="메일 주소 입력 ")
    maillb.grid(row=3, column=0, sticky="w", pady=5)

    mailen=tkinter.Entry(Clabelf)
    mailen.grid(row=3, column=1, pady=5)   

    Cbutton = tkinter.Button(Clabelf, text="검색", overrelief="solid", width=15, command=cif)
    Cbutton.grid(row=10, column=1, sticky="e", pady=5)

    Cbutton2 = tkinter.Button(Clabelf, text="항목 초기화", overrelief="solid", width=15, command=cre_info)
    Cbutton2.grid(row=10, column=0, sticky="w", pady=5)

    nulllb=tkinter.Label(Clabelf, text="", height=5)
    nulllb.grid(row=11, column=0, sticky="w", pady=5)

    relf=tkinter.Label(new, text="고객 정보 수정 (등록, 삭제, 수정 선택)", width=37, height=2, bg='grey87', relief="ridge")
    relf.place(x=400, y=345)

    c1 = tkinter.Button(Clabelf, text='등록', overrelief="solid", width=15, command=cadd)
    c1.grid(row=12, column=1, sticky="se")
    c2 = tkinter.Button(Clabelf, text='삭제', overrelief="solid", width=15, command=cdelete)
    c2.grid(row=12, column=0, sticky="se")
    c3 = tkinter.Button(Clabelf, text='수정', overrelief="solid", width=15, command=cupdate)
    c3.grid(row=13, column=1, sticky="se", pady=5)

    costla=tkinter.Label(new, text="연체자 관리하기", width=14, height=3, fg="red", bg='grey87', relief="ridge", anchor="n", pady=13, font=font4)
    costla.place(x=225, y=382)

    buttonC = tkinter.Button(new, text="연체자 목록", overrelief="solid", width=15, height=2, command=ban_cust)
    buttonC.place(x=240, y=422)

    #---------------------------표 만들기---------------------------------------

    Ctreeview=tkinter.ttk.Treeview(new, columns=["zero", "one", "two", "tree"], displaycolumns=["zero", "one", "two", "tree"], height=12)
    Ctreeview.place(x=20, y=109)

    Ctreeview.column("zero", width=90, anchor="center")
    Ctreeview.heading("zero", text="고객번호", anchor="center")

    Ctreeview.column("one", width=80, anchor="center")
    Ctreeview.heading("one", text="고객명", anchor="center")

    Ctreeview.column("two", width=100, anchor="center")
    Ctreeview.heading("two", text="연락처", anchor="center")

    Ctreeview.column("tree", width=80, anchor="center")
    Ctreeview.heading("tree", text="잔여 대여", anchor="center")

    Ctreeview["show"]="headings"

    conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
    cursor = conn.cursor()

    cursor.execute('SELECT stNum, c_name, phone, pos_rent FROM customer;')

    for infom in cursor.fetchall():
        Ctreeview.insert('','end', text="", values=infom, iid=infom)
    
    conn.close()

#---------------------------------함수 끝!---------------------------------


#--------------------------메인, 대여중인 고객 검색--------------------------

window=tkinter.Tk()
window.title("도서 대여 관리 시스템")
window.geometry("700x500+400+200")
window.resizable(False, False)

font=tkinter.font.Font(family="맑은 고딕", size=25, weight="bold")
font2=tkinter.font.Font(size=12, weight="bold")
font3=tkinter.font.Font(size=12, weight="bold")

mainlf=tkinter.Label(window, text="안양대 도서 대여 관리 시스템", width=700, height=2, bg='Slategray1', font=font)
mainlf.pack(side="top")

mainlf2=tkinter.Label(window, text="- 대여 검색은 '고객번호' 입력을 필요로 합니다 -", bg='Slategray1')
mainlf2.place(x=425, y=70)

mainlf2=tkinter.Label(window, text="", width=700, height=100, bg='RoyalBlue4')
mainlf2.pack(side="bottom")

labelf=tkinter.LabelFrame(window, text="대여 목록 설정", padx=5, pady=20, fg='white', bg='RoyalBlue4', font=font2)
labelf.place(x=415, y=100)

stnum=tkinter.Label(labelf, text="   고객번호 입력    ", bg='Slategray1', relief="ridge")
stnum.grid(row=0, column=0)

entry=tkinter.Entry(labelf)
entry.grid(row=0, column=1, sticky="w")

nullnum=tkinter.Label(labelf, text="", bg='RoyalBlue4')
nullnum.grid(row=1, column=0, sticky="w")

booknum=tkinter.Label(labelf, text="   도서코드 입력    ", bg='Slategray1', relief="ridge")
booknum.grid(row=2, column=0)

bookentry=tkinter.Entry(labelf)
bookentry.grid(row=2, column=1, sticky="w")

nullnum2=tkinter.Label(labelf, text="", bg='RoyalBlue4')
nullnum2.grid(row=3, column=0, sticky="w")

button = tkinter.Button(labelf, text="검색", overrelief="solid", width=15, command=calc)
button.grid(row=4, column=1, sticky="e")

rest = tkinter.Button(labelf, text="항목 초기화", overrelief="solid", width=15, command=del_calc)
rest.grid(row=4, column=0, sticky="w")

nullnum3=tkinter.Label(labelf, text="", height=10, bg='RoyalBlue4')
nullnum3.grid(row=5, column=0, sticky="w")

relf=tkinter.Label(window, text="대여 목록 수정 (대여, 반납 선택)", width=37, height=2, bg='Slategray1', relief="ridge")
relf.place(x=420, y=345)

b1 = tkinter.Button(labelf, text='반납', overrelief="solid", width=15, command=delete)
b1.grid(row=11, column=1, sticky="se")
b1 = tkinter.Button(labelf, text='대여', overrelief="solid", width=15, command=add)
b1.grid(row=11, column=0, sticky="se")

bookla=tkinter.Label(window, text="도서 목록 보러 가기                              ", width=35, height=2, fg="blue", bg='skyblue', relief="ridge")
bookla.place(x=160, y=365)

buttonB = tkinter.Button(window, text="도서 목록", overrelief="solid", width=15, command=bookInfo)
buttonB.place(x=290, y=370)

costla=tkinter.Label(window, text="고객 목록 보러 가기                              ", width=35, height=2, fg="blue", bg='skyblue', relief="ridge")
costla.place(x=160, y=415)

buttonC = tkinter.Button(window, text="고객 목록", overrelief="solid", width=15, command=custlist)
buttonC.place(x=290, y=420)

costla=tkinter.Label(window, text="연체자 관리하기", width=14, height=3, fg="red", bg='skyblue', relief="ridge", anchor="n", pady=13, font=font3)
costla.place(x=10, y=365)

buttonC = tkinter.Button(window, text="연체자 목록", overrelief="solid", width=15, height=2, command=ban_cust)
buttonC.place(x=25, y=405)

#---------------------------표 만들기---------------------------------------

treeview=tkinter.ttk.Treeview(window, columns=["zero", "one", "two", "tree"], displaycolumns=["zero", "one", "two", "tree"], height=11)
treeview.place(x=10, y=109)

treeview.column("zero", width=100, anchor="center")
treeview.heading("zero", text="고객번호", anchor="center")

treeview.column("one", width=100, anchor="center")
treeview.heading("one", text="대여일", anchor="center")

treeview.column("two", width=100, anchor="center")
treeview.heading("two", text="반납일", anchor="center")

treeview.column("tree", width=100, anchor="center")
treeview.heading("tree", text="도서코드", anchor="center")

treeview["show"]="headings"

conn = pymssql.connect(host="127.0.0.1", database='도서대여관리', user='younsoo', password='carloveff35',  charset='utf8')
cursor = conn.cursor()

cursor.execute('SELECT stNum, r_startdate, r_enddate, b_num FROM rent;')

for infom in cursor.fetchall():
    treeview.insert('','end', text="", values=infom, iid=infom)
    
conn.close()

window.mainloop()