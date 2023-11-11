from excel_to_sql import process_control
from data.create_testKeys import create_keys

# Запуск функции
process_control((5, 11), file_name='Расписание')
create_keys()
