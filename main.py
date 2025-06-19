import argparse, csv
from tabulate import tabulate


# чтение файла


def read_csv(file_path):
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader]
    return rows


# аргументы скрипта


def parse_arguments():
    parser = argparse.ArgumentParser(description="Обработка CSV файлов")
    parser.add_argument("file", help="Путь к файлу")
    parser.add_argument("--where", help="Условие фильтрации")
    parser.add_argument("--aggregate", help="Агрегация(только для числовой колонки)")
    return parser.parse_args()


# обработка фильтрации


def condition_parser(condition):
    delimeters = (">", "<", "=")

    # if not any(x in condition for x in delimeters):
    #     raise ValueError(
    #         "Некорректное условие сравнения (не найден оператор сравнения)"
    #     )
    # if condition.count('>') > 1 or condition.count()

    # доделать логику проверок. выбрасываем ошибки при >> >= ><>< итд,
    # также сделать проверку при текстовом формате значения - допустим только оператор =

    for delimeter in delimeters:
        if delimeter in condition:
            field, operator, value = condition.partition(delimeter)
            return field.strip(), operator, value.strip()


def filter_csv(data, condition):
    cond_field, operator, cond_value = condition_parser(condition)

    if cond_field not in data[0]:
        raise KeyError(f"Не найдено поле {cond_field}")

    filtered_data = []

    try:
        cond_value = float(cond_value)
        for row in data:
            field_value = row[cond_field]
            if operator == "=" and float(field_value) == cond_value:
                filtered_data.append(row)
            elif operator == ">" and float(field_value) > cond_value:
                filtered_data.append(row)
            elif operator == "<" and float(field_value) < cond_value:
                filtered_data.append(row)
    except ValueError:
        for row in data:
            field_value = row[cond_field]
            if operator == "=" and field_value == cond_value:
                filtered_data.append(row)
    return filtered_data


# агрегация


def aggregate_csv(data, condition):

    if "=" not in condition:
        raise ValueError(f'Условие агрегации должно быть вида "поле=оператор"')

    field, operator = condition.split("=")

    if field not in data[0]:
        raise KeyError(f"Не найдено поле: {field}")

    agg_data = [
        int(row[field]) if "." not in row[field] else float(row[field]) for row in data
    ]

    if operator == "min":
        result = min(agg_data)
    elif operator == "max":
        result = max(agg_data)
    elif operator == "avg":
        result = sum(agg_data) / len(agg_data)
    else:
        raise ValueError(
            f"Неизвестный оператор агрегации: {operator}, доступные операторы: min, max, avg"
        )

    result_row = {field: result}

    return [result_row]


# вывод данных


def print_table(data):
    print(tabulate(data, headers="keys", tablefmt="pretty"))


# main


def main():
    args = parse_arguments()
    data = read_csv(args.file)

    if args.where:
        data = filter_csv(data, args.where)

    if args.aggregate:
        data = aggregate_csv(data, args.aggregate)

    print_table(data)


if __name__ == "__main__":
    main()
