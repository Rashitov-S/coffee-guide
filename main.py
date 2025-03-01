import io
import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QApplication, QMessageBox

template = open("main.ui", mode="r", encoding="utf-8").read()

template_add_edit = open("addEditCoffeeForm.ui", mode="r", encoding="utf-8").read()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.load_data()
        self.addButton.clicked.connect(self.open_add_form)
        self.editButton.clicked.connect(self.open_edit_form)

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

    def open_add_form(self):
        self.add_edit_form = AddEditForm(self)
        self.add_edit_form.show()

    def open_edit_form(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            coffee_id = self.tableWidget.item(selected_row, 0).text()
            self.add_edit_form = AddEditForm(self, coffee_id)
            self.add_edit_form.show()
        else:
            QMessageBox.warning(self, "Warning", "Please select a coffee entry to edit.")


class AddEditForm(QWidget):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__()
        f = io.StringIO(template_add_edit)
        uic.loadUi(f, self)

        self.parent = parent
        self.coffee_id = coffee_id

        if coffee_id:
            self.load_coffee_data(coffee_id)

        self.saveButton.clicked.connect(self.save_coffee)

    def load_coffee_data(self, coffee_id):
        connection = sqlite3.connect('coffee_guide.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coffee WHERE ID=?", (coffee_id,))
        coffee_data = cursor.fetchone()

        if coffee_data:
            self.sortLineEdit.setText(coffee_data[1])
            self.roastingLineEdit.setText(coffee_data[2])
            self.conditionLineEdit.setText(coffee_data[3])
            self.tasteDesriptionLineEdit.setText(coffee_data[2])
            self.costLineEdit.setText(str(coffee_data[3]))
            self.volumeLineEdit.setText(str(coffee_data[3]))

        connection.close()

    def save_coffee(self):
        sort = self.sortLineEdit.text()
        roasting = self.roastingLineEdit.text()
        condition = self.conditionLineEdit.text()
        description = self.tasteDesriptionLineEdit.text()
        cost = self.costLineEdit.text()
        volume = self.volumeLineEdit.text()

        connection = sqlite3.connect('coffee_guide.db')
        cursor = connection.cursor()

        if self.coffee_id:
            cursor.execute(
                "UPDATE coffee SET sort=?, roasting=?, condition=?, taste_description=?, cost=?, volume=? WHERE ID=?",
                (sort, roasting, condition, description, cost, volume, self.coffee_id))
        else:
            cursor.execute(
                "INSERT INTO coffee (sort, roasting, condition, taste_description, cost, volume) VALUES (?, ?, ?, ?, ?, ?)",
                (sort, roasting, condition, description, cost, volume))

        connection.commit()
        connection.close()

        self.parent.load_data()
        self.close()

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
