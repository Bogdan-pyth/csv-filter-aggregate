import argparse, csv, tabulate


def parse_arguments():
    parser = argparse.ArgumentParser(description="Обработка CSV файлов")
    parser.add_argument("--file", required=True, help="Путь к файлу")
    parser.add_argument("--where", help="Условие фильтрации")
    parser.add_argument("--aggregate", help="Агрегация(только для числовой колонки)")
    return parser.parse_args()


def read_csv(file_path):
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader]
    return rows
