# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 22:11:20 2016

@author: Shevjensen
"""

import urllib2
#import requests
#from lxml import html
import re
import csv

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)
    
link = 'https://www.mountainproject.com/u/molly-z//110619029?action=ticks&&export=1'

def read_html(link):
    req = urllib2.Request(link)
    response = urllib2.urlopen(req)
    the_page = response.read()
    page_split = the_page.split('\n')
    output  = []
    for line in page_split:
        new_line = line.split('|')
        try:
            new_line[2] = remove_tags(new_line[2])
        except:
            pass
        try:
            if remove_tags(new_line[0])!='':
                output.append(new_line) 
        except:
            pass
        
    #output
    user = output[0][0].split(' ')[3]
    keys = output[1]
    data = []
    for x in output[2:]:
      
      line = {keys[i]: x[i] for i in range(len(keys))}
      line['user'] = user
      data.append(line)

    return data

'''

page = requests.get(link)

tree = html.fromstring(page.content)
rating = tree.xpath('//span[@class="rateYDS"]/text()')
numerical_rating = tree.xpath('//span[@class="rateEwbanks"]/text()')

'''
def read_all_links(filename = 'input.csv'):
    
    data = []
    #single_user_data
    with open(filename) as source:
      reader = csv.reader(source)
      for line in reader:
          link = line[0]
          data += read_html(link)
            
    output = []
    for x in data:
        x['route_ID']=x['URL'].split('/')[-1]           
        x['rating'] = x['Rating'].split(' ')[0]

        if x['rating'][0] == '5':
            x['type'] = 'rock'
        elif x['rating'][:2] == 'WI':
            x['type'] = 'ice'
        elif x['rating'][0] == 'V':
            x['type'] = 'boulder'
        else:
            x['type'] = 'rock'
        #need better logic here to handle non-YDS ratings    
        x['numerical_rating'] = ''
        if x['type'] == 'rock':
            try:
                x['numerical_rating'] = x['Rating'].split(' ')[2]
            except:
                pass
        if x['Style'] != '':
            pass
        else:
            notes = x['Notes'].lower()                    
            if ('follow' in notes) | ('second' in notes) :
                x['Style'] = 'Follow'
                
            elif  ('lead' in notes) | ('os' in notes) | ('redpoint' in notes) | ('onsight' in notes):
                x['Style'] = 'Lead' 
                
            elif ('tr' in notes) | ('top rope' in notes) | ('toprope' in notes):
                x['Style'] = 'TR'                    
        x['location'] = x['Location'].split(':')[0].strip()
        #need better logic here            
        x['area'] = ''
        if x['location'] != 'International':
            try:
                x['area'] = x['Location'].split(':')[1].strip()
                #x['crag'] = x['Location'].split(':')[2].strip()
            except:
                print 'can not get area or crag: ' + x['Route'] + ', ' + x['Location']
        output.append(x)
    return output