import numpy as np
import pandas as pd

from bokeh.models import ColumnDataSource, CategoricalColorMapper, Div, Panel
from bokeh.models.widgets import Select, RangeSlider, TextInput, Tabs, DataTable
from bokeh.layouts import column, row, WidgetBox
from bokeh.plotting import figure
from bokeh.palettes import d3


def o3_tab():

    def make_dataset(select_site, text_input, slider_time):
        global color_map, convert_t, groupby
        path = '/Users/farewell/Documents/EMCT/WOT/Bokeh_app/data/'
        df = pd.read_csv(path + select_site.value + '.csv')
        fun = pd.read_csv(path + '2017_format.csv')
        # checke time 
        time_start = slider_time.value[0]
        time_end = slider_time.value[1]
        assert time_start < time_end, "Start must be less than end!"

        # filter data
        df = df[(df['時間'] >= time_start) & (df['時間'] <= time_end)]

        # calculate thershold converted by linear regression
        fun = fun[fun['Location'] == select_site.value].values
        funList = fun.tolist()

        thersheld = abs(float(text_input.value))
        convert_t = (thersheld - funList[0][1]) / funList[0][2]

        # condition defined
        condition = []

        moveValue = list(df['移動平均'])
        hourValue = list(df['小時值'])

        for ix in range(len(df)):
            #if value >
            if moveValue[ix] >= float(text_input.value) and hourValue[ix] >= round(convert_t, 2):
                condition.append('TP')
            elif moveValue[ix]>= float(text_input.value) and hourValue[ix] < round(convert_t, 2):
                condition.append('FP')
            elif moveValue[ix] < float(text_input.value) and hourValue[ix] > round(convert_t, 2):
                condition.append('FN')
            elif moveValue[ix] < float(text_input.value) and hourValue[ix] < round(convert_t, 2):
                condition.append('TN')
            else:
                condition.append('ERROR')

        df['cat'] = condition
        df = df.loc[:, ['移動平均', '小時值', 'cat']]

        groupby = df.groupby('cat')['小時值'].size()

                # color 
        palette = d3['Category10'][len(df['cat'].unique())]
        color_map = CategoricalColorMapper(factors=df['cat'].unique(),palette=palette)
        
        return ColumnDataSource(df)


    def make_plot(select_site, src):
        #global 

        p = figure(plot_width=700,
                    plot_height = 700, 
                    #title = select_site.value + ' 8小時移動平均與1小時散佈圖',
                    x_axis_label='8小時移動平均',
                    y_axis_label='1小時實際數值')
        p.title.text = str(select_site.value) + ' 8小時移動平均與1小時散佈圖'
        
        p.scatter(x='移動平均', y='小時值', color={'field': 'cat', 'transform': color_map}, legend='cat', source=src)
        
        #table = DataTable(df)
        #vline = Span(location=float(text_input.value), dimension='height', line_color='red', line_width=3)
        #hline = Span(location=float(convert_t), dimension='width', line_color='green', line_width=3)
        #p.renderers.extend([vline])
        return p

    def update(attr, old, new):
        global convert_t
        new_src = make_dataset(select_site, text_input, slider_time)
        src.data.update(new_src.data)

        p.title.text = str(select_site.value) + ' 8小時移動平均與1小時散佈圖'
        txt.text = '8小時移動平均: ' + str(text_input.value) + '<br/>' + '1小時實際推估值: ' + str(float(round(convert_t, 2))) + '<br/><br/>' + 'TP次數: ' + str(groupby['TP']) + '<br/>' + 'FN次數: ' + str(groupby['FN']) + '<br/>' + 'FP次數: ' + str(groupby['FP']) + '<br/>' + 'TN次數: ' + str(groupby['TN']) + '<br/><br/>' + 'Recall(召回率): ' + str(round(groupby['TP'] / (groupby['TP'] + groupby['FN']+ 0.001),2)*100) + '%' + '<br/>' + 'Precesion(精確率): ' + str(round(groupby['TP'] / (groupby['TP'] + groupby['FP']+ 0.001),2)*100) + '%'
        
        #p.title.update(select_site.value)
        #div = Div(text=str(text_input.value))
    #def text_update(attr, old, new):

    select_site = Select(title='測站名稱', value='古亭', options=['二林', '三義', '土城', '士林', '大里', '大園', '大寮', '小港', '中山', '中壢', '仁武', '斗六', '冬山', '古亭', '左營', '平鎮', '永和', '安南', '朴子', '汐止', '竹山', '竹東', '西屯', '沙鹿', '宜蘭', '忠明', '松山', '板橋', '林口', '林園', '花蓮', '金門', '前金', '前鎮', '南投', '屏東', '恆春', '美濃', '苗栗', '埔里', '桃園', '馬公', '馬祖', '基隆', '崙背', '淡水', '麥寮', '善化', '富貴角', '復興', '湖口', '菜寮', '陽明', '新竹', '新店', '新莊', '新港', '新營', '楠梓', '萬里', '萬華', '嘉義', '彰化', '臺西', '臺東', '臺南', '鳳山', '潮州', '線西', '橋頭', '頭份', '龍潭', '豐原', '關山', '觀音'])
    select_site.on_change("value", update)

    text_input = TextInput(value='71', title='Thersheld: ')
    text_input.on_change("value", update)

    slider_time = RangeSlider(start=0, end=23, value=(0, 23), step=1, title='Push Notification: ')
    slider_time.on_change('value', update)



    #div = Div(text=str(text_input.value), height=300)
    #div.on_change('text', update)

    initial= select_site

    src = make_dataset(initial, text_input, slider_time)

    p = make_plot(select_site, src)

    # output
    controls = WidgetBox(select_site, text_input, slider_time)

    txt = Div(text='8小時移動平均: ' + str(text_input.value) + '<br/>' + 
                   '1小時實際推估值: ' + str(float(round(convert_t, 2))) + '<br/><br/>' +
                    'TP次數: ' + str(groupby['TP']) + '<br/>' +
                    'FN次數: ' + str(groupby['FN']) + '<br/>' +
                    'FP次數: ' + str(groupby['FP']) + '<br/>' +
                    'TN次數: ' + str(groupby['TN']) + '<br/><br/>' +
                    'Recall(召回率): ' + str(round(groupby['TP'] / (groupby['TP'] + groupby['FN']+ 0.001),2)*100) + '%' + '<br/>' +
                    'Precesion(精確率): ' + str(round(groupby['TP'] / (groupby['TP'] + groupby['FP']+ 0.001),2)*100) + '%'
                    
                    
    )
    #divs = WidgetBox(txt, txt)
    ##
    layout = row(controls, p, txt)

    # Make a tab with the layout 
    tab = Panel(child=layout, title = 'O3 Notification（recall & precision)')

    return tab
