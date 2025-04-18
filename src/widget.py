from masks import get_mask_card_number, get_mask_account
import datetime

def mask_account_card(string: str) -> str:
    """Платеж. система карты либо 'Счет', скрытие символов номера. Функция"""
    #Если ввод только номера
    if string.isdigit():
        return get_mask_card_number(string)
    #Если в строке содержится "Счет", формирование строки по формату
    elif "Счет" in string:
        account_number = string[-20:]
        return string[:5] + get_mask_account(account_number)
    #Если в строке содержится Платеж. система, формирование строки по формату
    else:
        card_number = " ".join(string[-16:].split())
        return string[:-16] + get_mask_card_number(card_number)


# print(mask_account_card(input("Ввод номера: ")))


def get_date(unformatted_date: str) -> str:
    """Форматирование даты. Функция"""
    #Обрезка строки до "даты" по формату
    date_object = datetime.datetime.strptime(unformatted_date[:10], "%Y-%m-%d").date()
    #Приведение даты к формату
    formatted_date = date_object.strftime("%d.%m.%Y")
    return formatted_date


# print(get_date("2024-03-11T02:26:18.671407"))