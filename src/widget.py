import datetime
import re

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(string_to_mask: str) -> str:
    """Платеж. система карты либо 'Счет', скрытие символов номера. Функция"""
    ### Честно спизженый код у другого студента.
    if not isinstance(string_to_mask, str):
        string_to_mask = str(string_to_mask)

    if card := re.search(r"(\s\d{16}$)", string_to_mask):
        return (f"{string_to_mask[:card.start()]} "
                f"{get_mask_card_number(card.group()[1:])}"
                )
    elif account := re.search(r"(\s\d{20}$)", string_to_mask):
        return (f"{string_to_mask[:account.start()]} "
                f"{get_mask_account(account.group()[1:])}"
                )
    else:
        return "Номер некорректный"


    # # Если ввод только номера
    # if string_to_mask.isdigit():
    #     return get_mask_card_number(string_to_mask)
    # # Если в строке содержится "Счет", формирование строки по формату
    # elif "Счет" in string_to_mask:
    #     account_number = string_to_mask[-20:]
    #     return string_to_mask[:5] + get_mask_account(account_number)
    # # Если в строке содержится Платеж. система, формирование строки по формату
    # else:
    #     card_number = " ".join(string_to_mask[-16:].split())
    #     return string_to_mask[:-16] + get_mask_card_number(card_number)


if __name__ == "__main__":
    print(mask_account_card(input("Ввод номера: ")))


def get_date(unformatted_date: str) -> str:
    """Форматирование даты. Функция"""
    # Обрезка строки до "даты" по формату
    date_object = datetime.datetime.strptime(unformatted_date[:10], "%Y-%m-%d").date()
    # Приведение даты к формату
    formatted_date = date_object.strftime("%d.%m.%Y")
    return formatted_date


# if __name__ == "__main__":
#     print(get_date("2024-03-11T02:26:18.671407"))
