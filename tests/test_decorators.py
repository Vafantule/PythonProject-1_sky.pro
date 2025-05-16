import os
from datetime import datetime
from typing import Any, Callable, Generator, Optional, Union
from unittest.mock import patch

import pytest
from _pytest.capture import CaptureFixture

from src.decorators import log


@pytest.fixture
def log_decorators_write_to_temp_file(temp_file: str) -> Generator[None, Any, None]:
    """

    :param temp_file:
    :return:
    """
    temp_dir = os.path.dirname(temp_file)

    def write_log_to_temp_file(log_message: str, filename: str) -> None:
        try:
            with open(filename, "a", encoding="utf-8") as file:
                file.write(log_message + "\n")
        except (PermissionError, OSError) as error:
            # Выводим сообщение об ошибке
            print(f"Ошибка записи в {filename}: {type(error).__name__}")

            # Пробуем создать новый файл mylog_n.txt
            number = 1
            while True:
                new_filename = os.path.join(temp_dir, f"mylog_{number}.txt")
                print(f"Попытка записи в {new_filename}")
                if not os.path.exists(new_filename):
                    try:
                        with open(new_filename, "a", encoding="utf-8") as file:
                            file.write(log_message + "\n")
                        print(f"Успешная запись в {new_filename}")
                        break
                    except (PermissionError, OSError):
                        print(f"Ошибка записи в {new_filename}: {type(error).__name__}")
                        number += 1
                        continue
                number += 1
    with patch("src.decorators.write_log_to_file", write_log_to_temp_file):
        yield


@pytest.fixture
def decorated_function() -> Callable[[Optional[str], str], Callable[..., Any]]:
    """

    :return:
    """
    def create_function(filename: Optional[str], function_type: str) -> (
            Callable)[..., Union[str, None]]:
        if function_type == "success":
            @log(filename=filename)
            def test_function_log(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> str:
                return "success"
            return test_function_log
        elif function_type == "value_error":
            @log(filename=filename)
            def test_function_log(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
                raise ValueError("Тестирование ошибки значения.")
            return test_function_log
        elif function_type == "zero_division_error":
            @log(filename=filename)
            def test_function_log(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
                raise ZeroDivisionError("Тестирование ошибки деления на 0.")
            return test_function_log
        elif function_type == "type_error":
            @log(filename=filename)
            def test_function_log(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
                raise TypeError("Тестирование ошибки типа данных.")
            return test_function_log
        else:
            raise ValueError("Не правильный тип функции")
    return create_function


@pytest.mark.parametrize("filename_type", ["console", "file"])
@pytest.mark.parametrize("function_type, expected", [
    ("success", None),
    ("value_error", ValueError),
    ("zero_division_error", ZeroDivisionError),
    ("type_error", TypeError),
])
@pytest.mark.parametrize("args_kwargs", [
    ((), {}),  # Пустые args и kwargs
    ((1, 2), {"x": 3.14}),  # Числа
    (("hello", "world"), {"name": "Alice"}),  # Строки
    (([1, 2], [3, 4]), {"items": [5, 6]}),  # Списки
    ((1, "test", [7, 8]), {"num": 9, "text": "mixed"})  # Смешанные типы
])
def test_function_log_execution(
        temp_file: str,
        capsys: CaptureFixture[str],
        decorated_function: Callable,
        filename_type: str,
        function_type: str,
        expected: Optional[type],
        args_kwargs: tuple
) -> None:
    """

    :param temp_file:
    :param capsys:
    :param decorated_function:
    :param filename_type:
    :param function_type:
    :param expected:
    :param args_kwargs:
    :return:
    """
    filename = None if filename_type == "console" else temp_file
    args, kwargs = args_kwargs

    function_log = decorated_function(filename, function_type)
    expected_log = (
        f"• {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} → "
        f"{function_log.__name__}. OK." if function_type == "success"
        else f"• {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} → {function_log.__name__}. Error: "
             f"{expected.__name__ if expected else 'None'}. Inputs: {args}, {kwargs}"

    )

    if expected:
        with pytest.raises(expected):
            function_log(*args, **kwargs)
    else:
        result = function_log(*args, **kwargs)
        assert result == "success"

    if filename_type == "console":
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_log
    else:
        with open(temp_file, "r", encoding="utf-8") as file:
            log_content = file.read().strip()
        assert log_content == expected_log


@pytest.mark.parametrize("error_type", [PermissionError, OSError])
def test_file_write_error(
        temp_file: str,
        capsys: CaptureFixture[str],
        mock_file_error: Callable,
        log_decorators_write_to_temp_file: None,
        # patched_log_decorator: None,
        error_type: type
) -> None:
    """

    :param temp_file:
    :param capsys:
    :param mock_file_error:
    :param log_decorators_write_to_temp_file:
    :param error_type:
    :return:
    """
    @log(filename=temp_file)
    def add(a: int, b: int) -> int:
        return a + b

    with mock_file_error(error_type):
        result = add(9, -4)
        assert result == 5
        captured = capsys.readouterr()
        assert f"Ошибка записи в {temp_file}: {error_type.__name__}" in captured.out

    temp_dir = os.path.dirname(temp_file)
    new_file = os.path.join(temp_dir, "mylog_1.txt")
    assert os.path.exists(new_file)
    with open(new_file, "r", encoding="utf-8") as file:
        log_content = file.read().strip()
    assert log_content.endswith(". OK.")

    created_files = [file for file in os.listdir(temp_dir) if
                     file.startswith("mylog_") and file.endswith(".txt")]
    assert len(created_files) == 1
    # assert created_files == ["mylog_1.txt"]


def test_unt8_encoding(temp_file: str) -> None:
    """
    Тестирование записи логов в файл с кодировкой UTF-8.
    :param temp_file: Файл temp для записи.
    :assert:
    """
    @log(filename=temp_file)
    def greet(name: str) -> str:
        return f"Mother, {name}!"

    result = greet("Anarchy")
    assert result == "Mother, Anarchy!"

    with open(temp_file, "r", encoding="utf-8") as file:
        log_content = file.read().strip()
    assert log_content == f"• {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} → greet. OK."

    with open(temp_file, "w", encoding="utf-8") as file:
        file.write("Проверка символов кириллицы\n")
    with open(temp_file, "r", encoding="utf-8") as file:
        assert file.read().strip() == "Проверка символов кириллицы"
