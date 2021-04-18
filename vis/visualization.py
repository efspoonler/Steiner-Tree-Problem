import pandas as pd
import plotly_express as px
import os
import plotly.graph_objects as go
import plotly.figure_factory as ff

DATASET_EVERYTHING = 'eval_everything.csv'
DATASET_HEURISTICS = 'eval_heuristics.csv'
DATASET_HEURISTICS_NO_HOLES ='eval_heuristics_no_holes.csv' 

def everything():
    file_everything= os.getcwd() + '/evaluation/collected_data/' + DATASET_EVERYTHING

    df_everything = pd.read_csv(file_everything, sep=';', header='infer')
    
    df_everything.sort_values(by=['dataset_name', 'numb_terminals', 'algorithm'], inplace=True)
    df_everything['error'] = (1 - df_everything['optimal_solution']/df_everything['alg_solution']) * 100
    
    table_df = df_everything[['dataset_name','numb_nodes', 'numb_edges', 'numb_terminals']]
    table_df = table_df.drop_duplicates('dataset_name')
    list_of_rows = []

    for row in table_df.iterrows():
        row = row[1]
        current_row = [row['dataset_name'],row['numb_nodes'], row['numb_edges'], row['numb_terminals']] 
        list_of_rows.append(current_row)
    table_data = [[x for x in table_df.columns.to_list()]] # add column names.
    [table_data.append(row) for row in list_of_rows] # add column data
    

    ff_fig = ff.create_table(table_data)

    x = sorted(df_everything['dataset_name'].unique())
    fig =go.Figure(data=[
        go.Bar(name='heuristic',  x=x, y=df_everything.loc[df_everything['algorithm'] == 'heuristic']['time'], opacity=0.85, text=df_everything.loc[df_everything['algorithm'] == 'heuristic']['error']),
        go.Bar(name='approximation',  x=x, y=df_everything.loc[df_everything['algorithm'] == 'approximation']['time'], opacity=0.85, text=df_everything.loc[df_everything['algorithm'] == 'approximation']['error']),
        go.Bar(name='networkx_approximation',  x=x, y=df_everything.loc[df_everything['algorithm'] == 'networkx_approximation']['time'], opacity=0.85, text=df_everything.loc[df_everything['algorithm'] == 'networkx_approximation']['error']),
        go.Bar(name='exact_parallel',  x=x, y=df_everything.loc[df_everything['algorithm'] == 'exact_parallel']['time'], opacity=0.85, text=df_everything.loc[df_everything['algorithm'] == 'exact_parallel']['error']),
        go.Bar(name='exact',  x=x, y=df_everything.loc[df_everything['algorithm'] == 'exact']['time'], opacity=0.85, text=df_everything.loc[df_everything['algorithm'] == 'exact']['error'])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_yaxes(type='log', title_text='time in ms')
    fig.update_xaxes(title_text='data-set name')
    fig.update_traces(texttemplate='%{text:.3s}%', textposition='inside')

    fig.show()
    ff_fig.show()


def heuristic():
    file_heuristics = os.getcwd() + '/evaluation/collected_data/' + DATASET_HEURISTICS_NO_HOLES

    df_heuristics = pd.read_csv(file_heuristics, sep=';', header='infer')
    
    df_heuristics.sort_values(by=['dataset_name', 'algorithm'], inplace=True)
    df_heuristics['error'] = (1 - df_heuristics['optimal_solution']/df_heuristics['alg_solution']) * 100
  
    table_df = df_heuristics[['dataset_name', 'numb_edges', 'numb_terminals']]
    table_df = table_df.drop_duplicates('dataset_name')
    list_of_rows = []
    for row in table_df.iterrows():
        row = row[1]
        current_row = [row['dataset_name'], row['numb_edges'], row['numb_terminals']] 
        list_of_rows.append(current_row)
    table_data = [[x for x in table_df.columns.to_list()]] # add column names.
    [table_data.append(row) for row in list_of_rows] # add column data
    

    ff_fig = ff.create_table(table_data)

    x = sorted(df_heuristics['dataset_name'].unique())
    fig =go.Figure(data=[
        go.Bar(name='heuristic',  x=x, y=df_heuristics.loc[df_heuristics['algorithm'] == 'heuristic']['time'], opacity=0.85, text=df_heuristics.loc[df_heuristics['algorithm'] == 'heuristic']['error']),
        go.Bar(name='approximation',  x=x, y=df_heuristics.loc[df_heuristics['algorithm'] == 'approximation']['time'], opacity=0.85, text=df_heuristics.loc[df_heuristics['algorithm'] == 'approximation']['error']),
        go.Bar(name='networkx_approximation',  x=x, y=df_heuristics.loc[df_heuristics['algorithm'] == 'networkx_approximation']['time'], opacity=0.85, text=df_heuristics.loc[df_heuristics['algorithm'] == 'networkx_approximation']['error'])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_yaxes(type='log', title_text='time in ms')
    fig.update_xaxes(title_text='data-set name')
    fig.update_traces(texttemplate='%{text:.3s}%', textposition='inside')

    fig.show()
    ff_fig.show()    


def comp_exact_parallel():
    file_everything= os.getcwd() + '/evaluation/collected_data/' + DATASET_EVERYTHING

    df_everything = pd.read_csv(file_everything, sep=';', header='infer')
    
    df_everything.sort_values(by=['dataset_name', 'numb_terminals', 'algorithm'], inplace=True)
    
    exact_parallel = ['exact', 'exact_parallel']
    data_sets = ['lin02.stp', 'lin03.stp']
    df_everything = df_everything.loc[df_everything['algorithm'].isin(exact_parallel)] #filter just exact and parallel
    df_everything = df_everything.loc[df_everything['dataset_name'].isin(data_sets)] #filter just exact and parallel
    df_everything['error'] = (1 - df_everything['optimal_solution']/df_everything['alg_solution']) * 100
    
    table_df = df_everything[['dataset_name','numb_nodes', 'numb_edges', 'numb_terminals']]
    table_df = table_df.drop_duplicates('dataset_name')
    list_of_rows = []

    for row in table_df.iterrows():
        row = row[1]
        current_row = [row['dataset_name'],row['numb_nodes'], row['numb_edges'], row['numb_terminals']] 
        list_of_rows.append(current_row)
    table_data = [[x for x in table_df.columns.to_list()]] # add column names.
    [table_data.append(row) for row in list_of_rows] # add column data
    

    ff_fig = ff.create_table(table_data)

    x = sorted(df_everything['dataset_name'].unique())
    fig =go.Figure(data=[
        go.Bar(name='exact_parallel',  x=x, y=df_everything.loc[df_everything['algorithm'] == 'exact_parallel']['time'], opacity=0.85, text=df_everything.loc[df_everything['algorithm'] == 'exact_parallel']['time']),
        go.Bar(name='exact',  x=x, y=df_everything.loc[df_everything['algorithm'] == 'exact']['time'], opacity=0.85, text=df_everything.loc[df_everything['algorithm'] == 'exact']['time'])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_yaxes(title_text='time in ms')
    fig.update_xaxes(title_text='data-set name')
    fig.update_traces(texttemplate='%{text:.4s}  ms', textposition='outside')

    fig.show()
    ff_fig.show()



everything()
#heuristic()
#comp_exact_parallel()