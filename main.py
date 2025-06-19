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
    for delimeter in delimeters:
        if delimeter in condition:
            field, operator, value = condition.partition(delimeter)
            return field.strip(), operator, value.strip()


def filter(data, condition):
    cond_field, operator, cond_value = condition_parser(condition)
    filtered_data = []

    for row in data:
        field_value = row[cond_field]
        if operator == "=" and float(field_value) == float(cond_value):
            filtered_data.append(row)
        elif operator == ">" and float(field_value) > float(cond_value):
            filtered_data.append(row)
        elif operator == "<" and float(field_value) < float(cond_value):
            filtered_data.append(row)

    return filtered_data


# агрегация


def aggregate(data, condition):
    field, operator = condition.split("=")
    agg_data = [float(row[field]) for row in data]

    if operator == "min":
        result = min(agg_data)
    elif operator == "max":
        result = max(agg_data)
    elif operator == "avg":
        result = sum(agg_data) / len(agg_data)

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
        data = filter(data, args.where)

    if args.aggregate:
        data = aggregate(data, args.aggregate)

    print_table(data)


if __name__ == "__main__":
    main()
