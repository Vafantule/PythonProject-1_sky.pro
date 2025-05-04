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


## Документация:

Для получения дополнительной информации обратитесь к [документации](README.md).

## Лицензия:

Этот проект не лицензирован.
