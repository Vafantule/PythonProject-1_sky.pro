import functools
import os
from datetime import datetime
from typing import TypeVar, Callable, Optional

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


def log(filename: Optional[str] = None) -> (
        Callable)[[Callable[..., variable_type_t]], Callable[..., variable_type_t]]:
    """
    Декоратор, который выводит выполнение функции
    в файл (если указан filename)
    или консоль (если filename=None).
    :param filename: Файл с событиями при вызове функции.
    :return:
    """
    def decorator(function_log: Callable[..., variable_type_t]) -> (
            Callable)[..., variable_type_t]:
        """
        Оборачивание выполнения функции создания логирования.
        :param function_log:
        :return:
        """
        @functools.wraps(function_log)
        def wrapper(*args: any, **kwargs: any) -> variable_type_t:
            """
            Запись данных в лог-файл. Функция.
            :param args, kwargs: Аргументы, передаваемые в декорируемую функцию.
            :return: Результат выполнения декорируемой функции.
            """
            func_name = function_log.__name__
            try:
                # Выполняем функцию и сохраняем результат
                result = function_log(*args, **kwargs)
                log_message = (f"• {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} →"
                               f" {func_name}. OK.")

                # Записываем лог в файл или консоль
                if filename:
                    write_log_to_file(log_message, filename)
                else:
                    print(log_message)
                return result
            except Exception as error:
                # Формируем сообщение об ошибке
                log_message = (f"• {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} → "
                               f"{func_name}. Error: {type(error).__name__}. Inputs: {args}, {kwargs}")

                # Записываем лог в файл или консоль
                if filename:
                    write_log_to_file(log_message, filename)
                else:
                    print(log_message)

                # Перебрасываем исключение
                raise
        return wrapper
    return decorator


# Пример использования при указанном файле mylog.txt либо нет.
@log(filename=None)
def function_for_test_log(a: any, b: any) -> any:
    return a + b


@log(filename="mylog.txt")
def faulty_function_for_test_log(x: any) -> any:
    return x / 0


# Тестирование
# if __name__ == "__main__":
#     # Тест успешного выполнения
#     try:
#         function_for_test_log(1, 2)
#     except Exception:
#         pass
#
#     # Тест с ошибкой
#     try:
#         faulty_function_for_test_log(5)
#     except Exception:
#         pass
