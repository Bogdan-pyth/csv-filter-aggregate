import pytest, tempfile, os, sys


import main


# Тест на корректные аргументы
def test_valid_arguments():
    sys.argv = [
        "main.py",
        "--file",
        "data.csv",
        "--where",
        "price>100",
        "--aggregate",
        "price=avg",
    ]
    args = main.parse_arguments()

    assert args.file == "data.csv"
    assert args.where == "price>100"
    assert args.aggregate == "price=avg"


# Некорректный --where
def test_invalid_operator_in_where():
    sys.argv = [
        "main.py",
        "--file",
        "data.csv",
        "--where",
        "price>>100",
    ]

    with pytest.raises(ValueError):
        main.parse_arguments()


def test_invalid_operator_in_where_2():
    sys.argv = [
        "main.py",
        "--file",
        "data.csv",
        "--where",
        "price100",
    ]

    with pytest.raises(ValueError):
        main.parse_arguments()


# Некорректный --aggregate
def test_invalid_aggregate_format():
    sys.argv = [
        "main.py",
        "--file",
        "data.csv",
        "--aggregate",
        "priceavg",
    ]

    with pytest.raises(ValueError):
        main.parse_arguments()


# Тестирование чтения CSV файла
@pytest.fixture
def mock_csv():
    # Создаем данные в формате CSV в виде строки
    data = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
"""
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(delete=False, mode="w", newline="") as temp_file:
        temp_file.write(data)
        temp_file_path = temp_file.name  # Путь к временно созданному файлу

    yield temp_file_path  # Передаем путь к файлу в тест

    # Удаляем временный файл после теста
    os.remove(temp_file_path)


def test_read_csv(mock_csv):
    data = main.read_csv(mock_csv)
    assert len(data) == 3
    assert data[0]["name"] == "iphone 15 pro"
    assert data[1]["price"] == "1199"


# фильтрация
def test_condition_parser():
    condition = "price>1000"
    field, operator, value = main.condition_parser(condition)
    assert field == "price"
    assert operator == ">"
    assert value == "1000"


data = [
    {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
    {"name": "galaxy s23 ultra", "brand": "samsung", "price": "1199", "rating": "4.8"},
    {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
]


def test_filter_numeric():
    condition = "price>1000"
    filtered_data = main.filter_csv(data, condition)
    assert len(filtered_data) == 1
    assert filtered_data[0]["name"] == "galaxy s23 ultra"


def test_filter_string():
    condition = "brand=apple"
    filtered_data = main.filter_csv(data, condition)
    assert len(filtered_data) == 1
    assert filtered_data[0]["name"] == "iphone 15 pro"


def test_filter_invalid_condition():
    condition = "price>invalid_type"
    with pytest.raises(ValueError):
        main.filter_csv(data, condition)


def test_filter_invalid_condition_2():
    condition = "invalid_field>198"
    with pytest.raises(ValueError):
        main.filter_csv(data, condition)


# def test_filter_invalid_condition_3():
#     condition = "price>=198"  # invalid operator
#     with pytest.raises(ValueError):
#         main.filter_csv(data, condition)


def test_filter_invalid_condition_4():
    condition = "brand>apple"
    with pytest.raises(ValueError):
        main.filter_csv(data, condition)


# агрегация


def test_aggregate_avg():
    condition = "price=avg"
    result = main.aggregate_csv(data, condition)
    assert result[0]["price"] == 799.0


def test_aggregate_min():
    condition = "price=min"
    result = main.aggregate_csv(data, condition)
    assert result[0]["price"] == 199.0


def test_aggregate_max():
    condition = "price=max"
    result = main.aggregate_csv(data, condition)
    assert result[0]["price"] == 1199.0


def test_aggregate_invalid_condition():
    condition = "price=invalid_operator"
    with pytest.raises(ValueError):
        main.aggregate_csv(data, condition)


# def test_aggregate_invalid_condition_2():
#     condition = "invalid_condition"
#     with pytest.raises(ValueError):
#         main.aggregate_csv(data, condition)


def test_aggregate_invalid_condition_3():
    condition = "invalid_field=min"
    with pytest.raises(ValueError):
        main.aggregate_csv(data, condition)


def test_aggregate_after_filter():
    data = []
    condition = "price=min"
    with pytest.raises(SystemExit):
        main.aggregate_csv(data, condition)


# вывод


def test_print_table(capsys):
    data = [{"price": 999}, {"price": 1199}, {"price": 199}]
    main.print_table(data)
    captured = capsys.readouterr()
    assert "price" in captured.out
    assert "999" in captured.out
    assert "1199" in captured.out
