'''
- 안양문고 관리 ERP 시스템
- 6조 구성원    :   김승호, 오정훈, 김연수, 김재경, 오지연, 곽동현, 박세준
- 저작자        :   김연수 (DB-김승호)
- 최종 작성일    :   2022.12.10 (v1.70)

- 구조          :   로그인 메소드(로그인 페이지 구현)
                    메인 메소드(메인 페이지 구현)
                    메시지 메소드(안내 메시지 구현)

-설계언어        : 파이썬

-tkinter        : pymssql (MS SQL SERVER 연결)
                tkinter (GUI 구현)
                datetime (시스템 날짜 추출)
                matplotlib (그래프 사용)
'''

from asyncio.windows_events import NULL
import pymssql
import tkinter
import tkinter.ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import datetime
import tkinter.font

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.widgets import CheckButtons
import pandas as pd
import numpy as np

def Msgadd():
    tkinter.messagebox.showinfo("등록 완료", "정상적으로 등록되었습니다.")

def Msgbuy():
    tkinter.messagebox.showinfo("주문 완료", "정상적으로 주문되었습니다.")

def Msgdel():
    tkinter.messagebox.showinfo("삭제 완료", "삭제가 완료되었습니다.")

def Msgre():
    tkinter.messagebox.showinfo("환불 완료", "환불 처리되었습니다.")

def Msgup():
    tkinter.messagebox.showinfo("수정 완료", "정상적으로 수정되었습니다.")

def Msgbox():
    tkinter.messagebox.showinfo("찾을 수 없음", "검색 내용을 찾을 수 없습니다\n(다시 입력해주세요)")

def MsgErr():
    tkinter.messagebox.showerror("주문 할 수 없음", "주문 불가능한 코드입니다\n(주문 정보 확인해주세요)")

def MsgErr2():
    tkinter.messagebox.showerror("등록 할 수 없음", "이미 등록된 정보입니다\n(리스트를 확인해주세요)")

def MsgErr3():
    tkinter.messagebox.showerror("삭제 할 수 없음", "삭제가 불가능한 고객입니다\n(고객 정보 확인해주세요)")
#=======================================메인 페이지==========================================================
def mainWin():
    today = datetime.date.today()

    def calc():
        ck=0
        conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()
        stn=entry.get()

        treeview.delete(*treeview.get_children())
        cursor.execute('SELECT INDX, DIVI, TRPRICE, SCALE FROM finance;')
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
        conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()

        cursor.execute('SELECT INDX, DIVI, TRPRICE, SCALE FROM finance;')

        for infom in cursor.fetchall():
            treeview.insert('','end', text="", values=infom, iid=infom)
            
        conn.close()


    #--------------------------환불, 주문-----------------------------

    def delete():
        cd=0
        conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
        dcursor = conn.cursor()
        stn=entry.get()
        bstn=bookentry.get()
        print(stn)

        dcursor.execute('SELECT INDX FROM finance;')
        sql="DELETE FROM finance WHERE INDX=%s;"
        val=(stn)

        for i in dcursor.fetchall():
            print(i)
            if i[0] == stn:
                cd+=1
                dcursor.execute(sql , val)
                conn.commit()
                Msgre()
            
        if cd==0:
            Msgbox()

        conn.close()


    def add():
        conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
        acursor = conn.cursor()
        count=0
        stn=entry.get()
        sdate=today
        num=buyentry.get()
        pr=prientry.get()        

        sql="INSERT INTO finance(INDX, BID, SSID, SCALE, TRPRICE, DIVI, TRDATE) VALUES(%s, %s, %s, %s, %s, %s, %s);"
        val=(stn, "B001", "S001", num, pr, "buy", sdate)

        acursor.execute('SELECT INDX FROM finance;')

        for i in acursor.fetchall():
            if i == stn:
                print("겹침")
                count+=1
        
        # 물류번호가 겹치지 않아야 주문 가능
        if count==0:
            acursor.execute(sql,val)
            conn.commit()
            Msgbuy()
        else:
            MsgErr()
        conn.close()


    #--------------------------------------------------------------------------------
    #----------------------------로그인 관리 윈도우-----------------------------------
    #--------------------------------------------------------------------------------
    def ban_cust():
        def redata():
            ck=0
            idcod=Bentry.get()
            pwcod=Bnamen.get()
            nwpw=Bentry2.get()
            renw=Bentry3.get()

            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            sql="SELECT STID, PWD FROM loginID;"
            cursor.execute(sql)

            for infom in cursor.fetchall():
                if idcod == infom[0] and pwcod == infom[1]:
                    if nwpw == renw:
                        ck+=1
                        sql2="UPDATE loginID SET STID = %s, PWD = %s WHERE STID = %s;"
                        val2=(idcod, nwpw, idcod)
                        cursor.execute(sql2 , val2)
                        conn.commit()
                        Msgup()
                        conn.close()
                        new.destroy()
                        break
                    else:
                        break
            if ck==0:
                Msgbox()
                return 0            


        global new
        new=Toplevel()

        new.title("로그인 관리")
        new.geometry("350x350+600+500")
        new.resizable(False, False)


        font3=tkinter.font.Font(family="맑은 고딕", size=13, weight="bold")

        mainlf=tkinter.Label(new, text="비밀번호 재설정", width=350, height=2, fg="red", bg='grey87', font=font3)
        mainlf.pack(side="top")

        Blabelf=tkinter.LabelFrame(new, text="정보 입력", padx=5, pady=20)
        Blabelf.place(x=50, y=80)

        Bstnum=tkinter.Label(Blabelf, text="아이디")
        Bstnum.grid(row=0, column=0, sticky="w", pady=5)

        Bentry=tkinter.Entry(Blabelf)
        Bentry.grid(row=0, column=1, pady=5)

        Bstnam=tkinter.Label(Blabelf, text="기존 비밀번호")
        Bstnam.grid(row=1, column=0, sticky="w", pady=5)

        Bnamen=tkinter.Entry(Blabelf)
        Bnamen.grid(row=1, column=1, pady=5)
        
        Bstnum2=tkinter.Label(Blabelf, text="신규 비밀번호")
        Bstnum2.grid(row=2, column=0, sticky="w", pady=5)

        Bentry2=tkinter.Entry(Blabelf)
        Bentry2.grid(row=2, column=1, pady=5)

        Bstnum3=tkinter.Label(Blabelf, text="비밀번호 재입력")
        Bstnum3.grid(row=3, column=0, sticky="w", pady=5)

        Bentry3=tkinter.Entry(Blabelf)
        Bentry3.grid(row=3, column=1, pady=5)

        Bbutton = tkinter.Button(Blabelf, text="재설정", overrelief="solid", width=15, command=redata)
        Bbutton.grid(row=4, column=1, sticky="e", pady=5)





