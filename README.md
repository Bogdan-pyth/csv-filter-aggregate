Скрипт для вывода в консоль csv файла с поддержкой фильтрации и агрегации.

Установка:
1. Клонируйте репозиторий: git clone https://github.com/Bogdan-pyth/csv-filter-aggregate.git
2. Установите зависимости: pip install -r requirements.txt

Запуск:
python main.py --file <path_to_csv> --where <"field=value"> --aggregate <"field=operator">
где:

--file - обязательный аргумент, в который нужно передать путь к csv файлу.

--where - необязательный аргумент, используется для фильтрации значений.
        В качестве параметров нужно передать строку "field=value", где:
        field - Название поля.
        = - Оператор сравнения. Поддерживаются >, < и =
        value - Значение для фильтрации.

--aggregate - необязательный аргумент, используется для агрегации значений. Работает только для числовых значений.
        В качестве параметров нужно передать строку "field=operator", где:
        field - Название поля. 
        operator - Операция агрегации. Поддерживаются min, max и avg.


Пример запуска для файла products.csv:

python main.py --file products.csv --where "brand=samsung" --aggregate "rating=avg"

python main.py --file products.csv --where "rating>4.5" --aggregate "price=min"

Также смотри примеры запуска на скриншоте "Пример работы.JPG".


p.s. для запуска тестов:  
pip install pytest  
pip install pytest-cov  
pytest --cov=main test_main.py 