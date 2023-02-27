import pymysql
import sqlalchemy as alch
from sqlalchemy import create_engine
from getpass import getpass
import pandas as pd
import numpy as np
   

def sql_connection():
    password = getpass("MySQL password: ")
    dbName = "journals"
    connectionData=f"mysql+pymysql://root:{password}@localhost/{dbName}"
    engine = alch.create_engine(connectionData)
    return engine

def include_into_sql(df_bbc_together,df_aj_all,engine):
    df_bbc_together.to_sql('bbc', con=engine)
    df_aj_all.to_sql('aljazeera', con=engine)
    return

def df_bbc_sql_query(df_bbc_sql,engine):
    df_bbc_sql= pd.read_sql_query("""SELECT * FROM bbc """,con=engine)
    df_bbc_sql['(ukraine:length)*100']=pd.read_sql_query("""SELECT ukraine/length*100 FROM bbc """,con=engine)
    df_bbc_sql['(war:length)*100']=pd.read_sql_query("""SELECT war/length*100 FROM bbc """,con=engine)
    df_bbc_sql['(russia:length)*100']=pd.read_sql_query("""SELECT russia/length*100 FROM bbc """,con=engine)
    df_bbc_sql['(putin:length)*100']=pd.read_sql_query("""SELECT putin/length*100 FROM bbc """,con=engine)
    df_bbc_sql['(zelensky:length)*100']=pd.read_sql_query("""SELECT zelensky/length*100 FROM bbc """,con=engine)
    return df_bbc_sql

def bbc_df_clearance(df_bbc_sql):
    df_bbc_sql=df_bbc_sql.drop(columns={'index'})
    df_bbc_sql['source']=  'BBC'
    df_bbc_sql.drop(columns={'article','length','ukraine','war','russia','putin','zelensky'},inplace=True)
    df_bbc_sql.set_index(['source'],inplace=True)
    df_bbc_sql = df_bbc_sql[["polarity","subjectivity", "(ukraine:length)*100",'(war:length)*100','(russia:length)*100','(putin:length)*100','(zelensky:length)*100','link']]
    return df_bbc_sql

def df_aj_sql_query(df_aj_sql,engine):
    df_aj_sql= pd.read_sql_query("""SELECT * FROM aljazeera """,con=engine)
    df_aj_sql['(ukraine:length)*100']=pd.read_sql_query("""SELECT ukraine/length*100 FROM aljazeera """,con=engine)
    df_aj_sql['(war:length)*100']=pd.read_sql_query("""SELECT war/length*100 FROM aljazeera """,con=engine)
    df_aj_sql['(russia:length)*100']=pd.read_sql_query("""SELECT russia/length*100 FROM aljazeera """,con=engine)
    df_aj_sql['(putin:length)*100']=pd.read_sql_query("""SELECT putin/length*100 FROM aljazeera """,con=engine)
    df_aj_sql['(zelensky:length)*100']=pd.read_sql_query("""SELECT zelensky/length*100 FROM aljazeera """,con=engine)
    return df_aj_sql

def aj_df_clearance(df_aj_sql):
    df_aj_sql=df_aj_sql.drop(columns={'index'})
    df_aj_sql['source']=  'Aljazeera'
    df_aj_sql.drop(columns={'article','length','ukraine','war','russia','putin','zelensky'},inplace=True)
    df_aj_sql.set_index(['source'],inplace=True)
    df_aj_sql = df_aj_sql[["polarity","subjectivity","(ukraine:length)*100",'(war:length)*100','(russia:length)*100','(putin:length)*100','(zelensky:length)*100','link']]
    return df_aj_sql

