import builtins
import os
import tempfile
from datetime import datetime
from typing import Any, Callable, Generator, Optional, Union
from unittest.mock import MagicMock, patch

import pytest
from _pytest.capture import CaptureFixture

from src.decorators import MAX_ATTEMPTS, log


@pytest.fixture
def temp_file() -> Generator[str, Any, None]:
    """
    Создание и удаление временных файлов для тестирования функций.
    :return:
    """
    temp = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")
    temp.close()

    temp_dir = os.path.dirname(temp.name)
    for file in os.listdir(temp_dir):
        if file.startswith("mylog_") and file.endswith(".txt"):
            os.remove(os.path.join(temp_dir, file))

    yield temp.name

    if os.path.exists(temp.name):
        os.remove(temp.name)
    for file in os.listdir(temp_dir):
        if file.startswith("mylog_") and file.endswith(".txt"):
            os.remove(os.path.join(temp_dir, file))


@pytest.fixture
def mock_file_error(temp_file: str) -> Callable[[type, bool], MagicMock]:
    """
    Имитация ошибки записи в файл для temp_file
    :param temp_file: Временный файл.
    :return:
    """
    def create_mock(error_type: type, all_files: bool = False) -> MagicMock:
        """
        Создание имитации ошибки.
        :param all_files:
        :param error_type: Тип ошибки.
        :return:
        """
        real_open = builtins.open

        def mock_open(*args: Any, **kwargs: Any) -> Any:
            # if args and args[0] == temp_file:
            if args:
                if args[0] == temp_file or (all_files and 'mylog_' in
                                            args[0] and args[0].endswith('.txt')):
                    raise error_type("Ложная ошибка")
            return real_open(*args, **kwargs)
        return patch("builtins.open", side_effect=mock_open)
    return create_mock


@pytest.fixture
def log_decorators_write_to_temp_file(temp_file: str) -> Generator[None, Any, None]:
    """
    Проверка создания файлов mylog_n.txt в директории temp_file. Фикстура.
    :param temp_file: Временный файл для проведения тестов.
    :return:
    """
    temp_dir = os.path.dirname(temp_file)
    # MAX_ATTEMPTS = 1000

    def write_log_to_temp_file(log_message: str, filename: str) -> None:
        try:
            with open(filename, "a", encoding="utf-8") as file:
                file.write(log_message + "\n")
        except (PermissionError, OSError) as error:
            # Выводим сообщение об ошибке
            print(f"Ошибка записи в {filename}: {type(error).__name__}")

            # Пробуем создать новый файл mylog_n.txt
            number = 1
            while number <= MAX_ATTEMPTS:
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
            if number > MAX_ATTEMPTS:
                raise RuntimeError(f"Ошибка записи в mylog_n.txt после {MAX_ATTEMPTS} попыток.")
    with patch("src.decorators.write_log_to_file", write_log_to_temp_file):
        yield


@pytest.fixture
def decorated_function() -> Callable[[Optional[str], str], Callable[..., Union[str, None]]]:
    """
    Проверка на различные ошибки в тестах. Фикстура.
    :return:
    """
    def create_function(filename: Optional[str], function_type: str) -> Callable[..., Union[str, None]]:
        if function_type == "success":
            @log(filename=filename)
            def test_function_log(*args: Any, **kwargs: Any) -> str:
                return "success"
            return test_function_log
        elif function_type == "value_error":
            @log(filename=filename)
            def test_function_log(*args: Any, **kwargs: Any) -> Any:
                raise ValueError("Тестирование ошибки значения.")
            return test_function_log
        elif function_type == "zero_division_error":
            @log(filename=filename)
            def test_function_log(*args: Any, **kwargs: Any) -> Any:
                raise ZeroDivisionError("Тестирование ошибки деления на 0.")
            return test_function_log
        elif function_type == "type_error":
            @log(filename=filename)
            def test_function_log(*args: Any, **kwargs: Any) -> Any:
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
    Проверка тестирования функции для разных комбинаций. Тестирование.
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


def test_function_metadata() -> None:
    """Проверяет сохранение метаданных функции."""
    @log()
    def add(a: int, b: int) -> int:
        return a + b

    assert add.__name__ == "add"


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


@pytest.mark.parametrize("error_type", [PermissionError, OSError])
def test_file_write_error(
        temp_file: str,
        capsys: CaptureFixture[str],
        mock_file_error: Callable,
        log_decorators_write_to_temp_file: None,
        error_type: type
) -> None:
    """
    Проверка тестов ошибки записи в файл. Тестирование.
    :param temp_file:
    :param capsys:
    :param mock_file_error:
    :param log_decorators_write_to_temp_file:
    :param error_type:
    :return:
    """
    @log(filename=temp_file)
    def add(*args: Any, **kwargs: Any) -> int:
        return sum(args)

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


