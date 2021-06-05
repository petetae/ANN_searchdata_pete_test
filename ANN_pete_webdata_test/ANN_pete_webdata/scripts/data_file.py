import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.colors
from collections import OrderedDict
import requests
from xml.etree import ElementTree


def get_ANN_data(searchQuery = ""):
# Get AnimeNewsNetwork data and then clean for plot

  # def get_ANN_data(searchQuery = ""):
  input_data = searchQuery
  titleSearchQuery = '?title=~' + input_data
  url = 'https://cdn.animenewsnetwork.com/encyclopedia/api.xml' + titleSearchQuery 
  # + '&nlist=500'
  print('url used: ', url)
  response = requests.get(url)
  tree = ElementTree.fromstring(response.content)
  df = extract_anime_data(tree)
  return df
  

def extract_anime_data(xml_data):
  column_names = ['id','maintitle','staffcount','staffname','ratings']
  if xml_data.findall('anime') == []:
      return pd.DataFrame(columns = column_names)

  id_list = []
  maintitle_list = []
  staffcount_list = []
  staffname_list = []
  ratings_list = []

  for anime_data in xml_data.findall('anime'):
      id_list.append(anime_data.attrib.get('id'))

      for maintitle_data in anime_data.findall('info'):
          if maintitle_data.get('type') == 'Main title':
              maintitle_list.append(maintitle_data.text)

      staffcount = 0
      staffname = ''
      for staff_data in anime_data.findall('staff'):

          for person_data in staff_data.findall('person'):
              staffcount+=1
              if staffname == '':
                  staffname = person_data.text
              else:
                  staffname = staffname + ',' + person_data.text
      staffcount_list.append(staffcount)
      staffname_list.append(staffname)

      if anime_data.findall('ratings') == []:
        ratings_list.append(0.0)
      else:
            # tree.findall('anime')[1].findall('ratings')[0].get('weighted_score')
            # tree.findall('anime')[0].findall('ratings') == []
        ratings_list.append(float(anime_data.findall('ratings')[0].get('weighted_score')))

  print('maintitle_list: ', maintitle_list)
  df = pd.concat([pd.DataFrame(id_list,columns=['id'])
  ,pd.DataFrame(maintitle_list,columns=['maintitle'])
  ,pd.DataFrame(staffcount_list,columns=['staffcount'])
  ,pd.DataFrame(staffname_list,columns=['staffname'])
  ,pd.DataFrame(ratings_list,columns=['ratings'])]
  ,axis=1)
  return df


def return_figures(searchQuery = ""):
  """Creates four plotly visualizations using the World Bank API

    Args:
        Search anime name to show stats and information

    Returns:
        list (dict): list containing the plotly visualisations
        - anime data table (row1)
        - anime plot 1 (row2)
        - anime plot 2 (row2)

  """
  print('searchQuery in return_figures: ', searchQuery)
  df = get_ANN_data(searchQuery)

  # if df.empty:
  #   print('empty no anime data')
  # else:
  #   #     Continue to code for plots etc from this data
  #   print(df)
  
  # first chart plots arable land from 1990 to 2015 in top 10 economies 
  # as a line chart

  graph_one = []

  graph_one.append(
      go.Table(
      header = dict(values=['id','maintitle','staffcount','staffname','ratinigs']),
      cells = dict(values=[df['id'], df['maintitle'],df['staffcount'], df['staffname'],df['ratings']])
      )
  )  
  layout_one = dict(title = 'Table data show')


  graph_two = []

  graph_two.append(
      go.Bar(
      x = df['maintitle'],
      y = df['staffcount']
      )
  )
    

  layout_two = dict(title = 'Search data title and staff count',
                xaxis = dict(title = 'Anime',),
                yaxis = dict(title = 'Staff count'),
                automargin = True
                )


  graph_three = []

  graph_three.append(
      go.Line(
      x = df['maintitle'],
      y = df['ratings']
      )
  )
    

  layout_three = dict(title = 'Search data title and ratings',
                xaxis = dict(title = 'Anime',),
                yaxis = dict(title = 'Ratings')

                )

  # second chart plots ararble land for 2015 as a bar chart
  # graph_two = []
  # df_one.sort_values('value', ascending=False, inplace=True)
  # df_one = df_one[df_one['date'] == '2015'] 

  # graph_two.append(
  #     go.Bar(
  #     x = df_one.country.tolist(),
  #     y = df_one.value.tolist(),
  #     )
  # )

  # layout_two = dict(title = 'Hectares Arable Land per Person in 2015',
  #               xaxis = dict(title = 'Country',),
  #               yaxis = dict(title = 'Hectares per person'),
  #               )

  # # third chart plots percent of population that is rural from 1990 to 2015
  # graph_three = []
  # df_three = pd.DataFrame(data_frames[1])
  # df_three = df_three[(df_three['date'] == '2015') | (df_three['date'] == '1990')]

  # df_three.sort_values('value', ascending=False, inplace=True)
  # for country in countrylist:
  #     x_val = df_three[df_three['country'] == country].date.tolist()
  #     y_val =  df_three[df_three['country'] == country].value.tolist()
  #     graph_three.append(
  #         go.Scatter(
  #         x = x_val,
  #         y = y_val,
  #         mode = 'lines',
  #         name = country
  #         )
  #     )

  # layout_three = dict(title = 'Change in Rural Population <br> (Percent of Total Population)',
  #               xaxis = dict(title = 'Year',
  #                 autotick=False, tick0=1990, dtick=25),
  #               yaxis = dict(title = 'Percent'),
  #               )

  # # fourth chart shows rural population vs arable land as percents
  # graph_four = []
  # df_four_a = pd.DataFrame(data_frames[2])
  # df_four_a = df_four_a[['country', 'date', 'value']]
  
  # df_four_b = pd.DataFrame(data_frames[3])
  # df_four_b = df_four_b[['country', 'date', 'value']]

  # df_four = df_four_a.merge(df_four_b, on=['country', 'date'])
  # df_four.sort_values('date', ascending=True, inplace=True)

  # plotly_default_colors = plotly.colors.DEFAULT_PLOTLY_COLORS

  # for i, country in enumerate(countrylist):

  #     current_color = []

  #     x_val = df_four[df_four['country'] == country].value_x.tolist()
  #     y_val = df_four[df_four['country'] == country].value_y.tolist()
  #     years = df_four[df_four['country'] == country].date.tolist()
  #     country_label = df_four[df_four['country'] == country].country.tolist()

  #     text = []
  #     for country, year in zip(country_label, years):
  #         text.append(str(country) + ' ' + str(year))

  #     graph_four.append(
  #         go.Scatter(
  #         x = x_val,
  #         y = y_val,
  #         mode = 'lines+markers',
  #         text = text,
  #         name = country,
  #         # textposition = 'top'
  #         )
  #     )

  # layout_four = dict(title = '% of Population that is Rural versus <br> % of Land that is Forested <br> 1990-2015',
  #               xaxis = dict(title = '% Population that is Rural', range=[0,100], dtick=10),
  #               yaxis = dict(title = '% of Area that is Forested', range=[0,100], dtick=10),
  #               )


  # append all charts
  figures = []
  figures.append(dict(data=graph_one, layout=layout_one))
  figures.append(dict(data=graph_two, layout=layout_two))
  figures.append(dict(data=graph_three, layout=layout_three))
  # figures.append(dict(data=graph_four, layout=layout_four))

  return figures
