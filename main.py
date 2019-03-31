import json
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

HIGHSCHOOL_DATASET = 'Public_Highschool_Dataset.xlsx'
POC2_DATASET = 'Boston_Social_Vulnerability.xlsx'

CODE_TRANSLATOR = {'D': "Dangerous",
                   'C': 'Definitely Declining',
                   'B': 'Still Desireable',
                   'A': 'Best'}

ZIPCODER_REDLINE = {'02108': {'NA': 0.9, 'C': 0.05, 'B': 0.05},
                    '02109': {'NA': 1},
                    '02110': {'NA': 1},
                    '02111': {'D': 0.5, 'NA': 0.5},
                    '02113': {'D': 1},
                    '02114': {'D': 0.95, 'C': 0.5},
                    '02115': {'C': 0.5, 'D': 0.5},
                    '02116': {'D': 0.6, 'C': 0.2, 'B': 0.2},
                    '02118': {'D': 1},
                    '02119': {'D': 1},
                    '02120': {'D': 1},
                    '02121': {'C': 1},
                    '02122': {'D': 0.75, 'C': 0.25},
                    '02124': {'C': 0.9, 'B': 0.1},
                    '02125': {'C': 0.9, 'D': 0.1},
                    '02126': {'C': 0.9, 'B': 0.1},
                    '02127': {'NA': 0.5, 'C': 0.25, 'D': 0.25},
                    '02128': {'NA': .6, 'D': 0.2, 'C': 0.15, 'B': 0.5},
                    '02129': {'D': 0.6, 'NA': 0.4},
                    '02130': {'A': 0.15, 'B': 0.1, 'C': 0.75},
                    '02131': {'C': 1},
                    '02132': {'C': 0.6, 'B': 0.4},
                    '02134': {'NA': 0.3, 'D': 0.4, 'C': 0.3},
                    '02135': {'B': 0.1, 'C': 0.4, 'D': 0.5},
                    '02136': {'C': 1},
                    '02151': {'D': 0.5, 'C': 0.5},
                    '02152': {'B': .4, 'C': 0.5, 'D': 0.1},
                    '02163': {'NA': 1},
                    '02199': {'NA': 1},
                    '02203': {'NA': 1},
                    '02210': {'NA': 1},
                    '02215': {'C': 0.9, 'B': 0.1},
                    '02467': {'A': 0.9, 'B': 0.1}
                    }

NEIGHBORHOODS = {'ALLSTON': '02134', 
                 'BACKBAY': '02116',
                 'BAYVILLAGE': '02116',
                 'BEACONHILL': '02108',
                 'BRIGHTON': '02135',
                 'CHARLESTOWN': '02129',
                 'CHINATOWNLEATHERDISTRICT': '02111',
                 'DORCHESTER': ['02121', '02122', '02124', '02125'],
                 'DOWNTOWN': '02201',
                 'EASTBOSTON': '02128',
                 'LONGWOOD': '02115',
                 # the city of boston doesn't recognize longwood as it's own neighborhood and includes 02115 in fenway kenmore
                 'FENWAYKENMORE': '02215',
                 'HYDEPARK': '02136',
                 'JAMAICAPLAIN': '02130',
                 'MATTAPAN': '02126',
                 'MIDDORCHESTER': ['02121', '02122', '02124', '02125'],
                 'MISSIONHILL': ['02120', '02115'],
                 'NORTHEND': '02113',
                 'ROSLINDALE': '02131',
                 'ROXBURY': '02119',
                 'SOUTHBOSTON': '02127',
                 'SOUTHEND': '02118',
                 'WESTEND': '02114',
                 'WESTROXBURY': '02132'
                 }

def get_POC2_number_for_area(df2):
    area_POC2_number = {}

    #iterates through the list
    for i in df2.index:
        area = df2['Name'][i]
        num_of_people = df2['POC2'][i]
        # checks if we have seen this area before
        if area in area_POC2_number:
            curr_siz = area_POC2_number[area]['population']
            area_POC2_number[area] = {'population': curr_siz + num_of_people}
        else:
            #sets the POC2 population for that area
            area_POC2_number[area] = {'population': num_of_people}

    return area_POC2_number
        
    

def get_average_graduation_rate_for_zipcde(df):
    zipcode_avg_graduationrate = {}

    # iterates through public high school 
    for i in df.index:
        zipcode = df['ZIPCODE'][i]
        graduation_rate = df['Graduation_Rate'][i]
        # checks if we have seen this zipcode before 
        if zipcode in zipcode_avg_graduationrate:
            curr_avg = zipcode_avg_graduationrate[zipcode]['rate']
            curr_size = zipcode_avg_graduationrate[zipcode]['size']
            # calculates average graduation rate for the zipcode 
            zipcode_avg_graduationrate[zipcode] = {'rate': (curr_avg + graduation_rate) / (curr_size + 1),
                                                   'size': curr_size + 1}
        else:
            # sets the graduation rate for that zipcode 
            zipcode_avg_graduationrate[zipcode] = {
                'rate': graduation_rate, 'size': 1}

    return zipcode_avg_graduationrate


def main():

    df = pd.read_excel(HIGHSCHOOL_DATASET, sheet_name='Public_Schools')
    df2 = pd.read_excel(POC2_DATASET, sheet_name='Climate_Ready_Boston_Social_Vul')

    POC2_number_for_area = get_POC2_number_for_area(df2)
    print(POC2_number_for_area)

    zipcode_avg_graduationrate = get_average_graduation_rate_for_zipcde(df)
    #print(zipcode_avg_graduationrate)


main()
