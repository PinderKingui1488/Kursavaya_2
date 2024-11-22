import psycopg2
from psycopg2 import sql


def database_create(database, params):
    """Создает базу данных и таблицы."""
    try:
        conn = psycopg2.connect(dbname="postgres", *params)
        conn.set_client_encoding("UTF8")
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(sql.Identifier(database)))
        cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(database)))

        cur.close()
        conn.close()

        with psycopg2.connect(dbname=database, *params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS employers (
                        company_id INTEGER PRIMARY KEY,
                        company_name TEXT NOT NULL
                    );"""

                )

                cur.execute(
                    """CREATE TABLE IF NOT EXISTS vacancies (
                            vacancy_id INTEGER PRIMARY KEY,
                            vacancy_name VARCHAR,
                            salary NUMERIC,
                            company_id INTEGER REFERENCES employers(company_id),
                            url VARCHAR
                        );"""
                )
                conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при создании базы данных:", error)


def db_save(database, vacancy, params):
    """Добавляет вакансию в базу данных."""
    try:
        with psycopg2.connect(dbname=database, *params) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                # Используем параметризованные запросы для предотвращения SQL-инъекций.
                cur.execute(
                    """
                    INSERT INTO employers (company_id, company_name) VALUES (%s, %s)
                    ON CONFLICT (company_id) DO UPDATE SET company_name = EXCLUDED.company_name;
                """,
                    (vacancy.employer_id, vacancy.employer_name),
                )

                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, vacancy_name, salary, company_id, url) VALUES 
                    (%s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO UPDATE SET vacancy_name = EXCLUDED.vacancy_name, salary = 
                    EXCLUDED.salary,
                     company_id = EXCLUDED.company_id, url = EXCLUDED.url;
                    
                """,
                    (
                        vacancy.id,
                        vacancy.name,
                        vacancy.salary,
                        vacancy.employer_id,
                        vacancy.url,
                    ),
                )
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при сохранении данных:", error)

