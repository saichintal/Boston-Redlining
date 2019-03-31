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
