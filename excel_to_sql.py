import os
import sqlite3
import openpyxl


def export_to_sqlite():
    '''Экспорт данных из xlsx в sqlite'''

    # 1. Создание и подключение к базе
    # Получаем текущую папку проекта
    prj_dir = os.path.abspath(os.path.curdir)
    a = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Имя базы
    base_name = 'timetable.sqlite3'
    # метод sqlite3.connect автоматически создаст базу, если ее нет
    connect = sqlite3.connect(prj_dir + '/' + base_name)
    # курсор - это специальный объект, который делает запросы и получает результаты запросов
    cursor = connect.cursor()
    # создание таблицы если ее не существует
    cursor.execute('CREATE TABLE IF NOT EXISTS timetables (lesson_pos, lesson, cabinet, class_letter, day)')

    # 2. Работа c xlsx файлом
    # Читаем файл и лист1 книги excel
    file_to_read = openpyxl.load_workbook('Расписание.xlsx', data_only=True)
    sheet = file_to_read['5 класс']
    # Циxкл по строкам начиная со второй (в первой заголовки)
    classes = [sheet.cell(1, col).value for col in range(1, 21) if sheet.cell(1, col).value]
    count_days = 0
    count_letters = 0
    for row in range(2, sheet.max_row + 1):
        count_days += 1
        if count_days == 1:
            day = sheet.cell(row, 1).value
        elif count_days % 9 == 0:
            day = sheet.cell(row, 1).value
            count_days = 1
        # Объявление списка
        data = []
        count_columns = 0
        # Цикл по столбцам от 1 до 4 ( 22 не включая)
        for col in range(2, 21):
            count_columns += 1
            # value содержит значение ячейки с координатами row col
            value = sheet.cell(row, col).value
            # Список который мы потом будем добавлять
            data.append(value)
            if count_columns == 3:
                data.append(classes[count_letters])
                count_letters += 1
                count_columns = 0
                data.append(day)
                cursor.execute("INSERT INTO timetables VALUES (?, ?, ?, ?, ?);",
                               (data[0], data[1], data[2], data[3], data[4]))
                data = []
        count_letters = 0
    # 3. Запись в базу и закрытие соединения
        # Вставка данных в поля таблицы

    # сохраняем изменения
    connect.commit()
    # закрытие соединения
    connect.close()


def clear_base():
    '''Очистка базы sqlite'''

    # Получаем текущую папку проекта
    prj_dir = os.path.abspath(os.path.curdir)

    # Имя базы
    base_name = 'timetables.sqlite3'

    connect = sqlite3.connect(prj_dir + '/' + base_name)
    cursor = connect.cursor()

    # Запись в базу, сохранение и закрытие соединения
    cursor.execute("DELETE FROM timetables")
    connect.commit()
    connect.close()


# Запуск функции
export_to_sqlite()