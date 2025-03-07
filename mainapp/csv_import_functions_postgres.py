import os
import numpy as np
import pandas as pd
import psycopg2


def create_df(file_path):
    df = {}
    try:
        df[file_path] = pd.read_csv(file_path)
    except UnicodeDecodeError:
        df[file_path] = pd.read_csv(file_path, encoding="ISO-8859-1") #if utf-8 encoding error
    print(file_path)
    
    return df

def clean_tbl_name(filename):
  
    #rename csv, force lower case, no spaces, no dashes
    clean_tbl_name = filename.lower().replace(" ", "").replace("-","_").replace(r"/","_").replace("\\","_").replace("$","").replace("%","")
    
    tbl_name = '{0}'.format(clean_tbl_name.split('.')[0])

    return tbl_name

def clean_colname(dataframe):
  
    #force column names to be lower case, no spaces, no dashes
    dataframe.columns = [x.lower().replace(" ", "_").replace("-","_").replace(r"/","_").replace("\\","_").replace(".","_").replace("$","").replace("%","") for x in dataframe.columns]

    #processing data
    replacements = {
        'timedelta64[ns]': 'varchar',
        'object': 'varchar',
        'float64': 'float',
        'int64': 'int',
        'datetime64': 'timestamp'
    }

    col_str = ", ".join("{} {}".format(n, d) for (n, d) in zip(dataframe.columns, dataframe.dtypes.replace(replacements)))
    
    return col_str, dataframe.columns



def upload_to_db(host, dbname, user, password, tbl_name, col_str, file, dataframe, dataframe_columns):

    conn_string = "host=%s dbname=%s user=%s password=%s" % (host, dbname, user, password)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('Opened the database Successfully')
    
    #drop table with same name
    cursor.execute("drop table if exists %s;" % (tbl_name))

    #create table
    cursor.execute("create table %s (%s);" % (tbl_name, col_str))
    print('{0} was created successfully'.format(tbl_name)) 
    
    #insert values to table

    #save df to csv
    dataframe.to_csv(file, header=dataframe_columns, index=False, encoding='utf-8')

    #open the csv file, save it as an object
    my_file = open(file)
    print('File opened in memory')
    
    #upload to db
    SQL_STATEMENT = """
    COPY %s FROM STDIN WITH
        CSV
        HEADER
        DELIMITER AS ','
    """

    cursor.copy_expert(sql=SQL_STATEMENT % tbl_name, file=my_file)
    print('File copied to database')
    
    cursor.execute("grant select on table %s to public" % tbl_name)
    conn.commit()
    cursor.close()
    print('Table {0} imported to database completed'.format(tbl_name))

    return

