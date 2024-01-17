from excel_to_sql import Timetable
from data.create_testKeys import create_keys


tb = Timetable()
# Запуск функции
tb.process_control((5, 11), file_name='Расписание')
create_keys()