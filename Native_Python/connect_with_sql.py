from sqlalchemy import create_engine
from pandas import read_csv,read_sql_table,read_sql_query
import os
import traceback
import matplotlib.pyplot as plt

def get_db_conn(db_api=None):
    if db_api is None:
        return None
    elif db_api.upper() == 'MYSQL':
        driver = r'mysql+pymysql'
    elif db_api.upper() == 'POSTGRESQL':
        driver = r'postgresql+pg8000'

    # connection string
    db = create_engine(f"{driver}://root@localhost/demo?host=localhost?port=3306")
    conn = db.connect()
    return conn,db

def dump_data_to_table(table_name,db_conn,df=None,if_exists='replace',file_name=None,file_format=None):
    if file_name is not None and file_format.upper() == 'CSV':
        df = read_csv(file_name)
    
    df.to_sql(name=table_name,con=db_conn,index=False,if_exists=if_exists)
    
def read_table_data(table_name,db_conn,sql_query=None,columns=None):
    if sql_query is None:
        df = read_sql_table(table_name=table_name,con=db_conn,columns=columns)
    else:
        df = read_sql_query(sql=sql_query,con=db_conn)
    return df

#### MAIN ########
try:
    conn,db = get_db_conn(db_api='MYSQL')

    ################ dumping csv as a table ########################
    # base_dir = r'/Users/manojkumarrajendran/how_stuff_works/Input_data'
    # file_name = os.path.join(base_dir,'HRDataset_v14.csv')
    # dump_data_to_table(file_name=file_name,table_name='hr_data',db_conn=conn,file_format='CSV')

    ################ adding a column to an already existing table ####################
    hr_data = read_table_data(table_name='hr_data',db_conn=conn)
    
    # sql_query = f"select * from demo.hr_data where UPPER(Department) = 'SALES'"
    # hr_data = read_table_data(table_name='hr_data',db_conn=conn,sql_query=sql_query)

    # print(hr_data)

    # dept_names = set(hr_data['Department'])
    # print(dept_names)
    # dept_details = dict(zip(
    #     dept_names,
    #     range(1,len(dept_names)+1)
    # ))

    # hr_data['role_id'] = [dept_details.get(record) for record in hr_data['Department']]
    # print(hr_data)

    # dump_data_to_table(table_name='hr_data',db_conn=conn,df=hr_data)

    ################ adding rows to an already existing table ####################
    # first_row = hr_data.iloc[0,:]
    # first_row_as_dict = dict(first_row)
    # first_row_as_dict['EmpID'] = 20000
    # first_row_as_dict['Employee_Name'] = 'Python'

    # print('Before appending :',len(hr_data))
    # hr_data = hr_data.append(first_row_as_dict,ignore_index=True)
    # print('After appending :',len(hr_data))
    # print(hr_data)

    ############ dump data to an already existing table with new rows ###############
    # dump_data_to_table(table_name='hr_data',df=hr_data,db_conn=conn,if_exists='append')

    ############ visualize data ############
    grouped_data = hr_data[['Department','EmpID']].groupby('Department').count()
    # print(grouped_data)
    grouped_data = grouped_data.reset_index()
    # print(grouped_data)
    grouped_data.plot(x='Department',y='EmpID',figsize=(20,5),kind='bar')
    plt.show()

except Exception:
    print('Exception caught is',traceback.print_exc())

finally:
    conn.close()
    db.dispose()
    print('Database disconnected from the program!')