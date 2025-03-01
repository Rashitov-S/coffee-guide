import io
import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QApplication

template = open("main.ui", mode="r", encoding="utf-8").read()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect('coffee_guide.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)

        for row_index, row_data in enumerate(rows):
            for column_index, item in enumerate(row_data):
                self.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(item)))

        connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
