from typing import List, Tuple
from mysql.connector import connect, Error
from etc.config import DBConfig

class DB():
    def __init__(self) -> None:
        self.host = DBConfig.host
        self.port = DBConfig.port
        self.user = DBConfig.user
        self.password = DBConfig.password
        self.database = DBConfig.database
        self.connection = None

    def connect(self):
        try:
            self.connection = connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(self.connection)
        except Error as e:
            print(e)

    def close(self):
        self.connection.close()


    # Auxiliar methods

    def adjust_clientes_result(self, select_result: list) -> List[dict]:
        result = []
        for id, nome in select_result:
            result.append({'id': id, 'nome': nome})    
        return result

    def adjust_produtos_result(self, select_result: list) -> List[dict]:
        result = []
        for id, descricao in select_result:
            result.append({'id': id, 'descricao': descricao})
        return result

    def adjust_vendas_result(self, select_result: list) -> List[dict]:
        result = []
        for id, cliente_id, produtos_id in select_result:
            produtos_id = [int(x) for x in str(produtos_id).split(',')]
            result.append({'id': id, 'cliente_id': cliente_id, 'produtos_id': produtos_id})
        return result


    # Standard Query Execute method

    def execute_query(self, query: str) -> bool:
        result = False

        try:
            self.connect()
            
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
                if cursor.rowcount > 0:
                    result = True
        except Error as e:
            print(e)
        finally:    
            self.close()

        return result


    # SELECT methods

    def execute_select(self, table: str, params: dict = None, opt_args: str = ""):
        query = f"""SELECT * FROM {table} """
        
        if params:
            query += """ WHERE """

            for idx, (k, v) in enumerate(params.items()):
                if type(v) == str:
                    query += f""" {k} = '{v}' """
                else:
                    query += f""" {k} = {v} """
                if idx < len(params)-1:
                    query += f""" AND """

        if opt_args:
            query += f""" {opt_args} """

        result = []

        try:
            self.connect()
            
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                for line in cursor.fetchall():
                    result.append(line)
        except Error as e:
            print(e)
        finally:
            self.close()
            
        return result

    def select_clientes(self, params: dict = None) -> List[dict]:
        select_result = self.execute_select(table='clientes', params=params)
        return self.adjust_clientes_result(select_result) 
        
    def select_produtos(self, params: dict = None) -> List[dict]:
        select_result = self.execute_select(table='produtos', params=params)
        return self.adjust_produtos_result(select_result)
    
    def select_vendas(self, params: dict = None) -> List[dict]:
        select_result = self.execute_select(table='vendas', params=params)
        return self.adjust_vendas_result(select_result)

    def execute_select_last_inserted(self, table: str) -> List[dict]:
        return self.execute_select(table=table, opt_args="ORDER BY id DESC LIMIT 1")

    def select_last_inserted_clientes(self) -> List[dict]:
        select_result = self.execute_select_last_inserted(table='clientes')
        return self.adjust_clientes_result(select_result) 
    
    def select_last_inserted_produtos(self) -> List[dict]:
        select_result = self.execute_select_last_inserted(table='produtos')
        return self.adjust_produtos_result(select_result)

    def select_last_inserted_vendas(self) -> List[dict]:
        select_result = self.execute_select_last_inserted(table='vendas')
        return self.adjust_vendas_result(select_result)


    # INSERT methods

    def execute_insert(self, table: str, params: dict) -> List[dict]:
        query = f""" INSERT INTO {table} """
        
        columns = ''
        values = ''
        for k, v in params.items():
            if columns != '':
                columns += ', '
            columns += k

            if values != '':
                values += ', '
            if type(v) == str:
                values += (f"'{v}'")
            else:
                values += v

        query += f""" ({columns}) values ({values}) """

        print(query)
        last_insert = []

        if self.execute_query(query=query):
            last_insert = self.execute_select_last_inserted(table=table)
        
        return last_insert
        
    def insert_cliente(self, params: dict) -> List[dict]:
        insert_result = self.execute_insert(table='clientes', params=params)
        if insert_result:
            return self.adjust_clientes_result(insert_result)

    def insert_produto(self, params: dict) -> List[dict]:
        insert_result = self.execute_insert(table='produtos', params=params)
        if insert_result:
            return self.adjust_produtos_result(insert_result)

    def insert_venda(self, params: dict):
        insert_result = self.execute_insert(table='vendas', params=params)
        if insert_result:
            return self.adjust_vendas_result(insert_result)


    # UPDATE methods    

    def execute_update(self, table: str, id: int, params: dict):
        query = f"""UPDATE {table} SET """    

        for idx, (k, v) in enumerate(params.items()):
            if type(v) == str:
                query += f""" {k} = '{v}' """
            else:
                query += f""" {k} = {v} """

            if idx < len(params)-1:
                query += f""" AND """
        
        query += f""" WHERE id = {id}"""
        print(query)
        if self.execute_query(query=query):
            return {'status': f'Tabela {table} atualizada com sucesso'}
        else:
            return {'error': f'Falha ao atualizar a tabela {table}'}

    
    # DELETE methods

    def execute_delete(self, table: str, params: dict) -> dict:
        query = f""" DELETE FROM {table} """

        if params:
            query += f""" WHERE """
            
            for idx, (k, v) in enumerate(params.items()):
                if type(v) == str:
                    query += f""" {k} = '{v}' """
                else:
                    query += f""" {k} = {v} """
                if idx < len(params)-1:
                    query += f""" AND """
        print(query)
        return self.execute_query(query=query)

    def delete_cliente(self, params: dict) -> bool:
        if self.execute_delete(table='clientes', params=params):
            return {'status': 'Cliente deletado com sucesso'}
        else:
            return {'error': 'Falha ao deletar o cliente'}

    def delete_produto(self, params: dict) -> bool:
        if self.execute_delete(table='produtos', params=params):
            return {'status': 'Produto deletado com sucesso'}
        else:
            return {'error': 'Falha ao deletar o produto'}

    def delete_venda(self, params: dict) -> bool:
        if self.execute_delete(table='produtos', params=params):
            return {'status': 'Venda deletada com sucesso'}
        else:
            return {'error': 'Falha ao deletar a venda'}