# necessary
import time
import pandas as pd

# db connection 
import pymysql
import sqlalchemy

class AccessDataBase:
    
    def __init__(self, db_name):
        # user info & db
        self.user_name = "root"
        self.password = "jys1013011!"
        self.db_name = db_name
        self.host_url = "localhost"
        
    def _connect(self):
        ''' db connect '''
            
        port_num = 3306
        conn = pymysql.connect(host=self.host_url, user=self.user_name, passwd=self.password, port=port_num, db=self.db_name, charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        
        return conn, curs

    def get_tbl(self, table_name, columns='all'):
        ''' db에서 원하는 테이블, 컬럼 pd.DataFrame에 할당 '''
        
        if table_name in self.get_tbl_list():
            st = time.time()
            conn, curs = self._connect()
            
            if columns == 'all':
                query = f'SELECT * FROM {table_name};'
            else:
                # SELECT columns
                query = 'SELECT '
                i = 0
                for col in columns:
                    if i == 0:
                        query += f"`{col}`"
                    else:
                        query += ', ' + f"`{col}`"
                    i += 1

                # FROM table_name
                query += f' FROM {table_name};'
            curs.execute(query)
            tbl = curs.fetchall()
            df = pd.DataFrame(tbl)
            curs.close()
            conn.close()
            
            ed = time.time()
            print(f'\n\n`{table_name}` Import Time: {round(ed-st, 1)}sec')
        else:
            df = None
            print(f'\n\n{table_name} does not exist in db')
        
        return df
    
    def get_tbl_list(self):
        ''' db에 존재하는 모든 테이블 이름 가져오기 '''

        conn, curs = self._connect()

        # get table name list
        query = "SHOW TABLES;"
        curs.execute(query)
        tables = curs.fetchall()

        table_list = []
        for table in tables:
            tbl = list(table.values())[0]
            table_list.append(tbl)
        curs.close()
        conn.close()
        
        return table_list
    
    def engine_upload(self, upload_df, table_name, if_exists_option="append"):
        ''' Upload Table into DB '''
        
        port_num = 3306
        
        # engine
        engine = sqlalchemy.create_engine(f'mysql+pymysql://{self.user_name}:{self.password}@{self.host_url}:{port_num}/{self.db_name}?charset=utf8mb4')
        
        # Create table or Replace table 
        upload_df.to_sql(table_name, engine, if_exists=if_exists_option, index=False)
        
        engine.dispose()
        print(f'\nTable Upload Success: `{table_name}`')