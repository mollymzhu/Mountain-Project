# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 17:15:45 2016

@author: laa037
"""
import csv
#import os
#import glob
import read_html



data = read_html.read_all_links()
#routes = get_routes()
YZ = 'YvonneYZ'
    
###################### Core Functions ######################
  
def get_date_of_climb(route,user='Molly',data=data):
    if user == '':
        return [x['Date']+', '+x['user'] for x in data if x['Route'] == route]
    else:
        return [x['Date'] for x in data if (x['Route'] == route) & (x['user'] == user)]


def get_region(region,data=data):
    output = []
    for line in data:
        if region.lower() in line['Location'].lower():
            output.append(line)
    return output

    
def get_unclimbed(region,min_star=2.5,climbed_by = '', unclimbed_by = 'Molly'):
    region_data = get_region(region) 
    output = []
    #dictionary = dict()
    pool = []
    if climbed_by != '':
        pool = [[x['Route'],x['rating'],','.join(map(str, x['Location'].split(':')[2:])),x['numerical_rating']] for x in region_data if (x['user'] == climbed_by) & (float(x['Avg Stars']) > min_star)]
    else:
        pool = [[x['Route'],x['rating'],','.join(map(str, x['Location'].split(':')[2:])),x['numerical_rating']] for x in region_data if float(x['Avg Stars']) >= min_star] 
    
    #pool = get_region(region, pool)
    if unclimbed_by != '':
        already_climbed = [x['Route'] for x in region_data if x['user'] == unclimbed_by]
    else:
        already_climbed = [x['Route'] for x in region_data]
        
    for x in pool:
        if (x[0] not in already_climbed) & (x not in output):
            output.append(x)
    output.sort(key=lambda x: x[3]) 
    output = [x[:-1] for x in output]     
    return output

def print_my_unclimbed(region,min_star=2.5,user='Molly'):
    output = []
    if type(user) is str:
        my_unclimbed=get_unclimbed(region,min_star,unclimbed_by = user)
        #print region
        for x in my_unclimbed:
            if (x[1][:3] in ['5.5','5.6','5.7','5.8','5.9']) | ('5.10' in x[1]):
                #print x
                output.append(x)

    elif type(user) is list:
        output_list = []
        for each_user in user:
            my_unclimbed  = get_unclimbed(region,min_star,unclimbed_by = each_user)
            if output_list == []:
                output_list = my_unclimbed 
            else:
                output_list = [x for x in output_list if x in my_unclimbed]
        for x in output_list:
            if (x[1][:3] in ['5.5','5.6','5.7','5.8','5.9']) | ('5.10' in x[1]):
                output.append(x)
    filename = 'output\unclimbed_' + user + '_' + region+'.csv'            
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Region: ',region])
        writer.writerow(['Climber: ',user])
        writer.writerow(['Min star: ',min_star])
        writer.writerow(['Routes unclimbed by climber(s)'])
        writer.writerow('\n')
        
        for x in output:
            writer.writerow(x)

def get_climbed(region,user):
    region_data = get_region(region) 
    output = [[x['Route'],x['rating'],x['Style'],x['Date'],','.join(map(str, x['Location'].split(':')[2:])),x['numerical_rating']] for x in region_data if (x['user'] == user)]
    output.sort(key=lambda x: (x[5],x[0]) )
    output = [x[:-1] for x in output]     
    return output
    
def print_unlead(region,user):  
    lead = []
    user_data = get_climbed(region,user)
    for x in user_data:
        if (x[0] not in lead ) & (x[2] == 'Lead'):
            #print 'append'+x[0]
            lead.append(x[0])

    output = []
    for x in user_data:
        if (x[0] not in lead) & (x not in output):
            output.append(x)
    #for x in output:
        #print x
    filename = 'output\unlead_' + user + '_' + region+'.csv'
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Region: ',region])
        writer.writerow(['Climber: ',user])
        writer.writerow(['Blank notes default to follow'])
        writer.writerow(['Routes followed but not lead by climber:'])
        writer.writerow('\n')
        
        for x in output:
            writer.writerow(x)   
            
# DO THE WORK NOW!!!!!!!!!!!!!!!!!
print_my_unclimbed('new river',min_star=2.5,user='Molly')
print_unlead('gunks',YZ) 

        
if __name__ == "__main__":
    pass