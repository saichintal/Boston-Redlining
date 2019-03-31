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

NEIGHBORHOODS = {'Allston': {'zipcode': ['02134'], 'population': 28821, 'code': 'B'},
                'Back Bay': {'zipcode': ['02116'], 'population': 21844,'code': 'D'},
                'Beaconhill': {'zipcode': ['02108'], 'population': 9943,'code': 'NA'},
                'Brighton': {'zipcode': ['02135'], 'population': 45977,'code': 'C'},
                'Charlestwon':{'zipcode': ['02129'], 'population': 16439,'code': 'D'},
                'Chinatown':{'zipcode': ['02111'], 'population': 7510,'code': 'D'},
                'Dorchester':{'zipcode': ['02121', '02122', '02124', '02125'], 'population': 88333,'code': 'C'},
                'Downtown': {'zipcode': ['02201'], 'population': 1976,'code': 'NA'},
                'East Boston': {'zipcode': ['02118'], 'population': 40508,'code': 'B'},
                'Longwood': {'zipcode': ['02115'], 'population': 1754,'code': 'D'},
                'Fenway': {'zipcode': ['02215'], 'population': 21174,'code': 'D'},
                'Hyde Park': {'zipcode': ['02136'], 'population': 31845,'code': 'C'},
                'Jamaica Plain': {'zipcode': ['02130'], 'population': 41262,'code': 'A'},
                'Mattapan': {'zipcode': ['02126'], 'population': 34391,'code': 'C'},
                'Mission Hill': {'zipcode': ['02120'], 'population': 13929,'code': 'D'},
                'North End': {'zipcode': ['02113'], 'population': 10605,'code': 'D'},
                'Roslindale':{'zipcode': ['02131'], 'population': 35945,'code': 'C'},
                'Roxbury': {'zipcode': ['02119'], 'population': 52534,'code': 'D'},
                'South Boston': {'zipcode': ['02127'], 'population': 11096,'code': 'C'},
                'South End': {'zipcode': ['02118'], 'population': 33638,'code': 'D'},
                'West End': {'zipcode': ['02114'], 'population': 5330,'code': 'D'},
                'West Roxbury': {'zipcode': ['02132'], 'population': 30442,'code': 'C'}
                }


def get_neighborhood_by_zipcode(zipcode): 
    for neighborhood, value in NEIGHBORHOODS.items():
        results = list(map(int, value['zipcode'])) # converts list of string to list of ints 
        if zipcode in results: # checks if zipcode is part of the neigborhood
            return neighborhood  



def get_POC2_number_for_area(df2, NEIGHBORHOODS):
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

    # fiding the % of POC in each neighborhood
    for neighborhood, value in NEIGHBORHOODS.items():
        neighborhood_pop = value['population']
       
        if neighborhood in area_POC2_number:
            POC_pop = area_POC2_number[neighborhood]['population']
            print(POC_pop)
            area_POC2_number[neighborhood]['percentage'] = (POC_pop / neighborhood_pop) * 100
            

    return area_POC2_number
        

def get_average_grad_rate(df):
    neighborhood_avg_grad_rate = {}

    # iterates through public high school 
    for i in df.index:
        zipcode = df['ZIPCODE'][i]
        neighborhood = get_neighborhood_by_zipcode(zipcode)
        graduation_rate = df['Graduation_Rate'][i]
        # checks if we have seen this neighborhood before 
        if neighborhood in neighborhood_avg_grad_rate:
            curr_avg = neighborhood_avg_grad_rate[neighborhood]['rate']
            curr_size = neighborhood_avg_grad_rate[neighborhood]['size']
            # calculates average graduation rate for the neighborhood 
            neighborhood_avg_grad_rate[neighborhood] = {'rate': (curr_avg + graduation_rate) / (curr_size + 1),
                                                   'size': curr_size + 1}
        else:
            # sets the graduation rate for that neighborhood 
            neighborhood_avg_grad_rate[neighborhood] = {
                'rate': graduation_rate, 'size': 1}

    return neighborhood_avg_grad_rate


def extractOnlyNumbers(data): 
    nums = [] 
    for neighborhood, value in data.items(): 
        if 'rate' in value.keys(): 
            nums.append(value['rate'])
        elif 'percent' in value.keys(): 
            nums.append(value['percent'])
        elif 'house' in value.keys(): 
            nums.append(value['house'])

    return nums


def main():
    df = pd.read_excel(HIGHSCHOOL_DATASET, sheet_name='Public_Schools')

    neighborhood_avg_graduationrate = get_average_grad_rate(df)


    print(neighborhood_avg_graduationrate)


main()
