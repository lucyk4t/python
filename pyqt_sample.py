from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi  # Convert UI Xml information to Class
from sqlite3 import *
import sys

class Database:  # Data controlled by DB sql
    @staticmethod
    def createtable():
        try:
            sql = 'create table product(prodname varchar(20), cnt int, proddate varchar(20))'
            db = connect("prodmgmt.db")
            db.execute(sql)
            db.close()
        except Exception as err:
            pass

    @staticmethod
    def inputtable(name, cnt, date):
        data = (name, cnt, date)
        try:
            sql = 'insert into product(prodname, cnt, proddate) values(?, ?, ?)'
            db = connect("prodmgmt.db")
            cur = db.cursor()
            cur.execute(sql, data)
            db.commit()
            db.close()
        except Exception as err:
            print("err: ", err)

    @staticmethod
    def viewtable():
        try:
            sql = 'select * from product'
            db = connect("prodmgmt.db")
            cur = db.cursor()
            cur.execute(sql)
            dt = [n for n in cur]
            return dt
        except Exception as err:
            print("err: ", err)

    @staticmethod
    def searchtable(str):
        try:
            sql = "select * from product where prodname like '%" + str + "%'"
            db = connect("prodmgmt.db")
            cur = db.cursor()
            cur.execute(sql)
            dt = [n for n in cur]
            return dt
        except Exception as err:
            print("err: ", err)

    @staticmethod
    def updatetable(modiftext, modifcnt, smodifdate, cur):
        data = (modiftext, int(modifcnt), smodifdate, cur)
        try:
            sql = "update product set prodname=?, cnt=?, proddate=? where prodname=?"
            db = connect("prodmgmt.db")
            cur = db.cursor()
            cur.execute(sql, data)
            db.commit()
            db.close()
        except Exception as err:
            print("err: ", err)
            

class MyInputDlg:
    def __init__(self):
        self.ui = loadUi('input.ui')
        self.ui.inputpush.clicked.connect(self.btnclick)
        self.ui.exec()

    def btnclick(self):
        self.ui.close()


class MyModifyDlg:
    def __init__(self):
        self.ui = loadUi('modify.ui')
        self.ui.modifypush.clicked.connect(self.btnclick)
        self.ui.exec()

    def btnclick(self):
        self.ui.close()


class MySearchDlg:
    def __init__(self):
        self.ui = loadUi('search.ui')
        self.ui.searchpush.clicked.connect(self.btnclick)
        self.ui.exec()
    def btnclick(self):
        self.ui.close()


class mymain():
    def __init__(self):
        Database.createtable()
        self.ui = loadUi('homework.ui')  # return Dialog object
        self.list_initialization()
        self.ui.actionInput.triggered.connect(self.inputdlg)
        self.ui.actionView.triggered.connect(self.viewdlg)
        self.ui.actionModify.triggered.connect(self.modifydlg)
        self.ui.actionSearch.triggered.connect(self.searchdlg)
        self.ui.show()

    def addtabledata(self, name, cnt, date):  # Tablewidget
        n = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.setRowCount(n+1)
        self.ui.tableWidget.setItem(n, 0, QTableWidgetItem(name))
        self.ui.tableWidget.setItem(n, 1, QTableWidgetItem(str(cnt)))
        self.ui.tableWidget.setItem(n, 2, QTableWidgetItem(str(date)))

    # Select * from product
    def list_initialization(self):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(3)

        data = Database.viewtable()
        for name, cnt, date in data:
            self.addtabledata(name, cnt, date)

    # Select * from product where prodname=?
    def list_search(self, str):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(3)

        data = Database.searchtable(str)
        for name, cnt, date in data:
            self.addtabledata(name, cnt, date)

    def inputdlg(self):
        inputdlg = MyInputDlg()
        inptext = inputdlg.ui.inputproduct.text() # 제품명
        cntspin = inputdlg.ui.countspin.value() # 스핀 카운트
        prodate = inputdlg.ui.proddate.date() # 날짜
        sprodate = "%d-%d-%d" % (prodate.year(), prodate.month(), prodate.day())
        Database.inputtable(inptext, int(cntspin), sprodate)
        self.list_initialization()

    def viewdlg(self):
        self.list_initialization()

    def modifydlg(self):
        modifydlg = MyModifyDlg()

        try:
            curtext = modifydlg.ui.curprod.text()  # 수정해야할 제품명
            modiftext = modifydlg.ui.modifprod.text() # 수정하는 제품명
            modifcnt = modifydlg.ui.modifcount.value()  # 스핀 카운트
            modifdate = modifydlg.ui.modifdate.date()  # 날짜
            smodifdate = "%d-%d-%d" % (modifdate.year(), modifdate.month(), modifdate.day())

            Database.updatetable(modiftext, int(modifcnt), smodifdate, curtext)
            self.list_initialization()
        except Exception as e:
            print(e)

    def searchdlg(self):
        searchdlg = MySearchDlg()
        searchtext = searchdlg.ui.searchprod.text()
        self.list_search(searchtext)


def main():
    app = QApplication(sys.argv)  # Event 감시
    dlg = mymain()
    app.exec()

if __name__ == "__main__":
    main()
