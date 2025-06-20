import argparse, csv
from tabulate import tabulate


# чтение файла
def read_csv(file_path):
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
        if not data:
            raise SystemExit(f"В файле '{file_path}' отсутствуют данные.")
    return data


# аргументы скрипта
def parse_arguments():
    parser = argparse.ArgumentParser(description="Обработка CSV файлов")
    parser.add_argument("--file", required=True, help="Путь к файлу")
    parser.add_argument("--where", help="Условие фильтрации")
    parser.add_argument("--aggregate", help="Агрегация(только для числовой колонки)")

    args = parser.parse_args()

    # проверка синтаксиса фильтрации --where
    if args.where:
        operators = (">", "<", "=")
        operator_count = sum([args.where.count(op) for op in operators])
        if operator_count != 1:
            raise ValueError(
                f"Некорректный оператор сравнения в аргументе --where. Доступные операторы: {operators}."
            )

    # проверка синтаксиса агрегации --aggregate
    if args.aggregate:
        if args.aggregate.count("=") != 1:
            raise ValueError(f"Условие агрегации должно быть вида 'поле=оператор'.")
    return args


# фильтрация --where
# разбираем условие фильтрации
def condition_parser(condition):
    delimeters = (">", "<", "=")

    for delimeter in delimeters:
        if delimeter in condition:
            # "поле, по которому сравниваем", "оператор(<, > или =)", "значение, с которым сравниваем"
            field, operator, value = condition.partition(delimeter)
            return field.strip(), operator, value.strip()


# фильтрация
def filter_csv(data, condition):
    cond_field, operator, cond_value = condition_parser(condition)

    # если поля нет в таблице
    if cond_field not in data[0]:
        raise ValueError(f"Не найдено поле '{cond_field}'.")

    filtered_data = []

    # в блоке try обрабатываем фильтрацию по числовому значению, в блоке except по текстовому
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
            is_float = False

            # блок try обрабатывает ошибку, когда числовое поле пытаются отфильтровать по текстовому значению
            try:
                field_value = float(field_value)
                is_float = True  # через флаг, чтобы не отдавать ошибку в except

            # поле в таблице и значение для фильтрации - текстовые
            except ValueError:
                if operator == "=" and field_value == cond_value:
                    filtered_data.append(row)
                elif operator != "=":
                    raise ValueError(
                        f"Некорректный оператор сравнения '{operator}'. Для сравнения по текстовому значению доступен только оператор '='."
                    )

            if is_float:
                raise ValueError(
                    f"Для поля '{cond_field}' недоступно сравнение по текстовому значению: '{cond_value}'. Введите число."
                )
    return filtered_data


# агрегация --aggregate
def aggregate_csv(data, condition):

    # разбираем условие агрегации
    field, operator = condition.split("=")
    field, operator = field.strip(), operator.strip()

    # обрабатываем неверный ввод поля
    try:
        if field not in data[0]:
            raise ValueError(f"Не найдено поле: '{field}'.")

    except IndexError:  # если пришел пустой список после фильтрации
        raise SystemExit("Отсутствуют данные для агрегации.")

    try:
        # собираем все поле в список значений
        agg_data = [
            int(row[field]) if "." not in row[field] else float(row[field])
            for row in data
        ]

    except ValueError:  # если выбрано не числовое поле
        raise ValueError("Агрегация доступна только по числовым полям.")

    if operator == "min":
        result = min(agg_data)
    elif operator == "max":
        result = max(agg_data)
    elif operator == "avg":
        result = round(sum(agg_data) / len(agg_data), 1)
    else:
        raise ValueError(
            f"Неизвестный оператор агрегации: '{operator}', доступные операторы: 'min', 'max', 'avg'."
        )

    result_row = {field: result}

    return [result_row]


# вывод данных
def print_table(data):
    print(tabulate(data, headers="keys", tablefmt="pretty"))


# main
def main():
    try:
        args = parse_arguments()
        data = read_csv(args.file)

        if args.where:
            data = filter_csv(data, args.where)

        if args.aggregate:
            data = aggregate_csv(data, args.aggregate)

        print_table(data)

    except ValueError as e:
        print(f"ValueError: {e}")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