#--------------------------------------------------------------------------------
#---------------------------재정 관리 윈도우----------------------------------
#--------------------------------------------------------------------------------
    def finInfo():
                
        global new
        new=Toplevel()

        new.title("재정 검색")
        new.geometry("900x500+500+400")
        new.resizable(False, False)

        font3=tkinter.font.Font(family="맑은 고딕", size=25, weight="bold")

        mainlf=tkinter.Label(new, text="재정 관리", width=700, height=2, bg='grey87', font=font3)
        mainlf.pack(side="top")

        conn = pymssql.connect(host="127.0.0.1", database='안양문고관리', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()
        cursor.execute('SELECT dis_div, dis_selldate, dis_price FROM finance;')
        
        buy=[0]*12
        sell=[0]*12
        cutdate=[]
        
        for ap in cursor.fetchall():
            #test=ap[1]  # 년-월-일 값 가져오기
            cutdate=str(ap[1]).split('-') # 몇월 인지만 가져오기
            if ap[0]=='구매':                              
                for i in range(1,12):
                    if i == int(cutdate[1]):
                        buy.insert(i, (buy[i]+int(ap[2])))
                        print(i,'=',buy[i])
            if ap[0]=='판매':
                for i in range(1,12):
                    if i == int(cutdate[1]):
                        sell.insert(i, (sell[i]+int(ap[2])))
            
        
        fig = Figure(figsize=(6, 4), dpi=100)  #그래프 그릴 창 생성 (크기, dpi)
        ax = fig.add_subplot(1,1,1)#창에 그래프 하나 추가
        ax.set_ylabel('price(million)')
        ax.set_xlabel('date(month)')
        ax.set_xticks([5,6,7,8],['5', '6', '7', '8'])
        ax.set_ylim([0, 5000000])
        ax.set_xlim([5,8])
        ax.plot([5,6,7,8],[buy[5],buy[6],buy[7],buy[8]], color="blue", marker='o', markersize=4, label='buy')
        ax.plot([5,6,7,8],[sell[5],sell[6],sell[7],sell[8]], color="red", marker='o', markersize=4, label='sell')
        ax.legend(loc=(0.96,0.99))

        canvas = FigureCanvasTkAgg(fig, master=new)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10, anchor="w") # 그래프 위치
        
        
        
        Blabelf=tkinter.LabelFrame(new, text="재정 목록 검색", padx=5, pady=20)
        Blabelf.place(x=620, y=100)

        Bstnum=tkinter.Label(Blabelf, text="연도")
        Bstnum.grid(row=0, column=0, sticky="e", padx=10, pady=5)

        Ycombo = Combobox(Blabelf, width=18)
        Ycombo['values']=(2022)
        Ycombo.current(0)
        Ycombo.grid(row=0, column=1, sticky="w", pady=5)

        Bstnum=tkinter.Label(Blabelf, text="월")
        Bstnum.grid(row=1, column=0, sticky="e", padx=10, pady=5)

        Mcombo = Combobox(Blabelf, width=18)
        Mcombo['values']=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        Mcombo.current(7)
        Mcombo.grid(row=1, column=1, sticky="w", pady=5)

        CheckVar1=tkinter.IntVar()
        CheckVar2=tkinter.IntVar()
        c1=tkinter.Checkbutton(Blabelf,text="buy",variable=tkinter.IntVar())
        c1.select()
        c1.grid(row=4, column=0, pady=5)
        
        c2=tkinter.Checkbutton(Blabelf,text="sell",variable=tkinter.IntVar())
        c2.select()
        c2.grid(row=4, column=1, pady=5)
        

        nullb=tkinter.Label(Blabelf, text="", height=4)
        nullb.grid(row=9, column=0, sticky="w", pady=5)       
        
        Bbutton = tkinter.Button(Blabelf, text="검색", overrelief="solid", width=15)
        Bbutton.grid(row=10, column=1, sticky="e", pady=5)


    #--------------------------------------------------------------------------------
    #---------------------------물류 목록 검색 윈도우----------------------------------
    #--------------------------------------------------------------------------------
    def totalInfo():
        def bif():  #원하는 물류 검색하기
            ck=0
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            stnum=Bentry.get()
            stn=Bnamen.get()

            Btreeview.delete(*Btreeview.get_children())
            
            cursor.execute('SELECT BID, BNAME, GID, BSTOCK FROM book;')
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

                sql="SELECT GID, GNAME, GSITE FROM genre WHERE GID=%s;"
                val=(gnum)
                cursor.execute(sql, val)
                kk=cursor.fetchall()
                for isa in kk:
                    blf3.config(text=str(isa))

            conn.close()

        def re_info():  #물류 전체 목록 다시 보기
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            cursor.execute('SELECT BID, BNAME, GID, BSTOCK FROM book ORDER BY GID ASC, BNAME ASC;')

            Btreeview.delete(*Btreeview.get_children())
            
            for infom in cursor.fetchall():
                Btreeview.insert('','end', text="", values=infom, iid=infom)
            
            blf3.config(text="('물류번호', '물류명', '추가정보')")
                    
            conn.close()

        def bookadd():
            count=0
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()  
            bnum=Bentry.get()
            bname=Bnamen.get()
            wname=Bentry2.get()
            countB=Bentry3.get()
            genr=Bentry4.get()

            sql="INSERT INTO book(BID, BNAME, PUBLISHER, GID, BSTOCK) VALUES(%s, %s, %s, %s, %s);"
            val=(bnum, bname, wname, genr, countB)

            sql2="SELECT BID FROM book;"
            cursor.execute(sql2)
            num=cursor.fetchone()

            #같은 물류번호가 이미 존재하는지 확인 (중복 등록 방지)
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
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            dcursor = conn.cursor()
            bnum=Bentry.get()
            bname=Bnamen.get()

            sql="DELETE FROM book WHERE BID = %s or BNAME = %s;"
            val=(bnum, bname)

            sql2="SELECT BSTOCK FROM book WHERE BID = %s or BNAME = %s;"
            dcursor.execute(sql2 , val)
            ban=dcursor.fetchone()
            for bren in ban:
                print(bren)
            
            #삭제 가능한 물류가 있는지 확인
            if bren != "0":
                dcursor.execute(sql , val)
                conn.commit()
                Msgdel()
            else:
                Msgbox()

            conn.close()

        def bupdate():
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            bnum=Bentry.get()
            bname=Bnamen.get()
            wname=Bentry2.get()
            countB=Bentry3.get()
            genr=Bentry4.get()

            cursor.execute('SELECT BID FROM book;')
            sel=cursor.fetchone()

            #물류번호를 입력하지 않았거나, 이미 존재하는 동일한 물류번호를 입력하면 업데이트 불가 메시지 출력
            if bnum=="" or bnum==sel:
                Msgbox()
            else:
                sql="UPDATE book SET BID = %s, BNAME = %s, PUBLISHER = %s, GID = %s, BSTOCK = %s WHERE BID = %s;"
                val=(bnum, bname, wname, genr, countB, bnum)              
                cursor.execute(sql , val)
                conn.commit()
                Msgup()
            conn.close()
                
        global new
        new=Toplevel()

        new.title("물류 검색")
        new.geometry("700x500+500+400")
        new.resizable(False, False)

        font3=tkinter.font.Font(family="맑은 고딕", size=25, weight="bold")

        mainlf=tkinter.Label(new, text="물류 관리", width=700, height=2, bg='grey87', font=font3)
        mainlf.pack(side="top")

        mainlf2=tkinter.Label(new, text="- 물류 검색은 '물류 번호' 또는 '물류명' 입력을 필요로 합니다 -", bg='grey87')
        mainlf2.place(x=350, y=70)

        Blabelf=tkinter.LabelFrame(new, text="물류 목록 검색", padx=5, pady=20)
        Blabelf.place(x=420, y=100)

        Bstnum=tkinter.Label(Blabelf, text="물류 번호 입력")
        Bstnum.grid(row=0, column=0, sticky="w", pady=5)

        Bentry=tkinter.Entry(Blabelf)
        Bentry.grid(row=0, column=1, pady=5)

        Bstnam=tkinter.Label(Blabelf, text="물류명 입력")
        Bstnam.grid(row=1, column=0, sticky="w", pady=5)

        Bnamen=tkinter.Entry(Blabelf)
        Bnamen.grid(row=1, column=1, pady=5)
        
        Bstnum2=tkinter.Label(Blabelf, text="작가명 입력")
        Bstnum2.grid(row=2, column=0, sticky="w", pady=5)

        Bentry2=tkinter.Entry(Blabelf)
        Bentry2.grid(row=2, column=1, pady=5)

        Bstnum3=tkinter.Label(Blabelf, text="물류 수량 입력")
        Bstnum3.grid(row=3, column=0, sticky="w", pady=5)

        Bentry3=tkinter.Entry(Blabelf)
        Bentry3.grid(row=3, column=1, pady=5)

        Bstnum4=tkinter.Label(Blabelf, text="금액 입력")
        Bstnum4.grid(row=4, column=0, sticky="w", pady=5)

        Bentry4=tkinter.Entry(Blabelf)
        Bentry4.grid(row=4, column=1, pady=5)
        
        Bbutton = tkinter.Button(Blabelf, text="검색", overrelief="solid", width=15, command=bif)
        Bbutton.grid(row=10, column=1, sticky="e", pady=5)

        Bbutton2 = tkinter.Button(Blabelf, text="목록 전체보기", overrelief="solid", width=15, command=re_info)
        Bbutton2.grid(row=10, column=0, pady=5)
        
        nullb=tkinter.Label(Blabelf, text="", height=3)
        nullb.grid(row=11, column=0, sticky="w", pady=5)

        blf=tkinter.Label(new, text="물류 정보 수정 (주문, 취소, 수정 선택)", width=37, height=2, bg='grey87', relief="ridge")
        blf.place(x=423, y=345)

        blf2=tkinter.Label(new, text=" 도서 위치 정보:                    ", width=20, height=2, bg='grey87', relief="ridge", anchor="w", padx=10)
        blf2.place(x=110, y=105)

        blf3=tkinter.Label(new, text="('물류번호', '물류명', '추가정보')", width=25, height=2, bg='white', relief="ridge", anchor="w", padx=10)
        blf3.place(x=214, y=105)
        
        blf4=tkinter.Label(new, text="총 물류 수: ", width=8, height=2, bg='grey87', relief="ridge", anchor="w", padx=10)
        blf4.place(x=5, y=105)

        blf5=tkinter.Label(new, text="", width=2, height=2, bg='white', relief="ridge", anchor="w", padx=10)
        blf5.place(x=80, y=105)

        b1 = tkinter.Button(Blabelf, text='주문', overrelief="solid", width=15, command=bookadd)
        b1.grid(row=12, column=1, sticky="se")
        b2 = tkinter.Button(Blabelf, text='취소', overrelief="solid", width=15, command=bdelete)
        b2.grid(row=12, column=0, sticky="se")
        b3 = tkinter.Button(Blabelf, text='수정', overrelief="solid", width=15, command=bupdate)
        b3.grid(row=13, column=1, sticky="se", pady=5)

        #---------------------------표 만들기---------------------------------------

        Btreeview=tkinter.ttk.Treeview(new, columns=["zero", "one", "two", "tree"], displaycolumns=["zero", "one", "two", "tree"], height=15)
        Btreeview.place(x=5, y=145)

        Btreeview.column("zero", width=100, anchor="center")
        Btreeview.heading("zero", text="물류코드", anchor="center")

        Btreeview.column("one", width=135, anchor="center")
        Btreeview.heading("one", text="물류명", anchor="center")

        Btreeview.column("two", width=80, anchor="center")
        Btreeview.heading("two", text="물류번호", anchor="center")

        Btreeview.column("tree", width=90, anchor="center")
        Btreeview.heading("tree", text="잔여 물류 수", anchor="center")

        Btreeview["show"]="headings"

        conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()

        cursor.execute('SELECT BID, BNAME, GID, BSTOCK FROM book ORDER BY GID ASC, BNAME ASC;')

        for infom in cursor.fetchall():
            Btreeview.insert('','end', text="", values=infom, iid=infom)


        sql="SELECT count(distinct BNAME) FROM book;"
        cursor.execute(sql)
        kk=cursor.fetchone()
        for isa in kk:
            blf5.config(text=str(isa))
        
        conn.close()



    #--------------------------------------------------------------------------------
    #---------------------------도서 목록 검색 윈도우----------------------------------
    #--------------------------------------------------------------------------------
    def bookInfo():
        def bif():  #원하는 도서 검색하기
            ck=0
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            stnum=Bentry.get()
            stn=Bnamen.get()

            Btreeview.delete(*Btreeview.get_children())
            
            cursor.execute('SELECT BID, BNAME, GID, BSTOCK FROM book;')
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

                sql="SELECT GID, GNAME, GSITE FROM genre WHERE GID=%s;"
                val=(gnum)
                cursor.execute(sql, val)
                kk=cursor.fetchall()
                for isa in kk:
                    blf3.config(text=str(isa))

            conn.close()

        def re_info():  #도서 전체 목록 다시 보기
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            cursor.execute('SELECT BID, BNAME, GID, BSTOCK FROM book ORDER BY GID ASC, BNAME ASC;')

            Btreeview.delete(*Btreeview.get_children())
            
            for infom in cursor.fetchall():
                Btreeview.insert('','end', text="", values=infom, iid=infom)
            
            blf3.config(text="('장르번호', '장르명', '도서위치')")
                    
            conn.close()

        def bookadd():
            count=0
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()  
            bnum=Bentry.get()
            bname=Bnamen.get()
            wname=Bentry2.get()
            countB=Bentry3.get()
            genr=Bentry4.get()

            sql="INSERT INTO book(BID, BNAME, PUBLISHER, GID, BSTOCK) VALUES(%s, %s, %s, %s, %s);"
            val=(bnum, bname, wname, genr, countB)

            sql2="SELECT BID FROM book;"
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
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            dcursor = conn.cursor()
            bnum=Bentry.get()
            bname=Bnamen.get()

            sql="DELETE FROM book WHERE BID = %s or BNAME = %s;"
            val=(bnum, bname)

            sql2="SELECT BSTOCK FROM book WHERE BID = %s or BNAME = %s;"
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
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            bnum=Bentry.get()
            bname=Bnamen.get()
            wname=Bentry2.get()
            countB=Bentry3.get()
            genr=Bentry4.get()

            cursor.execute('SELECT BID FROM book;')
            sel=cursor.fetchone()

            #도서번호를 입력하지 않았거나, 이미 존재하는 동일한 도서번호를 입력하면 업데이트 불가 메시지 출력
            if bnum=="" or bnum==sel:
                Msgbox()
            else:
                sql="UPDATE book SET BID = %s, BNAME = %s, PUBLISHER = %s, GID = %s, BSTOCK = %s WHERE BID = %s;"
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
        
        Bstnum2=tkinter.Label(Blabelf, text="출판사명 입력")
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

        conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()

        cursor.execute('SELECT BID, BNAME, GID, BSTOCK FROM book ORDER BY GID ASC, BNAME ASC;')

        for infom in cursor.fetchall():
            Btreeview.insert('','end', text="", values=infom, iid=infom)


        sql="SELECT count(distinct BNAME) FROM book;"
        cursor.execute(sql)
        kk=cursor.fetchone()
        for isa in kk:
            blf5.config(text=str(isa))
        
        conn.close()

    #--------------------------------------------------------------------------------
    #---------------------------문구 목록 검색 윈도우----------------------------------
    #--------------------------------------------------------------------------------
    def stnrInfo(): #stationery info
        def bif():  #원하는 문구 검색하기
            ck=0
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            stnum=Bentry.get()
            stn=Bnamen.get()

            Btreeview.delete(*Btreeview.get_children())
            
            cursor.execute('SELECT SSID, SNAME, CATEGORY, SSTOCK FROM stationery;')
            for infom in cursor.fetchall():
                if stn == infom[1] or stnum == infom[0]:
                    gnum=infom[1]
                    real=infom
                    ck+=1
            if ck==0:
                Msgbox()
                return 0
            else:
                print(gnum)
                Btreeview.insert('','end', text="", values=real, iid=real)

                sql="SELECT SNAME, MAKER, SPRICE FROM stationery WHERE SSID=%s;"
                val=(stnum)
                cursor.execute(sql, val)
                kk=cursor.fetchall()
                for isa in kk:
                    blf3.config(text=str(isa))

            conn.close()

        def re_info():  #도서 전체 목록 다시 보기
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            cursor.execute('SELECT SSID, SNAME, CATEGORY, SSTOCK FROM stationery ORDER BY CATEGORY ASC, SSID ASC;')

            Btreeview.delete(*Btreeview.get_children())
            
            for infom in cursor.fetchall():
                Btreeview.insert('','end', text="", values=infom, iid=infom)
            
            blf3.config(text="('문구명', '브랜드', '금액')")
                    
            conn.close()

        def bookadd():
            count=0
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()  
            bnum=Bentry.get()
            bname=Bnamen.get()
            wname=Bentry2.get()
            countB=Bentry3.get()
            genr=Bentry4.get()
            lc='0'
            price=Bentry5.get()
            
            sql="INSERT INTO stationery(SSID, SNAME, MAKER, SSTOCK, CATEGORY, SSALES, SPRICE) VALUES(%s, %s, %s, %s, %s, %s, %s);"
            val=(bnum, bname, wname, genr, countB, lc, price)

            sql2="SELECT SSID FROM stationery;"
            cursor.execute(sql2)
            num=cursor.fetchone()

            #같은 문구번호가 이미 존재하는지 확인 (중복 등록 방지)
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
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            dcursor = conn.cursor()
            bnum=Bentry.get()
            bname=Bnamen.get()

            sql="DELETE FROM stationery WHERE SSID = %s or SNAME = %s;"
            val=(bnum, bname)

            sql2="SELECT SSTOCK FROM stationery WHERE SSID = %s or SNAME = %s;"
            dcursor.execute(sql2 , val)
            ban=dcursor.fetchone()
            for bren in ban:
                print(bren)
            
            # 재고가 남아있는지 확인
            if bren == "0":
                dcursor.execute(sql , val)
                conn.commit()
                Msgdel()
            else:
                Msgbox()

            conn.close()

        def bupdate():
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            bnum=Bentry.get()
            bname=Bnamen.get()
            wname=Bentry2.get()
            countB=Bentry3.get()
            genr=Bentry4.get()
            lc="0" # 판매 수량
            price=Bentry5.get()
            
            cursor.execute('SELECT SSID FROM stationery;')
            sel=cursor.fetchone()

            #물류번호를 입력하지 않았거나, 이미 존재하는 동일한 물류번호를 입력하면 업데이트 불가 메시지 출력
            if bnum=="" or bnum==sel:
                Msgbox()
            else:
                sql="UPDATE stationery SET SSID = %s, SNAME = %s, MAKER = %s, CATEGORY = %s, SSTOCK = %s, SPRICE = %s , SSALES = %s WHERE SSID = %s;"
                val=(bnum, bname, wname, genr, countB, price, lc, bnum)              
                cursor.execute(sql , val)
                conn.commit()
                Msgup()
            conn.close()
                
        global new
        new=Toplevel()

        new.title("문구 검색")
        new.geometry("700x500+500+400")
        new.resizable(False, False)

        font3=tkinter.font.Font(family="맑은 고딕", size=25, weight="bold")

        mainlf=tkinter.Label(new, text="문구 관리", width=700, height=2, bg='grey87', font=font3)
        mainlf.pack(side="top")

        mainlf2=tkinter.Label(new, text="- 문구 검색은 '문구 번호' 또는 '문구명' 입력을 필요로 합니다 -", bg='grey87')
        mainlf2.place(x=350, y=70)

        Blabelf=tkinter.LabelFrame(new, text="문구 목록 검색", padx=5, pady=20)
        Blabelf.place(x=420, y=100)

        Bstnum=tkinter.Label(Blabelf, text="문구 번호 입력")
        Bstnum.grid(row=0, column=0, sticky="w", pady=5)

        Bentry=tkinter.Entry(Blabelf)
        Bentry.grid(row=0, column=1, pady=5)

        Bstnam=tkinter.Label(Blabelf, text="문구명 입력")
        Bstnam.grid(row=1, column=0, sticky="w", pady=5)

        Bnamen=tkinter.Entry(Blabelf)
        Bnamen.grid(row=1, column=1, pady=5)
        
        Bstnum2=tkinter.Label(Blabelf, text="업체명 입력")
        Bstnum2.grid(row=2, column=0, sticky="w", pady=5)

        Bentry2=tkinter.Entry(Blabelf)
        Bentry2.grid(row=2, column=1, pady=5)

        Bstnum3=tkinter.Label(Blabelf, text="문구 수량 입력")
        Bstnum3.grid(row=3, column=0, sticky="w", pady=5)

        Bentry3=tkinter.Entry(Blabelf)
        Bentry3.grid(row=3, column=1, pady=5)

        Bstnum4=tkinter.Label(Blabelf, text="카테고리 입력")
        Bstnum4.grid(row=4, column=0, sticky="w", pady=5)

        Bentry4=tkinter.Entry(Blabelf)
        Bentry4.grid(row=4, column=1, pady=5)
        
        Bstnum5=tkinter.Label(Blabelf, text="금액 입력")
        Bstnum5.grid(row=5, column=0, sticky="w", pady=5)

        Bentry5=tkinter.Entry(Blabelf)
        Bentry5.grid(row=5, column=1, pady=5)
        
        Bbutton = tkinter.Button(Blabelf, text="검색", overrelief="solid", width=15, command=bif)
        Bbutton.grid(row=10, column=1, sticky="e", pady=5)

        Bbutton2 = tkinter.Button(Blabelf, text="목록 전체보기", overrelief="solid", width=15, command=re_info)
        Bbutton2.grid(row=10, column=0, pady=5)
        
        nullb=tkinter.Label(Blabelf, text="", height=3)
        nullb.grid(row=11, column=0, sticky="w", pady=5)

        blf=tkinter.Label(new, text="문구 정보 수정 (등록, 삭제, 수정 선택)", width=37, height=2, bg='grey87', relief="ridge")
        blf.place(x=423, y=375)

        blf2=tkinter.Label(new, text=" 문구 위치 정보:                    ", width=20, height=2, bg='grey87', relief="ridge", anchor="w", padx=10)
        blf2.place(x=110, y=105)

        blf3=tkinter.Label(new, text="('문구명', '브랜드', '금액')", width=25, height=2, bg='white', relief="ridge", anchor="w", padx=10)
        blf3.place(x=214, y=105)
        
        blf4=tkinter.Label(new, text="총 문구 수: ", width=8, height=2, bg='grey87', relief="ridge", anchor="w", padx=10)
        blf4.place(x=5, y=105)

        blf5=tkinter.Label(new, text="", width=4, height=2, bg='white', relief="ridge", anchor="w")
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
        Btreeview.heading("zero", text="문구코드", anchor="center")

        Btreeview.column("one", width=135, anchor="center")
        Btreeview.heading("one", text="문구명", anchor="center")

        Btreeview.column("two", width=80, anchor="center")
        Btreeview.heading("two", text="카테고리", anchor="center")

        Btreeview.column("tree", width=90, anchor="center")
        Btreeview.heading("tree", text="잔여 문구 수", anchor="center")

        Btreeview["show"]="headings"

        conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()

        cursor.execute('SELECT SSID, SNAME, CATEGORY, SSTOCK FROM stationery ORDER BY CATEGORY ASC, SSID ASC;')

        for infom in cursor.fetchall():
            Btreeview.insert('','end', text="", values=infom, iid=infom)


        sql="SELECT count(distinct SSID) FROM stationery;"
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
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            stname=Cnamen.get() #이름 정보 가져오기
            stnum=Centry.get()  #학번 정보 가져오기

            Ctreeview.delete(*Ctreeview.get_children())
            cursor.execute('SELECT MID, MNAME, PN, MPOINT FROM client_member;')
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
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            cursor.execute('SELECT MID, MNAME, PN, MPOINT FROM client_member;')
            Ctreeview.delete(*Ctreeview.get_children())
            for infom in cursor.fetchall():
                Ctreeview.insert('','end', text="", values=infom, iid=infom)
        
            Centry.delete(0, 'end')
            Cnamen.delete(0, 'end')
            phonen.delete(0, 'end')
            mailen.delete(0, 'end')
                    
            conn.close()

        def cdelete():
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            dcursor = conn.cursor()
            stnum=Centry.get()
            stname=Cnamen.get()

            sql="DELETE FROM client_member WHERE MID = %s or MNAME = %s;"
            val=(stnum, stname)

            sql2="SELECT MPOINT FROM client_member WHERE MID = %s or MNAME = %s;"
            dcursor.execute(sql2 , val)
            ban=dcursor.fetchone()
            for bren in ban:
                print(bren)
            
            # 잔여 포인트가 있는 고객인지 확인
            if bren == "0":
                dcursor.execute(sql , val)
                Msgdel()
            else:
                MsgErr3()

            conn.commit()
            conn.close()

        def cadd():
            count=0

            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            stnum=Centry.get()
            stname=Cnamen.get()
            phone=phonen.get()
            bth=mailen.get()
            gn=gnd.get()
            

            sql="INSERT INTO client_member(MID, MNAME, PN, BIRTH, GENDER, MPOINT) VALUES(%s, %s, %s, %s, %s, %s);"
            val=(stnum, stname, phone, bth, gn, "0")

            sql2="SELECT MID FROM client_member;"
            cursor.execute(sql2)
            num=cursor.fetchone()

            #같은 고객번호가 이미 존재하는지 확인 (중복 등록 방지)
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
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            stnum=Centry.get()
            stname=Cnamen.get()
            phone=phonen.get()
            mail=mailen.get()
            point=pointen.get()

            sql="UPDATE client_member SET MNAME = %s, PN = %s, BIRTH = %s, MPOINT = %s WHERE MID = %s;"
            val=(stname, phone, mail, point, stnum)
            cursor.execute(sql , val)

            conn.commit()
            Msgup()
            conn.close()

        global new
        new=Toplevel()

        new.title("회원 검색")
        new.geometry("700x500+500+300")
        new.resizable(False, False)

        font3=tkinter.font.Font(family="맑은 고딕", size=25, weight="bold")
        font4=tkinter.font.Font(size=12, weight="bold")

        mainlf=tkinter.Label(new, text="회원 관리", width=700, height=2, bg='grey87', font=font3)
        mainlf.pack(side="top")

        mainlf2=tkinter.Label(new, text="- 회원 검색은 '회원 번호' 또는 '회원 이름' 입력을 필요로 합니다 -", bg='grey87')
        mainlf2.place(x=340, y=70)

        Clabelf=tkinter.LabelFrame(new, text="회원 목록 검색", padx=10, pady=20)
        Clabelf.place(x=395, y=100)

        Cstnum=tkinter.Label(Clabelf, text="회원 번호 입력 ")
        Cstnum.grid(row=0, column=0, sticky="w", pady=5)

        Centry=tkinter.Entry(Clabelf)
        Centry.grid(row=0, column=1, pady=5)

        Cnamelb=tkinter.Label(Clabelf, text="회원 이름 입력 ")
        Cnamelb.grid(row=1, column=0, sticky="w", pady=5)

        Cnamen=tkinter.Entry(Clabelf)
        Cnamen.grid(row=1, column=1, pady=5)

        phonelb=tkinter.Label(Clabelf, text="전화번호  입력 ")
        phonelb.grid(row=2, column=0, sticky="w", pady=5)

        phonen=tkinter.Entry(Clabelf)
        phonen.grid(row=2, column=1, pady=5)

        maillb=tkinter.Label(Clabelf, text="생년월일 입력 ")
        maillb.grid(row=3, column=0, sticky="w", pady=5)

        mailen=tkinter.Entry(Clabelf)
        mailen.grid(row=3, column=1, pady=5)
        
        gndlb=tkinter.Label(Clabelf, text="성별 입력")
        gndlb.grid(row=4, column=0, sticky="w", pady=5)

        gnd=tkinter.Entry(Clabelf)
        gnd.grid(row=4, column=1, pady=5)
        
        plb=tkinter.Label(Clabelf, text="포인트 입력")
        plb.grid(row=5, column=0, sticky="w", pady=5)

        pointen=tkinter.Entry(Clabelf)
        pointen.grid(row=5, column=1, pady=5)  

        Cbutton = tkinter.Button(Clabelf, text="검색", overrelief="solid", width=15, command=cif)
        Cbutton.grid(row=10, column=1, sticky="e", pady=5)

        Cbutton2 = tkinter.Button(Clabelf, text="항목 초기화", overrelief="solid", width=15, command=cre_info)
        Cbutton2.grid(row=10, column=0, sticky="w", pady=5)

        nulllb=tkinter.Label(Clabelf, text="", height=3)
        nulllb.grid(row=11, column=0, sticky="w", pady=5)

        relf=tkinter.Label(new, text="회원 정보 수정 (등록, 삭제, 수정 선택)", width=37, height=2, bg='grey87', relief="ridge")
        relf.place(x=400, y=375)

        c1 = tkinter.Button(Clabelf, text='등록', overrelief="solid", width=15, command=cadd)
        c1.grid(row=12, column=1, sticky="se")
        c2 = tkinter.Button(Clabelf, text='삭제', overrelief="solid", width=15, command=cdelete)
        c2.grid(row=12, column=0, sticky="se")
        c3 = tkinter.Button(Clabelf, text='수정', overrelief="solid", width=15, command=cupdate)
        c3.grid(row=13, column=1, sticky="se", pady=5)

        #---------------------------표 만들기---------------------------------------

        Ctreeview=tkinter.ttk.Treeview(new, columns=["zero", "one", "two", "tree"], displaycolumns=["zero", "one", "two", "tree"], height=15)
        Ctreeview.place(x=20, y=109)

        Ctreeview.column("zero", width=90, anchor="center")
        Ctreeview.heading("zero", text="회원번호", anchor="center")

        Ctreeview.column("one", width=80, anchor="center")
        Ctreeview.heading("one", text="회원명", anchor="center")

        Ctreeview.column("two", width=100, anchor="center")
        Ctreeview.heading("two", text="연락처", anchor="center")

        Ctreeview.column("tree", width=80, anchor="center")
        Ctreeview.heading("tree", text="보유 포인트", anchor="center")

        Ctreeview["show"]="headings"

        conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()

        cursor.execute('SELECT MID, MNAME, PN, MPOINT FROM client_member;')

        for infom in cursor.fetchall():
            Ctreeview.insert('','end', text="", values=infom, iid=infom)
        
        conn.close()



    #--------------------------------------------------------------------------------
    #---------------------------사원 목록 검색 윈도우----------------------------------
    #--------------------------------------------------------------------------------
    def memInfo():
        def bif():
            ck=0
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            stnum=Bentry.get()
            stn=Bnamen.get()

            Btreeview.delete(*Btreeview.get_children())
            
            cursor.execute('SELECT STID, STNAME, PN, DEPT FROM staff;')
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

                sql="SELECT STNAME, DEPT, SRANK FROM staff WHERE STID=%s;"
                val=(stnum)
                cursor.execute(sql, val)
                kk=cursor.fetchall()
                for isa in kk:
                    blf3.config(text=str(isa))

            conn.close()

        def re_info():  #사원 전체 목록 다시 보기
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            cursor.execute('SELECT STID, STNAME, PN, DEPT FROM staff ORDER BY DEPT ASC, STNAME ASC;')

            Btreeview.delete(*Btreeview.get_children())
            
            for infom in cursor.fetchall():
                Btreeview.insert('','end', text="", values=infom, iid=infom)
            
            blf3.config(text="('사원명', '부서명', '직급')")
                    
            conn.close()

        def bookadd():
            count=0
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()  
            bnum=Bentry.get()
            bname=Bnamen.get()
            wname=Bentry2.get()
            countB=Bentry3.get()
            genr=Bentry4.get()

            sql="INSERT INTO staff(STID, STNAME, PN, SRANK, DEPT) VALUES(%s, %s, %s, %s, %s);"
            val=(bnum, bname, wname, genr, countB)
            
            sql3="INSERT INTO loginID(STID, PWD) VALUES(%s, %s);"
            val3=(bnum, "1111")

            sql2="SELECT STID FROM staff;"
            cursor.execute(sql2)
            num=cursor.fetchone()

            #같은 사원번호가 이미 존재하는지 확인 (중복 등록 방지)
            for con in num:
                if bnum == con:
                    count+=1
            if count == 0:
                cursor.execute(sql , val)
                cursor.execute(sql3 , val3)
                conn.commit()
                Msgadd()
            else:
                MsgErr2()

            conn.close()

        def bdelete():
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            dcursor = conn.cursor()
            bnum=Bentry.get()
            bname=Bnamen.get()

            sql="DELETE FROM staff WHERE STID = %s or STNAME = %s;"
            val=(bnum, bname)
            
            sql3="DELETE FROM loginID WHERE STID = %s;"

            dcursor.execute(sql3 , val)
            dcursor.execute(sql , val)               
            conn.commit()
            Msgdel()

            conn.close()

        def bupdate():
            conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
            cursor = conn.cursor()
            bnum=Bentry.get()
            bname=Bnamen.get()
            wname=Bentry2.get()
            countB=Bentry3.get()
            genr=Bentry4.get()

            cursor.execute('SELECT STID FROM staff;')
            sel=cursor.fetchone()

            #사원번호를 입력하지 않았거나, 이미 존재하는 동일한 사원번호를 입력하면 업데이트 불가 메시지 출력
            if bnum=="" or bnum==sel:
                Msgbox()
            else:
                sql="UPDATE staff SET STID = %s, STNAME = %s, PN = %s, SRANK = %s, DEPT = %s WHERE STID = %s;"
                val=(bnum, bname, wname, genr, countB, bnum)              
                cursor.execute(sql , val)
                conn.commit()
                Msgup()
            conn.close()
                
        global new
        new=Toplevel()

        new.title("사원 검색")
        new.geometry("700x500+500+400")
        new.resizable(False, False)

        font3=tkinter.font.Font(family="맑은 고딕", size=25, weight="bold")
        font4=tkinter.font.Font(size=12, weight="bold")

        mainlf=tkinter.Label(new, text="사원 관리", width=700, height=2, bg='grey87', font=font3)
        mainlf.pack(side="top")

        mainlf2=tkinter.Label(new, text="- 사원 검색은 '사원 번호' 또는 '사원명' 입력을 필요로 합니다 -", bg='grey87')
        mainlf2.place(x=350, y=70)

        Blabelf=tkinter.LabelFrame(new, text="사원 목록 검색", padx=5, pady=20)
        Blabelf.place(x=420, y=100)

        Bstnum=tkinter.Label(Blabelf, text="사원 번호 입력")
        Bstnum.grid(row=0, column=0, sticky="w", pady=5)

        Bentry=tkinter.Entry(Blabelf)
        Bentry.grid(row=0, column=1, pady=5)

        Bstnam=tkinter.Label(Blabelf, text="사원명 입력")
        Bstnam.grid(row=1, column=0, sticky="w", pady=5)

        Bnamen=tkinter.Entry(Blabelf)
        Bnamen.grid(row=1, column=1, pady=5)
        
        Bstnum2=tkinter.Label(Blabelf, text="연락처 입력")
        Bstnum2.grid(row=2, column=0, sticky="w", pady=5)

        Bentry2=tkinter.Entry(Blabelf)
        Bentry2.grid(row=2, column=1, pady=5)

        Bstnum3=tkinter.Label(Blabelf, text="부서명 입력")
        Bstnum3.grid(row=3, column=0, sticky="w", pady=5)

        Bentry3=tkinter.Entry(Blabelf)
        Bentry3.grid(row=3, column=1, pady=5)

        Bstnum4=tkinter.Label(Blabelf, text="직급 입력")
        Bstnum4.grid(row=4, column=0, sticky="w", pady=5)

        Bentry4=tkinter.Entry(Blabelf)
        Bentry4.grid(row=4, column=1, pady=5)
        
        Bbutton = tkinter.Button(Blabelf, text="검색", overrelief="solid", width=15, command=bif)
        Bbutton.grid(row=10, column=1, sticky="e", pady=5)

        Bbutton2 = tkinter.Button(Blabelf, text="목록 전체보기", overrelief="solid", width=15, command=re_info)
        Bbutton2.grid(row=10, column=0, pady=5)
        
        nullb=tkinter.Label(Blabelf, text="", height=3)
        nullb.grid(row=11, column=0, sticky="w", pady=5)

        blf=tkinter.Label(new, text="사원 정보 수정 (등록, 삭제, 수정 선택)", width=37, height=2, bg='grey87', relief="ridge")
        blf.place(x=423, y=345)

        blf2=tkinter.Label(new, text=" 상세 사원 정보:                    ", width=20, height=2, bg='grey87', relief="ridge", anchor="w", padx=10)
        blf2.place(x=110, y=105)

        blf3=tkinter.Label(new, text="('사원명', '부서명', '직급')", width=25, height=2, bg='white', relief="ridge", anchor="w", padx=10)
        blf3.place(x=214, y=105)
        
        blf4=tkinter.Label(new, text="총 사원 수: ", width=8, height=2, bg='grey87', relief="ridge", anchor="w", padx=10)
        blf4.place(x=5, y=105)

        blf5=tkinter.Label(new, text="", width=5, height=2, bg='white', relief="ridge", anchor="w")
        blf5.place(x=80, y=105)

        b1 = tkinter.Button(Blabelf, text='등록', overrelief="solid", width=15, command=bookadd)
        b1.grid(row=12, column=1, sticky="se")
        b2 = tkinter.Button(Blabelf, text='삭제', overrelief="solid", width=15, command=bdelete)
        b2.grid(row=12, column=0, sticky="se")
        b3 = tkinter.Button(Blabelf, text='수정', overrelief="solid", width=15, command=bupdate)
        b3.grid(row=13, column=1, sticky="se", pady=5)

        costla=tkinter.Label(new, text="로그인 관리하기", width=14, height=3, fg="red", bg='grey87', relief="ridge", anchor="n", pady=13, font=font4)
        costla.place(x=260, y=382)

        buttonC = tkinter.Button(new, text="로그인 목록", overrelief="solid", width=15, height=2, command=ban_cust)
        buttonC.place(x=275, y=422)

        #---------------------------표 만들기---------------------------------------

        Btreeview=tkinter.ttk.Treeview(new, columns=["zero", "one", "two", "tree"], displaycolumns=["zero", "one", "two", "tree"], height=10)
        Btreeview.place(x=5, y=145)

        Btreeview.column("zero", width=100, anchor="center")
        Btreeview.heading("zero", text="사원코드", anchor="center")

        Btreeview.column("one", width=80, anchor="center")
        Btreeview.heading("one", text="사원명", anchor="center")

        Btreeview.column("two", width=135, anchor="center")
        Btreeview.heading("two", text="연락처", anchor="center")

        Btreeview.column("tree", width=90, anchor="center")
        Btreeview.heading("tree", text="부서명", anchor="center")

        Btreeview["show"]="headings"

        conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()
        
        cursor.execute('SELECT STID, STNAME, PN, DEPT FROM staff ORDER BY DEPT ASC, STNAME ASC;')

        for infom in cursor.fetchall():
            Btreeview.insert('','end', text="", values=infom, iid=infom)


        sql="SELECT count(distinct STID) FROM staff;"
        cursor.execute(sql)
        kk=cursor.fetchone()
        for isa in kk:
            blf5.config(text=str(isa))
        
        conn.close()
    #---------------------------------함수 끝!---------------------------------


    #--------------------------메인, 대여중인 고객 검색--------------------------

    window=tkinter.Tk()
    window.title("문고 관리 시스템")
    window.geometry("900x500+400+200")
    window.resizable(False, False)
    
    conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
    dcursor = conn.cursor()
    sql="SELECT STNAME, DEPT FROM staff WHERE STID = %s;"
    val=(user_id.get())
    dcursor.execute(sql , val)
    for data in dcursor.fetchall():
        print(data[0])
        userName=data[0]    # 유저명
        userAut=data[1]     # 유저 권한(직급)

    font=tkinter.font.Font(family="맑은 고딕", size=25, weight="bold")
    font2=tkinter.font.Font(size=12, weight="bold")
    font3=tkinter.font.Font(size=12, weight="bold")

    mainlf=tkinter.Label(window, text="안양문고 관리 시스템", width=700, height=2, bg='Slategray1', font=font)
    mainlf.pack(side="top")

    mainlf2=tkinter.Label(window, text="- 거래 검색은 '물류코드' 입력을 필요로 합니다 -", bg='Slategray1')
    mainlf2.place(x=625, y=70)
    
    def roo():
        window.destroy()
        log_pro()
    
    mainlf3=tkinter.Label(window, text=userName+" 님 안녕하세요!", bg='Slategray1')
    mainlf3.place(x=20, y=70)
    outbut = tkinter.Button(window, text="로그아웃", overrelief="solid", command= roo)
    outbut.place(x=180, y=70)

    mainlf2=tkinter.Label(window, text="", width=700, height=100, bg='RoyalBlue4')
    mainlf2.pack(side="bottom")

    labelf=tkinter.LabelFrame(window, text="거래 목록 검색", padx=5, pady=20, fg='white', bg='RoyalBlue4', font=font2)
    labelf.place(x=615, y=100)

    stnum=tkinter.Label(labelf, text="   물류코드 입력    ", bg='Slategray1', relief="ridge")
    stnum.grid(row=0, column=0)

    entry=tkinter.Entry(labelf)
    entry.grid(row=0, column=1, sticky="w")

    nullnum=tkinter.Label(labelf, text="", bg='RoyalBlue4')
    nullnum.grid(row=1, column=0, sticky="w")

    booknum=tkinter.Label(labelf, text="   거래일자 입력    ", bg='Slategray1', relief="ridge")
    booknum.grid(row=2, column=0)

    bookentry=tkinter.Entry(labelf)
    bookentry.grid(row=2, column=1, sticky="w")

    nullnum2=tkinter.Label(labelf, text="", bg='RoyalBlue4')
    nullnum2.grid(row=3, column=0, sticky="w")

    buynum=tkinter.Label(labelf, text="   거래수량 입력    ", bg='Slategray1', relief="ridge")
    buynum.grid(row=4, column=0)

    buyentry=tkinter.Entry(labelf)
    buyentry.grid(row=4, column=1, sticky="w")

    nullnum3=tkinter.Label(labelf, text="", bg='RoyalBlue4')
    nullnum3.grid(row=5, column=0, sticky="w")

    prinum=tkinter.Label(labelf, text="   거래금액 입력    ", bg='Slategray1', relief="ridge")
    prinum.grid(row=6, column=0)

    prientry=tkinter.Entry(labelf)
    prientry.grid(row=6, column=1, sticky="w")

    nullnum4=tkinter.Label(labelf, text="", bg='RoyalBlue4')
    nullnum4.grid(row=7, column=0, sticky="w")

    button = tkinter.Button(labelf, text="검색", overrelief="solid", width=15, command=calc)
    button.grid(row=8, column=1, sticky="e")

    rest = tkinter.Button(labelf, text="항목 초기화", overrelief="solid", width=15, command=del_calc)
    rest.grid(row=8, column=0, sticky="w")

    nullnum3=tkinter.Label(labelf, text="", height=4, bg='RoyalBlue4')
    nullnum3.grid(row=9, column=0, sticky="w")

    relf=tkinter.Label(window, text="거래 목록 수정 (주문, 환불 선택)", width=37, height=2, bg='Slategray1', relief="ridge")
    relf.place(x=620, y=355)

    b1 = tkinter.Button(labelf, text='주문', overrelief="solid", width=15, state=tkinter.DISABLED, pady=3, command=add)
    b1.grid(row=11, column=1, sticky="se")
    b2 = tkinter.Button(labelf, text='환불', overrelief="solid", width=15, state=tkinter.DISABLED, pady=3, command=delete)
    b2.grid(row=11, column=0, sticky="se")

    #------------- 목록 분류 ----------------
    bookla=tkinter.Label(window, text="물류 목록 보러 가기                   ", width=27, height=7, fg="blue", bg='skyblue', relief="ridge", anchor="nw", pady=10)
    bookla.place(x=10, y=109) #160 365

    buttonT = tkinter.Button(window, text="물류 목록", overrelief="solid", width=8, state=tkinter.DISABLED, command=totalInfo) #물류 전체 목록
    buttonT.place(x=135, y=115)

    buttonB = tkinter.Button(window, text="도서 관리", overrelief="solid", width=8, state=tkinter.DISABLED, command=bookInfo) #도서목록
    buttonB.place(x=135, y=160)

    buttonS = tkinter.Button(window, text="문구 관리", overrelief="solid", width=8, state=tkinter.DISABLED, command=stnrInfo) #문구목록
    buttonS.place(x=135, y=205)

    costla=tkinter.Label(window, text="회원 목록 보러 가기                   ", width=27, height=2, fg="blue", bg='skyblue', relief="ridge")
    costla.place(x=10, y=255)

    buttonC = tkinter.Button(window, text="회원 목록", overrelief="solid", width=8, state=tkinter.DISABLED, command=custlist)
    buttonC.place(x=135, y=261)

    costla=tkinter.Label(window, text="재정 관리 보러 가기                   ", width=27, height=2, fg="blue", bg='skyblue', relief="ridge")
    costla.place(x=10, y=300)

    buttonF = tkinter.Button(window, text="재정 목록", overrelief="solid", width=8, state=tkinter.DISABLED, command=finInfo)
    buttonF.place(x=135, y=305)

    costla=tkinter.Label(window, text="사원 관리하기", width=19, height=3, fg="red", bg='skyblue', relief="ridge", anchor="n", pady=13, font=font3)
    costla.place(x=10, y=365)

    buttonM = tkinter.Button(window, text="사원 목록", overrelief="solid", width=15, height=2, state=tkinter.DISABLED, command=memInfo)
    buttonM.place(x=50, y=405)

    # 버튼 권한 설정
    if (userAut == "Human Res"):
        b1['state'] = tkinter.NORMAL
        b2['state'] = tkinter.NORMAL
        buttonT['state'] = tkinter.NORMAL
        buttonB['state'] = tkinter.NORMAL
        buttonS['state'] = tkinter.NORMAL
        buttonC['state'] = tkinter.NORMAL
        buttonF['state'] = tkinter.NORMAL
        buttonM['state'] = tkinter.NORMAL
    elif (userAut=="Marketing"):
        buttonT['state'] = tkinter.NORMAL
        buttonB['state'] = tkinter.NORMAL
        buttonS['state'] = tkinter.NORMAL
    
    #---------------------------표 만들기---------------------------------------

    treeview=tkinter.ttk.Treeview(window, columns=["zero", "one", "two", "tree"], displaycolumns=["zero", "one", "two", "tree"], height=16)
    treeview.place(x=210, y=109)

    treeview.column("zero", width=100, anchor="center")
    treeview.heading("zero", text="물류코드", anchor="center")

    treeview.column("one", width=100, anchor="center")
    treeview.heading("one", text="구분", anchor="center")

    treeview.column("two", width=100, anchor="center")
    treeview.heading("two", text="거래금액", anchor="center")

    treeview.column("tree", width=100, anchor="center")
    treeview.heading("tree", text="거래수량", anchor="center")

    treeview["show"]="headings"

    conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
    cursor = conn.cursor()

    cursor.execute('SELECT INDX, DIVI, TRPRICE, SCALE FROM finance;')

    for infom in cursor.fetchall():
        treeview.insert('','end', text="", values=infom, iid=infom)
        
    conn.close()
    
    window.mainloop()