def test_file_write_existing_file(
    temp_file: str,
    capsys: CaptureFixture[str],
    mock_file_error: Callable,
    log_decorators_write_to_temp_file: None,
) -> None:
    """
    Проверяет запись в mylog_2.txt, если mylog_1.txt уже существует.
    :param temp_file:
    :param capsys:
    :param mock_file_error:
    :param log_decorators_write_to_temp_file:
    :return:
    """
    temp_dir = os.path.dirname(temp_file)
    existing_file = os.path.join(temp_dir, "mylog_1.txt")
    with open(existing_file, 'w', encoding='utf-8') as file:
        file.write("Запись существует.\n")

    @log(filename=temp_file)
    def add(*args: Any, **kwargs: Any) -> int:
        return sum(args)

    with mock_file_error(PermissionError, all_files=False):
        result = add(11, -2)
        assert result == 9
        captured = capsys.readouterr()
        assert f"Ошибка записи в {temp_file}: PermissionError" in captured.out

    new_file = os.path.join(temp_dir, "mylog_2.txt")
    assert os.path.exists(new_file)
    with open(new_file, 'r', encoding='utf-8') as f:
        log_content = f.read().strip()
    assert log_content.endswith("→ add. OK.")
    created_files = [file for file in os.listdir(temp_dir) if
                     file.startswith("mylog_") and file.endswith(".txt")]
    assert sorted(created_files) == ["mylog_1.txt", "mylog_2.txt"]


def test_file_write_high_number(
    temp_file: str,
    capsys: CaptureFixture[str],
    mock_file_error: Callable,
    log_decorators_write_to_temp_file: None,
) -> None:
    """
    Проверяет запись в mylog_1000.txt, если mylog_1.txt до mylog_999.txt существуют.
    :param temp_file:
    :param capsys:
    :param mock_file_error:
    :param log_decorators_write_to_temp_file:
    :return:
    """
    temp_dir = os.path.dirname(temp_file)
    # Создаём файлы mylog_1.txt до mylog_999.txt
    for number in range(1, 1000):
        existing_file = os.path.join(temp_dir, f"mylog_{number}.txt")
        with open(existing_file, 'w', encoding='utf-8') as file:
            file.write("Запись существует.\n")

    @log(filename=temp_file)
    def add(*args: Any, **kwargs: Any) -> int:
        return sum(args)

    with mock_file_error(PermissionError, all_files=False):
        result = add(-1, 21)
        assert result == 20
        captured = capsys.readouterr()
        assert f"Ошибка записи в {temp_file}: PermissionError" in captured.out

    new_file = os.path.join(temp_dir, "mylog_1000.txt")
    assert os.path.exists(new_file)
    with open(new_file, 'r', encoding='utf-8') as file:
        log_content = file.read().strip()
    assert log_content.endswith("→ add. OK.")
    created_files = [file for file in os.listdir(temp_dir) if
                     file.startswith("mylog_") and file.endswith(".txt")]
    assert "mylog_1000.txt" in created_files


@pytest.mark.parametrize("error_type", [PermissionError, OSError])
def test_file_write_max_attempts_error(
    temp_file: str,
    capsys: CaptureFixture[str],
    mock_file_error: Callable,
    log_decorators_write_to_temp_file: None,
    error_type: type
) -> None:
    """
    Проверяет выброс исключения, когда превышен лимит попыток записи (1000 файлов).
    :param temp_file:
    :param capsys:
    :param mock_file_error:
    :param log_decorators_write_to_temp_file:
    :param error_type:
    :return:
    """
    @log(filename=temp_file)
    def add(*args: Any, **kwargs: Any) -> int:
        return sum(args)

    with mock_file_error(error_type, all_files=True):
        with pytest.raises(RuntimeError) as exc_info:
            add(1, 2)
        assert str(exc_info.value) == f"Ошибка записи в mylog_n.txt после {MAX_ATTEMPTS} попыток."
        captured = capsys.readouterr()
        assert f"Ошибка записи в {temp_file}: {error_type.__name__}" in captured.out

    temp_dir = os.path.dirname(temp_file)
    created_files = [file for file in os.listdir(temp_dir) if
                     file.startswith("mylog_") and file.endswith(".txt")]
    assert created_files == []
