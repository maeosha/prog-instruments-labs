import sys
import os

from PyQt6.QtWidgets import (QMainWindow,
                             QPushButton,
                             QListView,
                             QLabel,
                             QTextBrowser,
                             QMenuBar,
                             QMenu,
                             QMessageBox,
                             QFileDialog,
                             QInputDialog,
                             QApplication)
from enum import Enum
from multiprocessing import Process

from Lab2.content import start_work
from Lab2.content import next_iter


class ProcessingMethod(Enum):
    annotation = "Сreating an annotation"
    default_data = "Creating a copy"
    random_data = "Creating a random date"


class IterWindow(QMainWindow):
    def __init__(self):
        """Creating an iterator window"""
        super().__init__()

        self.count: dict[int, int] = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
        self.fname: str = ""

        self.text1 = QLabel(self)
        self.setFixedSize(840, 525)
        self.setWindowTitle("My App2")
        zero_stars_btn = QPushButton(self)
        zero_stars_btn.setGeometry(2, 412, 139, 81)
        zero_stars_btn.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        zero_stars_btn.setText("0 stars:\n next elem")

        one_stars_btn = QPushButton(self)
        one_stars_btn.setGeometry(142, 412, 139, 81)
        one_stars_btn.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        one_stars_btn.setText("1 stars:\n next elem")

        two_stars_btn = QPushButton(self)
        two_stars_btn.setGeometry(282, 412, 139, 81)
        two_stars_btn.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        two_stars_btn.setText("2 stars:\n next elem")

        three_stars_btn = QPushButton(self)
        three_stars_btn.setGeometry(422, 412, 139, 81)
        three_stars_btn.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        three_stars_btn.setText("3 stars:\n next elem")

        four_stars_btn = QPushButton(self)
        four_stars_btn.setGeometry(562, 412, 139, 81)
        four_stars_btn.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        four_stars_btn.setText("4 stars:\n next elem")

        five_stars_btn = QPushButton(self)
        five_stars_btn.setGeometry(702, 412, 136, 81)
        five_stars_btn.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        five_stars_btn.setText("5 stars:\n next elem")

        go_back_btn = QPushButton(self)
        go_back_btn.setGeometry(2, 494, 836, 29)
        go_back_btn.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        go_back_btn.setText("Go back")

        path_list_full = QListView(self)
        path_list_full.setGeometry(2, 24, 836, 71)

        self.text_list_full = QTextBrowser(self)
        self.text_list_full.setGeometry(2, 98, 836, 311)

        path_list = QTextBrowser(self)
        path_list.setGeometry(2, 22, 836, 30)

        path_label_info = QLabel(self)
        path_label_info.setGeometry(2, 22, 836, 30)
        path_label_info.setText("Path to elem:")
        path_label_info.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        path_label_info.setMargin(6)


        self.path_label = QLabel(self)
        self.path_label.setGeometry(2, 51, 836, 43)
        self.path_label.setText("")
        self.path_label.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.path_label.setMargin(6)


        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        open_the_annotation = QMenu("&Open the annotation", self)
        menubar.addMenu(open_the_annotation)

        open_the_data_set = open_the_annotation.addAction("&Open the annotation", self.open_csv)
        zero_stars_btn.clicked.connect(self.next_elem)
        one_stars_btn.clicked.connect(self.next_elem)
        two_stars_btn.clicked.connect(self.next_elem)
        three_stars_btn.clicked.connect(self.next_elem)
        four_stars_btn.clicked.connect(self.next_elem)
        five_stars_btn.clicked.connect(self.next_elem)
        go_back_btn.clicked.connect(self.go_back)


    def open_csv(self):
        """Open a csv file"""
        self.fname: str = QFileDialog.getOpenFileNames(self)[0]
        self.path_label.setText(f"{self.fname[0]} had been opened")

    def next_elem(self):
        """Getting the next iterator element"""
        if self.fname == "":
            QMessageBox.warning(self, "Warning", "First, give access to the .csv fail!")
        else:
            stars = self.sender().text()
            stars = int(stars[0])
            text = ''
            fail_info: list = next_iter(self.fname[0], stars, self.count.get(stars))
            self.path_label.setText(fail_info[0])
            for line in fail_info[1]:
                text += line
            self.text_list_full.setText(text)
            self.count[stars] += 1

    def go_back(self):
        """Return to the main window"""
        self.main_window = MainWindow()
        self.close()
        self.main_window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        """A window with the creation of an annotation and a copy of data"""
        super().__init__()

        self.fname = ""

        self.setFixedSize(800, 230)
        self.setWindowTitle("My App1")

        path_list = QListView(self)
        path_list.setGeometry(2, 25, 796, 95)

        pushbutton_csv = QPushButton(self)
        pushbutton_csv.setGeometry(0, 120, 200, 101)
        pushbutton_csv.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        pushbutton_csv.setText("Сreating an annotation")

        pushbutton_copy = QPushButton(self)
        pushbutton_copy.setGeometry(200, 120, 200, 101)
        pushbutton_copy.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        pushbutton_copy.setText("Creating a copy")

        pushbutton_random = QPushButton(self)
        pushbutton_random.setGeometry(400, 120, 200, 101)
        pushbutton_random.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        pushbutton_random.setText("Creating a random date")

        pushbutton_iterator = QPushButton(self)
        pushbutton_iterator.setGeometry(600, 120, 200, 101)
        pushbutton_iterator.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        pushbutton_iterator.setText("Iterator")

        self.btn_clicker = IterWindow()

        self.path_label = QLabel(self)
        self.path_label.setGeometry(0, 25, 796, 95)
        self.path_label.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.path_label.setText("<html><head/><body><p align=\"center\">"
                           "No data available! To upload the data for further processing, click on the "
                           "&quot;""Open the data set&quot"
                           ";</p></body></html>")
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        open_the_data_set = QMenu("&Open_the_data_set", self)
        menubar.addMenu(open_the_data_set)

        open_the_data_set = open_the_data_set.addAction("&Open the data set", self.Open_data)

        pushbutton_csv.clicked.connect(self.all_functions)
        pushbutton_copy.clicked.connect(self.all_functions)
        pushbutton_random.clicked.connect(self.all_functions)
        pushbutton_iterator.clicked.connect(self.to_iter_page)

    def Open_data(self):
        """Open a file"""
        self.fname: str = QFileDialog.getExistingDirectory(self)
        self.path_label.setText("<html><head/><body><p align=\"center\">"
                           f"The {self.fname[self.fname.rfind('/') + 1:]} has been opened"
                           "</p></body></html>")

    def all_functions(self):
        """Create annotations and copies of data"""

        processing_method = self.sender().text()

        if self.fname == "":
            QMessageBox.warning(self, "Warning", "First, give access to the data!")

        else:
            file_name, ok = QInputDialog.getText(self, "The name of your file", "Enter the name of your file:")
            if file_name and ok:
                match processing_method:
                    case ProcessingMethod.annotation.value:
                        start_work([], self.fname, self.fname, file_name, 1)
                        self.path_label.setText("<html><head/><body><p align=\"center\">"
                                                f"The file {file_name}.csv was successfully created"
                                                "</p></body></html>")
                    case ProcessingMethod.default_data.value | ProcessingMethod.random_data.value:
                        random_list: list = list(range(0, 10000))
                        msg_box = QMessageBox(self)
                        msg_box.setWindowTitle("Save file")
                        msg_box.setText("Select the path where you want to save the new file:")
                        msg_box.setIcon(QMessageBox.Icon.Information)

                        msg_box.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel)
                        returnValue = msg_box.exec()
                        if returnValue == QMessageBox.StandardButton.Save:
                            path_to_dir: str = QFileDialog.getExistingDirectory(self)
                            csv_name = os.path.join(path_to_dir, file_name + ".csv")
                            new_dir_name = os.path.join(path_to_dir, file_name)

                            if processing_method == ProcessingMethod.default_data.value:
                                pr1 = Process(target=start_work, args=([], self.fname, new_dir_name, csv_name, 2))
                            else:
                                pr1 = Process(target=start_work, args=(random_list, self.fname, new_dir_name, csv_name, 3))
                            pr1.start()
                            pr1.join()

                            self.path_label.setText("<html><head/><body><p align=\"center\">"
                                                f"The file {file_name} was successfully created"
                                                "</p></body></html>")

                        if returnValue == QMessageBox.StandardButton.Cancel:
                            MainWindow()
            else:
                MainWindow()

    def to_iter_page(self):
        """Return to the return window"""
        self.iter_window = IterWindow()
        self.close()
        self.iter_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()