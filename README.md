``` shell
python
```

# Sky.pro_practice

Учебное задание по курсу Python школы Sky.pro

## Установка

### Для начала используйте клонирование репозитория на свое рабочее место:
```
git clone git@github.com:Vafantule/PythonProject-1_sky.pro.git
```

### Установить необходимые зависимости для корректной работы:
```
pip install -r requirements.txt
```




## Модуль processing

Модуль предоставляет функции для работы с банковскими операциями:

- `filter_by_state`: фильтрует операции по заданному состоянию.
- `sort_by_date`: сортирует операции по дате.

### Примеры использования:

```python
from src.processing import filter_by_state, sort_by_date

transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 59402872, 'state': 'CANCELLED', 'date': '2018-09-17T21:27:25.241241'}
]

# Фильтрация операций с состоянием "EXECUTED"
executed_transactions = filter_by_state(transactions)

# Сортировка операций по дате в порядке убывания
sorted_transactions = sort_by_date(transactions)
```
## Модуль generators

Модуль предоставляет функции для работы с банковскими операциями:

- `filter_by_currency`: выдает транзакции по заданной валюте.
- `transaction_descriptions`: выводит описание каждой операции по очереди.
- `card_number_generator`: генерирует диапазон банковских карт.

### Примеры использования:

```aiignore


Функция `transaction_descriptions` находится в файле generators.py. Пример использования:

from transaction_descriptions import transaction_descriptions

transactions = [
    {"description": "Перевод организации"},
    {"description": ""},
    {},
    {"description": 123},
    "not a dict"
]

for desc in transaction_descriptions(transactions):
    print(desc)

Вывод:

Перевод организации
Нет необходимого словаря.
Нет необходимого словаря.
Нет необходимого словаря.
```

## Модуль fin_read

### 
Предназначен для чтения и обработки данных 
финансовых операциях из файлов формата CSV и Excel (XLSX). 
Функции возвращают список словарей, словарь - отдельная транзакция
с ключами по названиям столбцов.

## Основные функции

### `read_financial_operations_from_csv_files(file_path: str) -> List[Dict[str, Any]]`

- Читает финансовые операции из CVS-файла.
- `file_path` - путь к CVS-файлу
- Возвращает:
  - Список словарей, каждый соответствует одной строке (операции) из файла.
  
### `read_financial_operations_from_xlsx_files(file_path: str) -> List[Dict[str, Any]]`

- Читает финансовые операции из Excel-файла (xlsx).
- `file_path` - путь к XLSX-файлу
- Возвращает:
  - Список словарей, каждый соответствует одной строке (операции) из файла.
  
## Требования

- Python 3.7+
- Зависимости:
  - `pandas`
  - `openpyxl` (для поддержки чтения .xlsx-файлов)

Установить зависимости можно командой:
```bash
pip install pandas openpyxl
```

## Примеры использования:

```python

# Чтение из CSV-файла
from fin_read import read_financial_operations_from_csv_files, read_financial_operations_from_xlsx_files
cvs_transactions = read_financial_operations_from_csv_files("transactions.csv")
for row in cvs_transactions:
    print(row)

# Чтение из Excel
xlsx_transactions = read_financial_operations_from_xlsx_files("transactions_excel.xlsx")
for row in xlsx_transactions:
    print(row)
```


## Описание функции `main()`

### Назначение

Функция `main()` реализует консольный интерфейс для интерактивной работы с банковскими транзакциями пользователя. 
Она позволяет загружать данные о транзакциях из различных форматов файлов, выполнять фильтрацию, 
сортировку и вывод информации в удобочитаемом виде.

### Возможности

- Загрузка транзакций из файлов форматов JSON, CSV и XLSX (Excel).
- Фильтрация транзакций по статусу (`executed`, `canceled`, `pending`).
- Возможность сортировки транзакций по дате (по возрастанию или убыванию).
- Фильтрация только рублёвых операций.
- Фильтрация по наличию слова/подстроки в любом поле или выбранном поле транзакции.
- Маскирование номеров счетов и карт при выводе.
- Вывод информации о транзакциях в удобном для пользователя формате.

### Как работает

1. При запуске программа приветствует пользователя и предлагает выбрать формат файла для загрузки данных о транзакциях.
2. Пользователь выбирает статус для фильтрации транзакций.
3. Предлагается отсортировать транзакции по дате.
4. Можно ограничить вывод только рублёвыми операциями.
5. Можно отфильтровать транзакции по наличию слова в любом поле или конкретном поле.
6. Итоговый список транзакций выводится на экран с форматированием, маскировкой номеров счетов/карт, отображением суммы и валюты.

### Пример запуска

```bash
python main.py
```

### Пример диалога

```
Привет! Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла

Ваш выбор 1/2/3: 1
...
```

### Используемые функции

- `load_transactions`
- `read_financial_operations_from_csv_files`
- `read_financial_operations_from_xlsx_files`
- `lower_keys`
- `filter_by_state`
- `sort_by_date`
- `filter_by_currency`
- `mask_account_card`
- `print_transaction`



### Запуск тестов для проверки стабильности кода:
```
Тестирование

Тесты находятся в файле test_generators.py и используют pytest.

Для запуска тестов:

Убедитесь, что оба файла (generators.py и test_generators.py) находятся в одной директории.

Выполните команду:

pytest test_transaction_descriptions.py -v
```

## Документация:

Для получения дополнительной информации обратитесь к [документации](README.md).

## Лицензия:

Этот проект не лицензирован.
