import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QMessageBox, QComboBox, QRadioButton, QButtonGroup, QHBoxLayout
)
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
from pyairtable import Table
from collections import defaultdict

# Airtable configuration
TOKEN = os.environ["AIRTABLE_TOKEN"]
BASE_ID = 'appeKpwmbTIiH15Vw'
TABLE_NAME = 'Inventory List'


class AirtableCleaner(QWidget):
    def __init__(self):
        super().__init__()

        # UI Setup
        self.setWindowTitle("Airtable Duplicates Remover")
        self.setGeometry(300, 300, 400, 250)
        layout = QVBoxLayout()

        self.info_label = QLabel("Select a field to identify duplicates and deletion method.")
        layout.addWidget(self.info_label)

        # Field selection dropdown
        self.field_selector = QComboBox()
        layout.addWidget(self.field_selector)

        # Fetch field names from Airtable
        self.populate_fields()

        # Deletion method selection
        method_layout = QHBoxLayout()
        self.oldest_radio = QRadioButton("Delete Oldest")
        self.newest_radio = QRadioButton("Delete Newest")
        self.oldest_radio.setChecked(True)  # Default to deleting oldest
        method_layout.addWidget(self.oldest_radio)
        method_layout.addWidget(self.newest_radio)
        layout.addLayout(method_layout)

        # Grouping radio buttons
        self.method_group = QButtonGroup()
        self.method_group.addButton(self.oldest_radio)
        self.method_group.addButton(self.newest_radio)

        # Delete button
        self.delete_button = QPushButton("Delete Duplicates")
        self.delete_button.clicked.connect(self.delete_duplicates)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)
        self.apply_gray_theme()

    def apply_gray_theme(self):
        # Apply a custom stylesheet for the gray theme
        self.setStyleSheet("""
            QWidget {
                background-color: #353535;
                color: #FFFFFF;
                font-size: 14px;
            }
            QComboBox, QPushButton, QRadioButton {
                background-color: #4C4C4C;
                border: 1px solid #AAAAAA;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #4C4C4C;
                selection-background-color: #777777;
            }
            QPushButton:hover {
                background-color: #5A5A5A;
            }
            QRadioButton::indicator {
                border: 1px solid #AAAAAA;
                background-color: #4C4C4C;
            }
            QRadioButton::indicator:checked {
                background-color: #777777;
            }
            QLabel {
                font-size: 16px;
            }
        """)

    def populate_fields(self):
        table = Table(TOKEN, BASE_ID, TABLE_NAME)
        # Fetch the fields of the first record to get the keys
        for records in table.iterate():
            fields = records[0].get("fields").keys()
            self.field_selector.addItems(fields)
            break

    def delete_duplicates(self):
        table = Table(TOKEN, BASE_ID, TABLE_NAME)
        selected_field = self.field_selector.currentText()
        print(f"Selected: {selected_field}")
        delete_oldest = self.oldest_radio.isChecked()

        # Fetch all records
        all_records = table.all()

        # Dictionary to store records by their unique identifying field
        records_map = defaultdict(list)
        duplicate_ids = []

        for record in all_records:
            unique_field_value = record['fields'].get(selected_field)
            print(f"Unique: {unique_field_value}")
            if unique_field_value:
                records_map[unique_field_value].append(record)

        # Identify and handle duplicates
        for records in records_map.values():
            if len(records) > 1:
                # Sort records by creation time
                records.sort(key=lambda x: x['createdTime'], reverse=not delete_oldest)
                # Keep the first record, mark others as duplicates
                duplicate_ids.extend([record['id'] for record in records[1:]])

        # Delete duplicates
        for record_id in duplicate_ids:
            table.delete(record_id)

        # Show confirmation
        if duplicate_ids:
            QMessageBox.information(self, "Success", f"Deleted {len(duplicate_ids)} duplicate records.")
        else:
            QMessageBox.warning(self, "No Duplicates found", f"Duplicates not found in the '{selected_field}' field")


def main():
    app = QApplication(sys.argv)
    cleaner = AirtableCleaner()
    cleaner.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
