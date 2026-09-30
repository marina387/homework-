import pandas as pd
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "sales.csv"
DATABASE_FILE = BASE_DIR / "sales.db"
TABLE_NAME = "sales"


def extract(file_path: str) -> pd.DataFrame:
    """
    Извлечение данных из CSV-файла.
    """
    print("1. EXTRACT")

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Файл {file_path} не найден"
        )

    df = pd.read_csv(path)

    print(f"Загружено строк: {len(df)}")

    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Очистка и преобразование данных.
    """
    print("\n2. TRANSFORM")

    # Работаем с копией
    df = df.copy()

    # Удаляем полностью пустые строки
    df = df.dropna(how="all")

    # Удаляем строки с отсутствующими важными значениями
    df = df.dropna(
        subset=["product", "price", "quantity"]
    )

    # Убираем лишние пробелы
    df["product"] = df["product"].str.strip()
    df["category"] = df["category"].str.strip()

    # Приводим данные к нужным типам
    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    # Удаляем строки, которые не удалось преобразовать
    df = df.dropna(
        subset=["price", "quantity"]
    )

    # Оставляем только корректные значения
    df = df[
        (df["price"] > 0) &
        (df["quantity"] > 0)
    ]

    # Приводим количество к целому числу
    df["quantity"] = df["quantity"].astype(int)

    # Создаём новый столбец
    df["total"] = (
        df["price"] * df["quantity"]
    )

    # Округляем деньги
    df["total"] = df["total"].round(2)

    # Добавляем дату обработки
    df["processed_at"] = pd.Timestamp.now()

    # Удаляем дубликаты
    df = df.drop_duplicates(
        subset=["product", "price", "quantity"]
    )

    print(f"После обработки строк: {len(df)}")

    return df


def load(
    df: pd.DataFrame,
    database_file: str,
    table_name: str
):
    """
    Загрузка данных в SQLite.
    """
    print("\n3. LOAD")

    with sqlite3.connect(database_file) as connection:

        df.to_sql(
            table_name,
            connection,
            if_exists="replace",
            index=False
        )

    print(
        f"Данные сохранены в базу {database_file}"
    )


def check_database(
    database_file: str,
    table_name: str
):
    """
    Проверка загруженных данных.
    """
    print("\n4. CHECK")

    with sqlite3.connect(database_file) as connection:

        query = f"""
        SELECT
            product,
            category,
            price,
            quantity,
            total
        FROM {table_name}
        ORDER BY total DESC
        """

        result = pd.read_sql_query(
            query,
            connection
        )

    return result


def run_etl():
    """
    Запуск полного ETL-процесса.
    """

    try:

        data = extract(INPUT_FILE)

        transformed_data = transform(data)

        load(
            transformed_data,
            DATABASE_FILE,
            TABLE_NAME
        )

        result = check_database(
            DATABASE_FILE,
            TABLE_NAME
        )

        print("\nРезультат из базы данных:")
        print(result)

        print("\nETL успешно завершён")

    except Exception as error:

        print("\nОшибка:")
        print(error)


run_etl()