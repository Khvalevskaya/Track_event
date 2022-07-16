from PyQt5.QtCore import QDate

from tracker import *

import pickle
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication




Form, Window = uic.loadUiType("trackerd.ui")

app = QApplication([])
window = Window()
form: object = Form()
form.setupUi(window)
window.show()


# создаем функцию, кот будет сохранять инфор. в файл (перед этим import pickle)
def save_to_file():
    global start_date, calk_date, description
    # start_date = QDate(2022,7,1)
    data_to_save = {"start": start_date, 'and': calk_date, "desc": description}
    file1 = open("config.txt", "wb")
    pickle.dump(data_to_save, file1)
    file1.close()



# создаем функцию, кот будет считывать  инфор. из файла
def read_from_file():
    global start_date, calk_date, description, now_date
    try:
        file1 = open("config.txt", "rb")
        data_to_load = pickle.load(file1)
        file1.close()
        start_date = data_to_load["start"]
        calk_date = data_to_load['and']
        description = data_to_load["desc"]
        print(start_date.toString("dd-MM-yyyy"), calk_date.toString("dd-MM-yyyy"), description)
        form.calendarWidget.setSelectedDate(calk_date)
        form.dateEdit.setDate(calk_date)
        form.textEdit.setPlainText(description)
        delta_days_left = start_date.daysTo(now_date)  # прошло дней
        delta_days_right = now_date.daysTo(calk_date)  # осталось дней
        days_total = start_date.daysTo(calk_date)  # всего дней
        print("$$$", delta_days_left, delta_days_right, days_total)
        procent = int(delta_days_left * 100 / days_total)
        print(procent)
        form.progressBar.setProperty("value", procent)
    except:
        print("Не могу прочитать файл(Может его нет)")


def on_click():
    global calk_date, description, start_date
    start_date = now_date
    calk_date = form.calendarWidget.selectedDate()
    description = form.textEdit.toPlainText()
    # print(form.dateEdit.dateTime().toString("dd-MM-yyyy"))
    # print(form.textEdit.toPlainText())
    print("Clicked!!!")
    save_to_file()
    # print(form.calendarWidget.selectedDate().toString("dd-MM-yyyy"))
    # date = QDate(2022,9,17)
    # form.calendarWidget.setSelectedDate(date)


def on_click_calendar():
    global start_date, calk_date
    # print(form.calendarWidget.selectedDate().toString("dd-MM-yyyy"))
    form.dateEdit.setDate(form.calendarWidget.selectedDate())
    calk_date = form.calendarWidget.selectedDate()
    delta_days = start_date.daysTo(calk_date)
    print(delta_days)
    form.label_3.setText("До наступления события осталось: %s дней" % delta_days)


def on_dateedit_change():
    print(form.dateEdit.dateTime().toString("dd-MM-yyyy"))
    form.calendarWidget.setSelectedDate(form.dateEdit.date())
    calk_date = form.dateEdit.date()
    delta_days = start_date.daysTo(calk_date)
    print(delta_days)
    form.label_3.setText("До наступления события осталось: %s дней" % delta_days)


form.pushButton.clicked.connect(on_click)
form.calendarWidget.clicked.connect(on_click_calendar)
form.dateEdit.dateChanged.connect(on_dateedit_change)

start_date = form.calendarWidget.selectedDate()
now_date = form.calendarWidget.selectedDate()
calk_date = form.calendarWidget.selectedDate()
description = form.textEdit.toPlainText()
read_from_file()

form.label.setText("Трекер события от %s" % start_date.toString("dd-MM-yyyy"))
on_click_calendar()

app.exec()


