# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 16:28:06 2016

@author: LAA037
"""
import climb
data = climb.get_data()
############# test ###############

def test_print_gunks_count():
    count = 0
    for line in data:
        if 'The Gunks' in line['Location'] :
            count += 1
    print count


def test_print_gunks_routes():
    output = []    
    for line in data:
        if ('The Gunks' in line['Location']) &  (line['Route'] not in output):
            #print line['Route']            
            output.append(line['Route'])
    classics = ['''Three Pines''','''Gelsa''','''Jackie''','''Horseman''','''High Exposure''','''Frog's Head''','''Disneyland''','''Shockley's Ceiling''','''Madame Grunnebaum's Wulst''','''Yellow Ridge''','''Strictly From Nowhere''','''Limelight''','''Ken's Crack''','''Something Interesting''','''Cascading Crystal Kaleidoscope (CCK)''','''Arrow''','''Double Crack''','''Son of Easy O''','''Birdland''','''Modern Times''','''Apoplexy''','''MF''','''Directissima''','''Ants' Line''','''Bonnie's Roof''','''CCK Direct''','''Never Never Land''','''The Dangler''','''Bird Cage''','''Feast of Fools''','''Welcome to the Gunks''','''Nosedive''','''Directississima''','''Nurse's Aid''','''Erect Direction''','''Ridicullissima''','''Fat City Direct''','''Graveyard Shift''','''10,000 Restless Virgins''','''Coexistence''','''Carbs and Caffeine''','''The Yellow Wall''','''Enduro Man's Longest Hangout''','''Kligfield's Follies''','''Suppers Ready''']

    for route in classics:
        if route not in output:
            print route


def test_unclimbed_gunks_classic(user):    

    classics = ['''Three Pines''','''Gelsa''','''Jackie''','''Horseman''','''High Exposure''','''Frog's Head''','''Disneyland''','''Shockley's Ceiling''','''Madame Grunnebaum's Wulst''','''Yellow Ridge''','''Strictly From Nowhere''','''Limelight''','''Ken's Crack''','''Something Interesting''','''Cascading Crystal Kaleidoscope (CCK)''','''Arrow''','''Double Crack''','''Son of Easy O''','''Birdland''','''Modern Times''','''Apoplexy''','''MF''','''Directissima''','''Ants' Line''','''Bonnie's Roof''','''CCK Direct''','''Never Never Land''','''The Dangler''','''Bird Cage''','''Feast of Fools''','''Welcome to the Gunks''','''Nosedive''','''Directississima''','''Nurse's Aid''','''Erect Direction''','''Ridicullissima''','''Fat City Direct''','''Graveyard Shift''','''10,000 Restless Virgins''','''Coexistence''','''Carbs and Caffeine''','''The Yellow Wall''','''Enduro Man's Longest Hangout''','''Kligfield's Follies''','''Suppers Ready''']
    output = []
    #dictionary = dict()
 
    already_climbed = [x['Route'] for x in data if x['user'] == user]
    
    for x in classics:
        if (x not in already_climbed) & (x not in output):
            output.append(x)
    return output
    
assert  'Directissima' in test_unclimbed_gunks_classic('YvonneYZ')
print test_unclimbed_gunks_classic('Molly')