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


import pickle##dump the model into a file
from bokeh.layouts import row, column, widgetbox
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.io import curdoc, show
from bokeh.resources import CDN
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

import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
nltk.download('punkt')


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
def fetch(enter_text, subreddit):

    #enter_text = 'All'
    #df = pd.read_csv('C:/Users/Pablo/Documents/Data Incubator/Reddit/New/Test_App/Redd_Test_App\comments_sent_text.csv')
    #df = pd.read_csv('comments_sent_text.csv')
    
   # url = 'https://drive.google.com/file/d/1pAaMsB8Ei1kmbh3ogqyESIVCztkxeORL/view?usp=sharing'
#https://github.com/davidsmith1993/Redd_Test_App//main/comments_sent_text.csv
    #df = pd.read_csv(url)
    
    #subreddit = 'science'
    #this is what I will be using I think
    #df = pd.read_csv('https://www.dropbox.com/s/e0jw65of362fazs/comments_sent_text.csv?dl=1')

    #df_sample = df.sample(n = 150000)
    #df = pd.read_csv('C:/Users\Pablo\Documents\Data Incubator/Reddit/New/Data/df_all_cleaned_dropped_95.csv')

    
    #df_sample.to_csv(r'C:\Users\Pablo\Documents\Data Incubator\Reddit\New\Test_App\Redd_Test_App\comments_sent_text_small.csv') 
    df_sample =  pd.read_csv('comments_sent_text_small.csv')
    if subreddit == 'All':
        df_sample = df_sample
    else:
        df_sample = df_sample.loc[df_sample['subreddit'] == subreddit]
    
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








def make_figure(df_sample, dfenteredlong, enter_text):
    
    
    
    p=figure()

    
    grouped2 = dfenteredlong.groupby(['group', 'sentiment1'])['score'].aggregate(['mean'])
    grouped2 = grouped2.dropna()
    g = grouped2.unstack(level='sentiment1')
    g.columns = g.columns.droplevel()

    sentiment = ['negative', 'neutral', 'positive']

    groups = [enter_text, 'Average Subreddit Comment Score']
    data = {'groups' : groups,
            'negative'   : g.negative.to_list(),
            'neutral'   : g.neutral.to_list(),
            'positive'   : g.positive.to_list()}
    source = ColumnDataSource(data)
    p = figure(x_range=groups,  title="Average comment score for " + enter_text,
               toolbar_location=None,  tooltips="@groups $name: @$name")

    p.vbar(x=dodge('groups', -0.25, range=p.x_range), top='negative', width=0.2, source=source,
           color="#696969", legend_label="negative", name = "negative")
    p.vbar(x=dodge('groups', 0, range=p.x_range), top='neutral', width=0.2, source=source,
           color="#FFFF00", legend_label="neutral", name = "neutral")
    p.vbar(x=dodge('groups', 0.25, range=p.x_range), top='positive', width=0.2, source=source,
           color="#add8e6", legend_label="positive", name = "positive")
    p.title.text_font_size = "20px"
    p.xaxis.major_label_text_font_size = "20px"
    p.yaxis.axis_label = 'Comment Score'
    p.yaxis.axis_label_text_font_size = "20pt"
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    #show(p)








    #output_file('templates/plot.html')
    save(p)
    script, div=components(p)
    
    return(script, div)




def model_it(comment, time_h, time_d, gild, par_score):
    
   
    #This opens
    ##loading the model from the saved file
    with open('model.bin', 'rb') as f_in:
        model = pickle.load(f_in)    
    
    


    
    """Then we test it with defined features"""

    #comment = 'I have a large dog and I love him'
    
    body_len = len(comment)
    #subreddit = 'askreddit'
    #time_h = 1
    #time_d = 2
    #gild = 0
    #par_score = 500
    
    
    #Our goal here is to conduct sentiment analyses of the comments
    sid = SentimentIntensityAnalyzer()
    
    
    scores = sid.polarity_scores(comment)
    sentiment = []
    
    
    if scores["compound"] >= 0.05:
        sentiment = 'positive'
        s = [0, 0, 1]
        
    elif scores["compound"] <= -0.05:
        sentiment = 'negative'
        s = [1, 0 ,0 ]
    else:
        sentiment = 'neutral'
        s = [0 , 1 ,0 ]






    c_test = [[par_score, body_len, gild, time_d, time_h] + s]

    c_pred= model.predict(c_test)
    return c_pred
















app = Flask(__name__)

app.vars = {}



@app.route('/')
def index():
  return render_template('index.html')
@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/resume')
def resume():
  return render_template('resume.html')


@app.route('/ex_analysis1')
def ex_analysis1():
  return render_template('ex_analysis1.html')


@app.route('/ex_analysis2')
def ex_analysis2():
  return render_template('ex_analysis2.html')


@app.route('/ex_analysis3')
def ex_analysis3():
  return render_template('ex_analysis3.html')

@app.route('/model_fits')
def model_fits():
  return render_template('model_fits.html')


@app.route('/word_freq')
def word_freq():
  return render_template('word_freq.html')

@app.route('/word_freq_sub_all')
def word_freq_sub_all():
  return render_template('word_freq_sub_all.html')

@app.route('/word_freq_sub_top')
def word_freq_sub_top():
  return render_template('word_freq_sub_top.html')

@app.route('/word_freq_sub_bottom')
def word_freq_sub_bottom():
  return render_template('word_freq_sub_bottom.html')


"""
@app.route('/main_graph')
def main_graph():
  #tickStr=request.form['chosen_word']
 # app.vars['ticker']=tickStr.upper() 
 # data, data2 =fetch(app.vars['ticker'])
  #script,div=make_figure(data, data2)
  
  
  return render_template('main_graph.html')
  #return render_template('main_graph.html, script=script, div=div')
    
"""



#This was my page to plot
@app.route('/main_graph', methods=['POST', 'GET'])
def main_graph():
    if request.method == 'POST':
        #subreddit = request.form['subreddit']
        form_data = request.form
        subreddit = form_data.get('chosen_reddit')
        
        tickStr = form_data.get('chosen_word')
        #tickStr=request.form['chosen_word']
        
        app.vars['ticker']=tickStr
        app.vars['chosen_reddit']=subreddit
        #app.vars['subreddit'] = request.form['subreddit']
        #data, data2 =fetch('magic')
        data, data2 =fetch(app.vars['ticker'], app.vars['chosen_reddit'])
        script,div=make_figure(data, data2, app.vars['ticker'])
    
        return render_template('main_graph.html', script=script, div=div)

    elif request.method == 'GET':
        return render_template('main_graph.html')
    
    
    
    
    
 
    
    
#This was my page to plot
@app.route('/deployed', methods=['POST', 'GET'])
def deployed():
    if request.method == 'POST':
        form_data = request.form
        comment = form_data.get('comment')
        time_h = form_data.get('hour')
        time_d = form_data.get('day')
        gild = form_data.get('gilded')
        par_score= form_data.get('par_score')
        
        prediction=model_it(comment, time_h, time_d, gild, par_score)
        return render_template('deployed.html', prediction = prediction)

    elif request.method == 'GET':
        return render_template('deployed.html')    

if __name__ == '__main__':
    app.run(port=33507)

