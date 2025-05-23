import functools
import os
from datetime import datetime
from typing import Callable, Optional, TypeVar, Any

VARIABLE_TYPE = TypeVar('VARIABLE_TYPE')
MAX_ATTEMPTS = 1000


def write_log_to_file(log_message: str, filename: str) -> None:
    """
    Записывает лог в файл mylog_%n%.txt при ошибке.
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
        while number <= MAX_ATTEMPTS:
            new_filename = os.path.join(os.path.dirname(filename), f"mylog_{number}.txt")
            if not os.path.exists(new_filename):
                try:
                    with open(new_filename, "a", encoding="utf-8") as file:
                        file.write(log_message + "\n")
                    break
                except (PermissionError, OSError):
                    number += 1
                    continue
            number += 1
        if number > MAX_ATTEMPTS:
            raise RuntimeError(f"Ошибка записи в mylog_n.txt после {MAX_ATTEMPTS} попыток.")


def log(filename: Optional[str] = None) -> (
        Callable)[[Callable[..., VARIABLE_TYPE]], Callable[..., VARIABLE_TYPE]]:
    """
    Декоратор, который выводит выполнение функции
    в файл (если указан filename)
    или консоль (если filename=None).
    :param filename: Файл с событиями при вызове функции.
    :return:
    """
    def decorator(function_log: Callable[..., VARIABLE_TYPE]) -> (
            Callable)[..., VARIABLE_TYPE]:
        """
        Оборачивание выполнения функции создания логирования.
        :param function_log:
        :return:
        """
        @functools.wraps(function_log)
        def wrapper(*args: Any, **kwargs: Any) -> VARIABLE_TYPE:
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
def function_for_test_log(a: Any, b: Any) -> Any:
    return a + b


@log(filename="mylog.txt")
def faulty_function_for_test_log(x: Any) -> Any:
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
