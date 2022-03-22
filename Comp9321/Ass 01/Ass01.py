import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import numpy as np
import math
import re

studentid = os.path.basename(sys.modules[__name__].__file__)


def log(question, output_df, other):
    print("--------------- {}----------------".format(question))

    if other is not None:
        print(question, other)
    if output_df is not None:
        df = output_df.head(5).copy(True)
        for c in df.columns:
            df[c] = df[c].apply(lambda a: a[:20] if isinstance(a, str) else a)

        df.columns = [a[:10] + "..." for a in df.columns]
        print(df.to_string())




def read_csv(csv_file):
    """
    :param csv_file: the path of csv file
    :return: A dataframe out of the csv file
    """
    return pd.read_csv(csv_file)


def question_1(routes, suburbs):
    """
    :param routes: the path for the routes dataset
    :param suburbs: the path for the routes suburbs
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    
    #################################################
    # Your code goes here ...
    #################################################
    csv_file = routes
    df1 = read_csv(csv_file)
    data = df1['service_direction_name'].map(lambda row:row.split(",")).str.get(0)
    data2 = df1['service_direction_name'].map(lambda row:row.split(",")).str.get(-1)
     # Clean some data for later usage
    data2 = data2.str.replace('then',' ')
    data2 = data2.str.replace('all stations to',' ')
    data2 = data2.str.lstrip()

    df1['start'] = data
    df1['end'] = data2
    #log("QUESTION 1", output_df=df1[["service_direction_name", "start", "end"]], other=df1.shape)
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: dataframe df2
            Please read the assignment specs to know how to create the output dataframe
    """

    series1 = df1['start'].value_counts().sort_values(ascending=False)
    series2 = df1['end'].value_counts().sort_values(ascending=False)

    series3 = series1 + series2 
    df = pd.DataFrame(series3).reset_index()
    df.columns = ['service_location', 'Frequency']
    df = df.sort_values(by='Frequency', ascending=False)
    df = df.reset_index(drop=True)
    df2 = df.dropna()
    df2 = df2[:5]
    log("QUESTION 2", output_df=df2, other=df2.shape)
    return df2

def question_3(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    #################################################
   # Lower all the case ! 
    # Stupid solution may need to change
    df1.transport_name = df1.transport_name.str.lower()
    df1['transport_name'][df1.transport_name.str.contains('bus')] = 'Bus'
    df1['transport_name'][df1.transport_name.str.contains('ferr')] = 'Ferry'
    df1['transport_name'][df1.transport_name.str.contains('metro')] = 'Metro'
    df1['transport_name'][df1.transport_name.str.contains('trains network')] = 'Train'
    df1['transport_name'][df1.transport_name.str.contains('light rail')] = 'Light Rail'
    df1['transport_name'][df1.transport_name.str.contains('private coach service')] = 'Bus'
    df1['transport_name'][df1.transport_name.str.contains('regional trains')] = 'Train'
    df1['transport_name'][df1.transport_name.str.contains('central west and orana network')] = 'Train'
    df1['transport_name'][df1.transport_name.str.contains('new england north west network')] = 'Train'
    df1['transport_name'][df1.transport_name.str.contains('south east and tablelands network')] = 'Train'
    df1['transport_name'][df1.transport_name.str.contains('riverina murray network')] = 'Train'
    df1['transport_name'][df1.transport_name.str.contains('north coast network')] = 'Train'
    df3 = df1.copy()
    #################################################

    log("QUESTION 3", output_df=df3[['transport_name']], other=df3.shape)
    return df3


def question_4(df3):
    """
    :param df3: the dataframe created in question 3
    :param continents: the path for the Countries-Continents.csv file
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    #################################################
    series1 = df3['transport_name'].value_counts().sort_values(ascending=True)
    df4 = pd.DataFrame(series1).reset_index()
    df4.columns = ['transport_name', 'frequency']

    log("QUESTION 4", output_df=df4[["transport_name", "frequency"]], other=df4.shape)
    return df4


    log("QUESTION 4", output_df=df4[["transport_name", "frequency"]], other=df4.shape)
    return df4


def question_5(df3, suburbs):
    """
    :param df3: the dataframe created in question 2
    :param suburbs : the path to dataset
    :return: df5
            Data Type: dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    #################################################
    # Your code goes here ...
    #################################################
    df2 = read_csv(suburbs)
    series2 = df2[['suburb', 'population']]
    df_p = pd.DataFrame(series2)
    df3 = df3[df3['depot_name'].notna()]
    df3['depot_name'] = df3['depot_name'].map(lambda row:row.split(",")).str.get(-1)
    series1 = df3['depot_name'].value_counts().sort_values(ascending=False)
    df_d = pd.DataFrame(series1).reset_index()
    df_c = df_d.set_index('index').join(df_p.set_index('suburb'))
    df_c = df_c.loc[df_c['population'] * df_c['depot_name'] != 0] 
    df_c = df_c.dropna()
    df_c['ratio'] = (df_c['depot_name'] / df_c['population']) * 100
    df_c = df_c.sort_values(by='ratio', ascending=False)
    df5 = df_c.head(5)
    df5 = df5.drop(columns = ['depot_name','population'])
    df5 = df5.reset_index()
    df5 = df5.rename({'index': 'depot'}, axis='columns')

    log("QUESTION 5", output_df=df5[["ratio"]], other=df5.shape)
    return df5


def question_6(df3):
    """
    :param df3: the dataframe created in question 3
    :return: pandas pivot table
    """
    table = None
    #################################################
    # Your code goes here ...
    #################################################
    series = df3['operator_name'].value_counts().sort_values(ascending=False)
    df3 = df3[['operator_name','transport_name']]
    df3 = df3.drop_duplicates(subset=None, keep='first', inplace=False)
    df_p = pd.DataFrame(series).reset_index()
    df_p = df_p.rename({'index': 'operator','operator_name':'frequency'}, axis='columns')
    df_c = df_p.set_index('operator').join(df3.set_index('operator_name'))
    df_c = df_c.sort_values(by='frequency', ascending=False)
    # Consinder data like this is mostly show how transfort industry are made of,
    # I choose the top 15 compines and their form for the graph
    df_c = df_c.reset_index()
    df_c = df_c.rename({'index': 'operator_name', 'frequency': 'num_of_service'}, axis='columns')
    df_c = df_c.head(15)
    table = pd.pivot_table (df_c, values='num_of_service', index='operator_name',
                    columns=['transport_name'],sort=True)
    log("QUESTION 6", output_df=None, other=table)
    return table




def question_7(df3,suburbs):
    """
    :param df3: the dataframe created in question 3
    :param suburbs : the path to dataset
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    #################################################

    plt.savefig("{}-Q7.png".format(studentid))


def question_8(df3,suburbs):
    """
    :param df3: the dataframe created in question 3
    :param suburbs : the path to dataset
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    #################################################

    plt.savefig("{}-Q8.png".format(studentid))



if __name__ == "__main__":
    df1 = question_1("routes.csv", "suburbs.csv")
    df2 = question_2(df1.copy(True))
    df3 = question_3(df1.copy(True))
    df4 = question_4(df3.copy(True))
    df5 = question_5(df3.copy(True), "suburbs.csv")
    table = question_6(df3.copy(True))
    # question_7(df3.copy(True), "suburbs.csv")
    # question_8(df3.copy(True), "suburbs.csv")