#=======================================로그아웃 페이지==========================================================
def log_pro():
    def MsgErr4():
        tkinter.messagebox.showerror("로그인 실패", "존재하지 않은 아이디 혹은 비밀번호 입니다\n(다시 입력해주세요)")
    
    login2 = Tk()
    login2.title("로그인")
    login2.geometry("350x200+400+200")
    login2.resizable(False, False)

    global user_id, password
    user_id2, password2 = StringVar(), StringVar()
    
    user_id = user_id2
    password = password2
    
    def check_data():
        sc2 = False
        conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
        cursor = conn.cursor()
        cursor.execute('SELECT STID, PWD FROM loginID;')
        
        for idd in cursor.fetchall():
            if idd[0] == user_id2.get() and idd[1] == password2.get():
                print("로그인 성공")
                sc2=True
                login2.destroy()
                mainWin() 
        if sc2 is False:        
            print("로그인 실패") 
            MsgErr4()
            
    font=tkinter.font.Font(family="맑은 고딕", size=13, weight="bold")
    font2=tkinter.font.Font(family="맑은 고딕", size=10, weight="bold")

    # id와 password, 그리고 확인 버튼의 UI를 만드는 부분
    maintit2=tkinter.Label(login2, text="", width=150, height=30, bg='RoyalBlue4')
    maintit2.place(x=0, y=0)
    maintit=tkinter.Label(login2, text="", width=150, height=4, bg='Slategray1')
    maintit.place(x=0, y=0)
    idbg=tkinter.Label(login2, text="", width=46, height=5, bg='skyblue', relief="ridge")
    idbg.place(x=10, y=77)
    
    tkinter.Label(login2, text = "안양문고 시스템", height=2, bg='Slategray1', font=font).grid(row = 0, column = 1, padx = 10, pady = 10)
    tkinter.Label(login2, text = "- 정상적으로 로그아웃 되었습니다 -", fg='red', bg='Slategray1', font=font2).place(x=75, y=0)
    tkinter.Label(login2, text = "ID : ", bg='skyblue').grid(row = 1, column = 0, padx = 30, pady = 10)
    tkinter.Label(login2, text = "PW : ", bg='skyblue').grid(row = 2, column = 0, padx = 30, pady = 10)
    tkinter.Entry(login2, textvariable = user_id2).grid(row = 1, column = 1, padx = 10, pady = 10)
    tkinter.Entry(login2, textvariable = password2, show="*").grid(row = 2, column = 1, padx = 10, pady = 10)
    tkinter.Button(login2, text = "Login", width=8, command = check_data).grid(row = 2, column = 2, padx = 10, pady = 10)
    
    login2.mainloop()
