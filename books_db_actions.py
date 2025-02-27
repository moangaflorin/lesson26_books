import os

import psycopg2 as ps
from psycopg2 import OperationalError

from init_config import config



def get_data(sql_query: str, db_config: dict, return_as_dict: bool = True):
    try:
        with ps.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                data = cursor.fetchall()
                if return_as_dict:
                    columns = [desc.name for desc in cursor.description]
                    items_list = []
                    for item in data:
                        items_list.append(dict(zip(columns, item)))
                    return items_list

        return data
    except OperationalError as e:
        print(f"The database config data is wrong {e}")
    except Exception as e:
        print(f"Exception here")

def insert_row(sql_query: str, db_config: dict):
    try:
        with ps.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                conn.commit()
                print("Row was added")



    except Exception as e:
        print(f"Exception was raised {e}")

def delete_row(name: str, db_config: dict, table_name: str = "books"):
    try:
        query = f"delete from public.{table_name} where \"name\" = '{name}'"
        with ps.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
                print(f"Successfully deleted row table: {table_name}, name: {name}")

    except Exception as e:
        print(f"Failed to delete the instance {name}: {e}")


if __name__ == '__main__':
    sql_query = "insert into books(\"name\", number_of_sales, reviews, author_id) values ('Harry Potter 7', 200000, 9, 1);"

    database_config = config.get("database_config")
    database_config['password'] = os.environ['db_password']
    if database_config:

        # insert_row(sql_query, database_config)
        delete_row("Harry Potter 1", database_config)
        query = "select * from public.books"
        response = get_data(query, database_config)
        print(response)
    else:
        print("No database")