import io
import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QApplication, QMessageBox

from UI import main_ui, addEditCoffeeForm_ui

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = main_ui.Ui_Form()
        self.ui.setupUi(self)
        self.load_data()
        self.ui.addButton.clicked.connect(self.open_add_form)
        self.ui.editButton.clicked.connect(self.open_edit_form)

    def load_data(self):
        connection = sqlite3.connect('data/coffee_guide.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]

        self.ui.tableWidget.setRowCount(len(rows))
        self.ui.tableWidget.setColumnCount(len(column_names))
        self.ui.tableWidget.setHorizontalHeaderLabels(column_names)

        for row_index, row_data in enumerate(rows):
            for column_index, item in enumerate(row_data):
                self.ui.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(item)))

        connection.close()

    def open_add_form(self):
        self.ui.add_edit_form = AddEditForm(self)
        self.ui.add_edit_form.show()

    def open_edit_form(self):
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            coffee_id = self.ui.tableWidget.item(selected_row, 0).text()
            self.ui.add_edit_form = AddEditForm(self, coffee_id)
            self.ui.add_edit_form.show()
        else:
            QMessageBox.warning(self, "Warning", "Please select a coffee entry to edit.")


class AddEditForm(QWidget):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__()
        self.ui = addEditCoffeeForm_ui.Ui_Form()
        self.ui.setupUi(self)

        self.parent = parent
        self.coffee_id = coffee_id

        if coffee_id:
            self.load_coffee_data(coffee_id)

        self.ui.saveButton.clicked.connect(self.save_coffee)

    def load_coffee_data(self, coffee_id):
        connection = sqlite3.connect('data/coffee_guide.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coffee WHERE ID=?", (coffee_id,))
        coffee_data = cursor.fetchone()

        if coffee_data:
            self.ui.sortLineEdit.setText(coffee_data[1])
            self.ui.roastingLineEdit.setText(coffee_data[2])
            self.ui.conditionLineEdit.setText(coffee_data[3])
            self.ui.tasteDesriptionLineEdit.setText(coffee_data[2])
            self.ui.costLineEdit.setText(str(coffee_data[3]))
            self.ui.volumeLineEdit.setText(str(coffee_data[3]))

        connection.close()

    def save_coffee(self):
        sort = self.ui.sortLineEdit.text()
        roasting = self.ui.roastingLineEdit.text()
        condition = self.ui.conditionLineEdit.text()
        description = self.ui.tasteDesriptionLineEdit.text()
        cost = self.ui.costLineEdit.text()
        volume = self.ui.volumeLineEdit.text()

        connection = sqlite3.connect('data/coffee_guide.db')
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
