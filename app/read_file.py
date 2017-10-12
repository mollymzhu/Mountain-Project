# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 20:25:29 2016

@author: laa037

This is a back-up method if read_html doesn't work due to proxy or fire-wall
"""


import csv
import glob

################### get data #################
def get_raw_data(filename):  
    '''
    get data from a single file
    '''

    raw_data = []
    first_line = ''
    with open(filename) as source:
        first_line = source.readline()
        user_name  = first_line.split(' ')[3]
        user_name = user_name.replace(',','')
        user_name = user_name.replace('\n','')
        rdr = csv.DictReader(source)
        for line in rdr:
            raw_data.append(line)
    for line in raw_data:
        line['user'] = user_name
    return raw_data
    #print raw_data['Route']

def get_data(filename_list = glob.glob('./*.csv')):
    
    '''
    Return data from a list of files
    '''

    output = []
    for filename in filename_list:
        try:
            data = get_raw_data(filename)
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
        except:
            print "Error: can not read " + filename
    return output
    
'''
# not sure if I want data for routes only....
# let me think think..

def get_routes(data=get_data()):
    output = dict()

    for x in data:
        if x['route_ID'] in output:
            pass
        else:
 #           output.append([x['route_ID'],x['Route'],x['Location'],x['rating']])
            output[x['route_ID']]=[x['Route'],x['Location'],x['area'],x['rating']]
    #print output
    return output
 '''