#------------------------- 로그인 페이지 -------------------------------------

def MsgErr4():
    tkinter.messagebox.showerror("로그인 실패", "존재하지 않은 아이디 혹은 비밀번호 입니다\n(다시 입력해주세요)")
# tkinter 객체 생성
login = Tk()
login.title("로그인")
login.geometry("350x200+400+200")
login.resizable(False, False)

# 사용자 id와 password를 저장하는 변수 생성
user_id, password = StringVar(), StringVar()
# 로그인 성공 여부 확인 변수

def check_data():
    sc = False
    conn = pymssql.connect(host="127.0.0.1", database='erp', user='younsoo', password='carloveff35',  charset='utf8')
    cursor = conn.cursor()
    cursor.execute('SELECT STID, PWD FROM loginID;')
    for idd in cursor.fetchall():
        if idd[0] == user_id.get() and idd[1] == password.get():
            print("로그인 성공")
            sc=True
            login.destroy()
            mainWin() 
    if sc is False:        
        print("로그인 실패") 
        MsgErr4()
        
font=tkinter.font.Font(family="맑은 고딕", size=13, weight="bold")
font2=tkinter.font.Font(size=8, weight="bold")
font3=tkinter.font.Font(size=8, weight="bold")

# id와 password, 그리고 확인 버튼의 UI를 만드는 부분
maintit2=tkinter.Label(login, text="", width=150, height=30, bg='RoyalBlue4')
maintit2.place(x=0, y=0)
maintit=tkinter.Label(login, text="", width=150, height=4, bg='Slategray1')
maintit.place(x=0, y=0)
idbg=tkinter.Label(login, text="", width=46, height=5, bg='skyblue', relief="ridge")
idbg.place(x=10, y=77)
tkinter.Label(login, text = "안양문고 시스템", height=2, bg='Slategray1', font=font).grid(row = 0, column = 1, padx = 10, pady = 10)
tkinter.Label(login, text = "ID : ", bg='skyblue').grid(row = 1, column = 0, padx = 30, pady = 10)
tkinter.Label(login, text = "PW : ", bg='skyblue').grid(row = 2, column = 0, padx = 30, pady = 10)
iden=tkinter.Entry(login, textvariable = user_id)
iden.grid(row = 1, column = 1, padx = 10, pady = 10)
pwen=tkinter.Entry(login, textvariable = password, show="*")
pwen.grid(row = 2, column = 1, padx = 10, pady = 10)
tkinter.Button(login, text = "Login", width=8, command = check_data).grid(row = 2, column = 2, padx = 10, pady = 10)

login.mainloop() 