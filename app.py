# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 21:04:41 2020

@author: dsmit
"""


"""
There are a few things I want this app to do. 
First, have you enter in something to then plot average score.
Other things?
...
"""





from flask import Flask, render_template, request, redirect
#"""
import alpha_vantage
import requests


from bokeh.layouts import row, column, widgetbox
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.io import curdoc, show

import pandas as pd
from bokeh.layouts import row
from bokeh.io import output_file, show
from bokeh.plotting import figure, save
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models.widgets import Dropdown
from bokeh.palettes import Spectral5
from bokeh.transform import factor_cmap
from bokeh.transform import dodge
from bokeh.models import ColumnDataSource, Select
from bokeh.io import curdoc
from alpha_vantage.timeseries import TimeSeries
from bokeh.embed import components 
from bokeh.io import output_file, show


"""
# Define a callback function: update_plot
def update_plot(attr, old, new):
    # If the new Selection is 'female_literacy', update 'y' to female_literacy
    if new == 'news': 
        dfreligionlong_news = dfreligionlong.loc[dfreligionlong['subreddit'] == 'news']
        grouped2 = dfreligionlong_news.groupby(['group', 'sentiment1'])['score'].aggregate(['mean'])
        grouped2 = grouped2.dropna()
        g = grouped2.unstack(level='sentiment1')
        g.columns = g.columns.droplevel()
        
        new_data = {'groups' : groups,
        'negative'   : g.negative.to_list(),
        'neutral'   : g.neutral.to_list(),
        'positive'   : g.positive.to_list()}
        source.data = new_data
    # Else, update 'y' to population
    else:
        dfreligionlong_news = dfreligionlong.loc[dfreligionlong['subreddit'] == 'news']
        grouped2 = dfreligionlong_news.groupby(['group', 'sentiment1'])['score'].aggregate(['mean'])
        grouped2 = grouped2.dropna()
        g = grouped2.unstack(level='sentiment1')
        g.columns = g.columns.droplevel()
        
        new_data = {'groups' : groups,
        'negative'   : g.negative.to_list(),
        'neutral'   : g.neutral.to_list(),
        'positive'   : g.positive.to_list()}
        source.data = new_data
# Create a dropdown Select widget: select    
select = Select(title="distribution", options=['news', 'population'], value='news')

# Attach the update_plot callback to the 'value' property of select
select.on_change('value', update_plot)

# Create layout and add to current document
layout = row(select, p)
curdoc().add_root(layout)
"""

"""
import urllib.request
url = 'https://www.dropbox.com/s/.../movie_data.csvhttps://www.dropbox.com/s/e0jw65of362fazs/comments_sent_text.csv?dl=0'
u = urllib.request.urlopen(url)
data = u.read()
u.close()


with open('movie_data.csv', "wb") as f :
   f.write(data)

"""

#dfm = pd.read_csv('https://www.dropbox.com/s/e0jw65of362fazs/comments_sent_text.csv?dl=1')




#This gets the dataset
def fetch(enter_text) :

    #df = pd.read_csv('C:/Users/Pablo/Documents/Data Incubator/Reddit/New/Test_App/Redd_Test_App\comments_sent_text.csv')
    #df = pd.read_csv('comments_sent_text.csv')
    
   # url = 'https://drive.google.com/file/d/1pAaMsB8Ei1kmbh3ogqyESIVCztkxeORL/view?usp=sharing'
#https://github.com/davidsmith1993/Redd_Test_App//main/comments_sent_text.csv
    #df = pd.read_csv(url)
    df = pd.read_csv('https://www.dropbox.com/s/e0jw65of362fazs/comments_sent_text.csv?dl=1')

    df_sample = df.sample(n = 50000)

    #enter_text = 'magic'
    df_sample['entered_text'] = df_sample['body'].str.contains(enter_text, case = False)

     
        
    #df = ColumnDataSource(new_data)
    dfentered = df_sample[['score', 'entered_text', 'sentiment1']]

    dfentered.loc[dfentered['entered_text'] == True, 'entered_text'] = dfentered['score']

    dfentered = dfentered[['score', 'entered_text', 'sentiment1']]
    dfenteredlong = pd.melt(dfentered, id_vars=['sentiment1'], var_name = 'group',  value_name = 'score')
    dfenteredlong = dfenteredlong[dfenteredlong.score != False]
    dfenteredlong['score'] = dfenteredlong.score.astype(float)

    return(df_sample, dfenteredlong)








def make_figure(df_sample, dfenteredlong):
    
    
    
    p=figure()

    
    grouped2 = dfenteredlong.groupby(['group', 'sentiment1'])['score'].aggregate(['mean'])
    grouped2 = grouped2.dropna()
    g = grouped2.unstack(level='sentiment1')
    g.columns = g.columns.droplevel()

    sentiment = ['negative', 'neutral', 'positive']

    groups = dfenteredlong['group'].unique().tolist()
    data = {'groups' : groups,
            'negative'   : g.negative.to_list(),
            'neutral'   : g.neutral.to_list(),
            'positive'   : g.positive.to_list()}
    source = ColumnDataSource(data)
    p = figure(x_range=groups, y_range=(-10, 100), title="Title to add",
               toolbar_location=None,  tooltips="@groups $name: @$name")

    p.vbar(x=dodge('groups', -0.25, range=p.x_range), top='negative', width=0.2, source=source,
           color="#c9d9d3", legend_label="negative", name = "negative")
    p.vbar(x=dodge('groups', 0, range=p.x_range), top='neutral', width=0.2, source=source,
           color="#718dbf", legend_label="neutral", name = "neutral")
    p.vbar(x=dodge('groups', 0.25, range=p.x_range), top='positive', width=0.2, source=source,
           color="#e84d60", legend_label="positive", name = "positive")

    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
   # show(p)








    output_file('templates/plot.html')
    save(p)
    script, div=components(p)
    
    return(script, div)




app = Flask(__name__)

app.vars = {}



@app.route('/')
def index():
  return render_template('index.html')


@app.route('/resume')
def resume():
  return render_template('resume.html')


@app.route('/ex_analysis1')
def ex_analysis1():
  return render_template('ex_analysis1.html')


@app.route('/ex_analysis2')
def ex_analysis2():
  return render_template('ex_analysis2.html')

@app.route('/model_fits')
def model_fits():
  return render_template('model_fits.html')



#This was my page to plot
@app.route('/plotpage', methods=['POST'])
def plotpage():
    tickStr=request.form['chosen_word']
    
    app.vars['ticker']=tickStr.upper()
    data, data2 =fetch(app.vars['ticker'])
    script,div=make_figure(data, data2)
    return render_template('plot.html', script=script, div=div)



if __name__ == '__main__':
    app.run(port=33507)

