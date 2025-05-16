import os
from typing import TypeVar


variable_type_t  = TypeVar('variable_type_t')

def write_log_to_file(log_message: str, filename: str) -> None:
    """
    Записывает лог в файл mylog_%n%
    .txt при ошибке.
    :param log_message: Сообщение с выводимыми данными.
    :param filename: Файл для записи сообщений о выполнении работы.
    :return:
    """
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(log_message + "\n")
    except (PermissionError, OSError) as error:
        # Выводим сообщение об ошибке
        print(f"Ошибка записи в {filename}: {type(error).__name__}")

        # Пробуем создать новый файл mylog_n.txt
        number = 1
        while True:
            new_filename = f"mylog_{number}.txt"
            if not os.path.exists(new_filename):
                try:
                    with open(new_filename, "a", encoding="utf-8") as file:
                        file.write(log_message + "\n")
                    break
                except (PermissionError, OSError):
                    number += 1
                    continue
            number += 1
