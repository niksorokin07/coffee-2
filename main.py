import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Message(QWidget):
    def __init__(self, titles):
        super().__init__()
        self.titles = titles
        uic.loadUi('addEditCoffeeForm.ui', self)  # Загружаем дизайн
        self.add.clicked.connect(self.addition)
        self.change_2.clicked.connect(self.alteration)

    def addition(self):
        try:
            if str(self.price.text()).isdigit() and str(self.volume.text()).isdigit():
                con = sqlite3.connect('coffee.sqlite')
                cur = con.cursor()
                res = cur.execute("""SELECT * FROM Coffee""").fetchall()[::-1][0][0]
                print(res)
                cur.execute(f"INSERT INTO coffee VALUES(?, ?, ?, ?, ?, ?, ?);",
                            (int(res) + 1, self.name.text(), self.fried.text(), self.type.text(),
                             self.taste.text(), int(self.price.text()), int(self.volume.text())))
                con.commit()
                con.close()
                MyWidget.update_result(form1)
                self.close()
            else:
                print(str(self.price.text()).isdigit(), str(self.volume.text()).isdigit())
                self.error.setText('Данные о добавлении товара неверны')
        except Exception as e:
            print(e)

    def alteration(self):
        try:
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            cur.execute(f"""UPDATE Coffee SET {self.name_change.text()} = '{self.change.text()}'
             WHERE ID = {self.id_change.text()}""")
            con.commit()
            con.close()
            MyWidget.update_result(form1)
            self.close()
        except Exception as e:
            self.error.setText('Данные об изменении товара неверны')
            print(e)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        global form1
        form1 = self
        uic.loadUi("main.ui", self)
        self.ac.clicked.connect(self.message)
        self.con = sqlite3.connect("coffee.sqlite")
        self.modified = {}
        self.connection = sqlite3.connect("coffee.sqlite")
        self.cur = self.connection.cursor()
        self.result = self.cur.execute(f"SELECT * FROM Coffee").fetchall()
        self.titles = [el[0] for el in self.cur.description]
        self.cur.close()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, row in enumerate(self.result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def message(self):
        try:
            self.msg = Message(self.titles)
            self.msg.show()
        except Exception as e:
            print(e)

    def update_result(self):
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.result = self.cur.execute("""SELECT * FROM Coffee""").fetchall()
        self.con.commit()
        self.con.close()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, row in enumerate(self.result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.modified = {}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
