import psycopg2
class Data:
    def __init__(self, database, user, password, host = 'localhost', port = '5432'):
        self.connection = psycopg2.connect(database = database, user = user, password = password, host = host, port = port)
        self.cursor = self.connection.cursor()
    def post_data(self, vals: dict, table_name: str):
        vals[1]['status'] = 'создана'
        self.cursor.execute(f'''insert into {table_name} ({','.join(vals[1].keys())}) \
                            values ({','.join([f"'{v}'" if type(v) == str else str(v) for v in vals[1].values()])})''')
        self.connection.commit()
    def get_status(self, table_name: str, user_id: str) -> dict:
        self.cursor.execute(f'''select request_number, status from {table_name} where user_id = '{user_id}' ''')
        vals = self.cursor.fetchall()
        return vals
    def get_last_req_number(self, table_name: str, user_id: str) -> dict:
        query = f'''select count(*) from {table_name} where user_id = '{user_id}' '''
        self.cursor.execute(query)
        val = self.cursor.fetchone()
        return val[0]