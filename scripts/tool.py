import pandas as pd

def formulato3(path, value):
    global dic
    formulat = pd.read_csv(path)
    formulat['o3_pred_1hr'] = (value - formulat['Intercept']) / formulat['slope']
    dic = pd.Series(formulat.o3_pred_1hr.values, index=formulat.Location).to_dict()


def selectDatetime(site, start_T, end_T):
    global df
    df = pd.read_csv('/Users/farewell/Documents/EMCT/GIS/geofance_O3_raw/o3_1hr_8hr/' + site + '.csv')
    df = df.drop(['Unnamed: 0'], axis=1)
    df = df[(df['移動平均'] != -1.0)].dropna()
    df = df.reset_index()
    df = df[(df['時間'] >= int(start_T)) & (df['時間'] <= int(end_T))].reset_index()
    df = df.iloc[:, 1:]

def selectO3value(df, value, value_hr, temp_list):
    global final_data, result_list
    
    ix = 0
    count_TT_up, count_FT, count_TF, count_TT_down, count_error  = 0, 0, 0, 0, 0

    result_list = []
    #while ix < len(df):
    for x in range(len(df)):

        #if df.loc[ix, '時間'] >= start_:
        #    t = df.loc[ix: ix + range_, :]
        #    print(t)
        #    for x in range(len(t)):
        if df.iloc[x, 5] >= value and df.iloc[x, 6] >= value_hr:
            temp_list.append('TT_UP')
            count_TT_up = count_TT_up + 1 
        elif df.iloc[x, 5] < value and df.iloc[x, 6] >= value_hr:
            temp_list.append('FT')
            count_FT = count_FT + 1
        elif df.iloc[x, 5] >= value and df.iloc[x, 6] < value_hr:
            temp_list.append('TF')
            count_TF = count_TF + 1 
        elif df.iloc[x, 5] < value and df.iloc[x, 6] < value_hr:
            temp_list.append('TT_DOWN')
            count_TT_down = count_TT_down + 1
        else:
            temp_list.append('Error')
            count_error = count_error + 1
        
    result_list = [count_TT_up, count_TT_down, count_FT, count_TF, count_error, len(df)]


    