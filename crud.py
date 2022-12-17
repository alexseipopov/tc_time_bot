from mysql.connector import connect
from config import *

def get_columns(table):
    req = f"SHOW COLUMNS FROM {table}"
    # conn = mysql.connect()
    # cursor = conn.cursor()
    # cursor.execute(req)
    # conn.commit()
    # user = cursor.fetchall()
    # return [i[0] for i in user]


def insert(table:str, params: dict):

    # Convert data into request
    
    req = f'INSERT INTO {table} ('
    for i in params:
        req += i + ', '
    else:
        req = req[:-2]+') VALUES ('
    
    for i in params:
        if type(params[i]) is not int:
            req += f'\"{str(params[i])}\", '
        else:
            req += f'{str(params[i])}, '
    else:
        req = req[:-2] +')'
    
    execute_write(req)
    

def update(table, params:dict, where:dict=None):

    req = f'UPDATE {table} SET '
    for i in params:
        if type(params[i]) is not int:
            if params[i] == "NULL":
                req += f'{i}=NULL,'
                print("k")
            else:
                req += f'{i}=\"{params[i]}\",'
        else:
            req += f'{i}={params[i]},'
    else:
        req = req[:-1]
    
    if where is not None:
        req += ' WHERE '
        for i in where:
            if type(where[i]) is not int:
                req += f'{i}=\"{where[i]}\" AND '
            else:
                req += f'{i}={where[i]} AND '
        else:
            req = req[:-4]
    
    execute_write(req)
    

def select(table, columns:list=None, where:dict=None, is_many:bool=False, ordered_by:dict=None):
    
    if columns is not None:
        req = "SELECT "
        for i in columns:
            req += i + ','
        else:
            req = req[:-1] + f' FROM {table}'
    else:
        req=f"SELECT * FROM {table}"
    

    if where is not None:
        req += ' WHERE '
        for i in where:
            if type(where[i]) is dict:
                for k in where[i]:
                    req += f'{i}{where[i][k]}{k} AND '
            elif type(where[i]) is not int:
                req += f'{i}=\"{where[i]}\" AND '
            else:
                req += f'{i}={where[i]} AND '
        else:
            req = req[:-4]
    
    if ordered_by is not None:
        req += ' ORDER BY '
        for i in ordered_by:
            req += f' {i} {ordered_by[i]},'
        else:
            req = req[:-1]
    
    return execute_read(req, is_many)


def delete(table:str, params:dict):
    req = f'DELETE FROM {table} WHERE '
    for i in params:
        req += f'{i}={params[i]},'
    else:
        req = req[:-1]
    execute_write(req)
    

def execute_write(cmd: str):
    # try:
    with connect(
        host="localhost",
        user=DB_USER,
        password=DB_PASSWORD,
        database="s21_peer"
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(cmd)
            connection.commit()
    # except:
    #     print("something wrong")


def execute_read(cmd: str, is_many: bool = False):
    with connect(
        host="localhost",
        user=DB_USER,
        password=DB_PASSWORD,
        database="s21_peer"
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(cmd)
            if is_many:
                data = cursor.fetchall()
            else:
                data = cursor.fetchone()
            return data