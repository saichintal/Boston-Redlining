import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
from pandas import ExcelWriter
from pandas import ExcelFile


HIGHSCHOOL_DATASET = 'Public_Highschool_Dataset.xlsx'
POC2_DATASET = 'Boston_Social_Vulnerability.xlsx'
PROPERTY_DATASET = 'Property_values.xlsx'

CODE_TRANSLATOR = {'D': "Dangerous",
                   'C': 'Definitely Declining',
                   'B': 'Still Desireable',
                   'A': 'Best'}

NEIGHBORHOODS = {'Allston': {'zipcode': ['02134'], 'population': 28821, 'code': 'B'},
                'Back Bay': {'zipcode': ['02116'], 'population': 21844,'code': 'D'},
                'Beaconhill': {'zipcode': ['02108'], 'population': 9943,'code': 'B'},
                'Brighton': {'zipcode': ['02135'], 'population': 45977,'code': 'C'},
                'Chinatown':{'zipcode': ['02111'], 'population': 7510,'code': 'D'},
                'Dorchester':{'zipcode': ['02121', '02122', '02124', '02125'], 'population': 88333,'code': 'C'},
                'East Boston': {'zipcode': ['02118'], 'population': 40508,'code': 'B'},
                'Longwood': {'zipcode': ['02115'], 'population': 1754,'code': 'D'},
                'Fenway': {'zipcode': ['02215'], 'population': 21174,'code': 'D'},
                'Hyde Park': {'zipcode': ['02136'], 'population': 31845,'code': 'C'},
                'Jamaica Plain': {'zipcode': ['02130'], 'population': 41262,'code': 'A'},
                'Mattapan': {'zipcode': ['02126'], 'population': 34391,'code': 'C'},
                'Mission Hill': {'zipcode': ['02120'], 'population': 13929,'code': 'D'},
                'North End': {'zipcode': ['02113'], 'population': 10605,'code': 'D'},
                'Roslindale':{'zipcode': ['02131'], 'population': 35945,'code': 'C'},
                'Roxbury': {'zipcode': ['02119'], 'population': 63672,'code': 'D'},
                'South Boston': {'zipcode': ['02127'], 'population': 35200,'code': 'C'},
                'South End': {'zipcode': ['02118'], 'population': 33638,'code': 'D'},
                'West End': {'zipcode': ['02114'], 'population': 5330,'code': 'D'},
                'West Roxbury': {'zipcode': ['02132'], 'population': 30442,'code': 'C'}
                }


def get_neighborhood_by_zipcode(zipcode): 
    for neighborhood, value in NEIGHBORHOODS.items():
        results = list(map(int, value['zipcode'])) # converts list of string to list of ints 
        if zipcode in results: # checks if zipcode is part of the neigborhood
            return neighborhood  
    return None



def get_avg_poverty_rate(df):
    area_poverty_number = {}

    #iterates through the list
    for i in df.index:
        area = df['Name'][i]
        num_of_low_income_people = df['Low_to_No'][i]
        # checks if we have seen this area before
        if area in area_poverty_number:
            curr_siz = area_poverty_number[area]['population']
            area_poverty_number[area] = {'population': curr_siz + num_of_low_income_people}
        else:
            #sets the poverty population for that area
            area_poverty_number[area] = {'population': num_of_low_income_people}

    # fiding the % of poverty in each neighborhood
    for neighborhood, value in NEIGHBORHOODS.items():
        neighborhood_pop = value['population']
        if neighborhood in area_poverty_number:
            pov_pop = area_poverty_number[neighborhood]['population']
            area_poverty_number[neighborhood]['rate'] = (pov_pop / neighborhood_pop) * 100
            area_poverty_number[neighborhood]['code'] = NEIGHBORHOODS[neighborhood]['code']


            

    return area_poverty_number
        

def get_average_grad_rate(df):
    neighborhood_avg_grad_rate = {}

    # iterates through public high school 
    for i in df.index:
        zipcode = df['ZIPCODE'][i]
        neighborhood = get_neighborhood_by_zipcode(zipcode)
        # checks if neighborhood is one of the neighborhoods we are examining 
        if neighborhood == None:
            continue
        
        graduation_rate = df['Graduation_Rate'][i]
        # checks if we have seen this neighborhood before 
        if neighborhood in neighborhood_avg_grad_rate:
            curr_avg = neighborhood_avg_grad_rate[neighborhood]['rate']
            curr_size = neighborhood_avg_grad_rate[neighborhood]['size']
            # calculates average graduation rate for the neighborhood 
            neighborhood_avg_grad_rate[neighborhood] = {'rate': ((curr_avg * curr_size) + graduation_rate) / (curr_size + 1),
                                                   'size': curr_size + 1, 'code': NEIGHBORHOODS[neighborhood]['code']}
        else:
            # sets the graduation rate for that neighborhood 
            neighborhood_avg_grad_rate[neighborhood] = {
                'rate': graduation_rate, 'size': 1, 'code': NEIGHBORHOODS[neighborhood]['code']}
        
    return neighborhood_avg_grad_rate


def get_average_property_val(df):
    neighborhood_avg_property_val = {}

    # iterates through properties 
    for i in df.index:
        zipcode = df['ZIPCODE'][i]
        neighborhood = get_neighborhood_by_zipcode(zipcode)
        # checks if neighborhood is one of the neighborhoods we are examining 
        if neighborhood == None:
            continue
        
        property_value = df['AV_TOTAL'][i]
        # checks if we have seen this neighborhood before 
        if neighborhood in neighborhood_avg_property_val:
            curr_avg = neighborhood_avg_property_val[neighborhood]['rate']
            curr_size = neighborhood_avg_property_val[neighborhood]['size']
            # calculates average property value for the neighborhood 
            neighborhood_avg_property_val[neighborhood] = {'rate': ((curr_avg * curr_size) + property_value) / (curr_size + 1),
                                                   'size': curr_size + 1, 'code': NEIGHBORHOODS[neighborhood]['code']}
        else:
            # sets the property value for that neighborhood 
            neighborhood_avg_property_val[neighborhood] = {
                'rate': property_value, 'size': 1, 'code': NEIGHBORHOODS[neighborhood]['code']}
        
    return neighborhood_avg_property_val

def get_avg_value_for_each_code(data): 
    avg_code_value = {'A' : {'avg' : 0, 'size': 0}, 'B' : {'avg' : 0, 'size': 0}, 
                      'C' : {'avg' : 0, 'size': 0}, 'D' : {'avg' : 0, 'size': 0}}
    
    # iterates thorugh each neighborhood 
    for neighborhood, value in data.items(): 
        code = value['code']
        rate = value['rate']
        curr_avg = avg_code_value[code]['avg'] 
        curr_size = avg_code_value[code]['size'] 
        # calculates the current running average and then the new average 
        avg_code_value[code]['avg'] =  ((curr_avg *  curr_size) + rate) / (curr_size + 1)
        # increments the running size by 1 
        avg_code_value[code]['size'] =  avg_code_value[code]['size'] + 1 
    
    return avg_code_value

def ANOVA( averages_by_neighborhood):
    '''
    params: averages by neighborhood and by code as Dictionaries
    returns: 
    DOES: determination of statistical analysis through ANOVA method
        this method assumes that the rates are distributed normally and
        that each group has the same standard deviation.
        These may not be reasonable assumptions but they were ones that allowed
        us to use the statsitical methods we knew how to implement.
    '''
    
    A = [ ]
    B = [ ]
    C = [ ]
    D = [ ]

    
    for key, value in averages_by_neighborhood.items():
        the_list = averages_by_neighborhood[key]["code"]
        try:
            additions = averages_by_neighborhood[key]["size"]
        except:
            additions = 1
        if the_list == "A":
            while additions > 0:
                A.append(averages_by_neighborhood[key]["rate"])
                additions -= 1
        elif the_list == "B":
            while additions > 0:
                B.append(averages_by_neighborhood[key]["rate"])
                additions -= 1
        elif the_list == "C":
            while additions > 0:
                C.append(averages_by_neighborhood[key]["rate"])
                additions -= 1
        elif the_list == "D":
            while additions > 0:
                D.append(averages_by_neighborhood[key]["rate"])
                additions -= 1

    #prints the lists so that they can be visually checked            
    #print("A:",A,'\n',"B:",B,'\n',"C:",C,'\n',"D:",D)

    #calculates N the total number of observations in the data
    n_population = len(A) + len(B) + len(C) + len(D)
    print("The n value for this test is: ", n_population)

    #used the stats package to run an f one way test also known as anova
    anova = stats.f_oneway(A,B,C,D)
    
    #anova returns an object with a handful of attributes one of which is the
    #p value we check the p value as a means of making conclusions 
    if anova.pvalue <= 0.01:
        print ("We are able to reject the null hypothesis that all four",
               "groups have the same mean at the 99% confidence interval",
               "The pvalue for this test was:", round(anova.pvalue,4) )
    elif anova.pvalue <=0.05:
        print ("We are able to reject the null hypothesis that all four",
               "groups have the same mean at the 99% confidence interval",
               "The pvalue for this test was:", round(anova.pvalue,4) )
    else:
        print ("We are unable to reject the null hypothesis that all four",
               "groups have the same true mean at the 95% confidence interval",
               "The pvalue for this test was:", round(anova.pvalue,4))
        

    return

    
    
def averages_bar_chart( neighborhood_averages, y_value_title, chart_title):
    '''
    params: neighborhood_averages as dictionary of dictionaries,
            y_value_title and chart_title as strings
    return: none
    Does: Graphs the averages by code for the datasets analyzed. 
    '''
    #creates lists (and a tupple) used for graphs
    codes = [ ]
    averages = [ ]
    colors = ("Green","Blue","Yellow","Red")

    #separates dictionary of dictionary into necessary components
    for key, value in neighborhood_averages.items():
        codes.append(key)
        averages.append(neighborhood_averages[key]["avg"])

    #builds the bar chart
    x_axis = np.arange(len(codes))
    plt.bar(x_axis, averages, align ='center', alpha = 0.5, color = colors)
    plt.xticks(x_axis, codes)
    plt.ylabel('Average'+ y_value_title + 'by code')
    plt.title(chart_title)

    #displays bar chart
    plt.show()



def neighborhood_bar_chart(neighborhood_data, y_value_title, chart_title):
    '''
    params: neighborhood_data as dictionary of dictionaries,
            y_value_title and chart_title as strings
    return: none
    Does: Graphs the data by neighborhood for the datasets analyzed. 
    '''
    neighborhoods = [ ]
    rates = [ ]
    #separates the dictionary into two lists of neighborhoods and their "rates"
    for key, value in neighborhood_data.items():
        neighborhoods.append(key)
        rates.append(neighborhood_data[key]["rate"])

    #sorts the lists from largest to smallest for a more visually appealing graph
    rates, neighborhoods = sort_lists (rates,neighborhoods )     

    x_axis = np.arange(len(neighborhoods))
    plt.bar(x_axis, rates, align ='center', alpha = 0.5)
    plt.xticks(x_axis, neighborhoods, rotation = 45)
    plt.ylabel( y_value_title + ' by Neighborhood')
    plt.title(chart_title)

    plt.show()

    

def sort_lists( rates, neighborhoods):
    '''
    Params: list of numbers, neighborhoods as lists
    Returns list of numbers, neighborhoods as a tupple of lists
    Does: Sorts the rates from largest to smallest to make a more visually
    appealing graph. Used only in neighborhood_bar_chart. It is pretty
    inefficient but this is my (Benjamin Novak's) first programming course
    with more time we would improve this function to take less time
    '''
    ordered = True
    while ordered:
        for i in range( len(rates) + 1 ):
            if i == 0:
                next
            elif i == len(rates):
                return rates, neighborhoods
            elif rates[i] > rates[i-1]:
                rates[i], rates[i-1] = rates[i-1], rates[i]
                neighborhoods[i], neighborhoods[i-1] = neighborhoods[i-1], neighborhoods[i]
                break
    return


def main():
    df = pd.read_excel(HIGHSCHOOL_DATASET, sheet_name='Public_Schools')

    neighborhood_avg_graduation_rate = get_average_grad_rate(df)
    #print(neighborhood_avg_graduation_rate, '\n\n\n')

    avg_graduation_for_code = get_avg_value_for_each_code(neighborhood_avg_graduation_rate)
    #print(avg_graduation_for_code)
    
    df2 = pd.read_excel(POC2_DATASET, sheet_name='Climate_Ready_Boston_Social_Vul')
    neighborhood_avg_poverty_rate = get_avg_poverty_rate(df2)
    #print(neighborhood_avg_poverty_rate,"\n\n\n") 

    avg_poverty_for_code = get_avg_value_for_each_code(neighborhood_avg_poverty_rate)
    #print(avg_poverty_for_code)

    df = pd.read_excel(PROPERTY_DATASET, sheet_name='Sheet1')
    
    neighborhood_avg_property_value = get_average_property_val(df)
    #print(neighborhood_avg_property_value,"DONE")
    
    avg_property_value_for_code = get_avg_value_for_each_code(neighborhood_avg_property_value)
    print(avg_property_value_for_code)
    
    #statistical analysis

    #Graduation Rates
    print("\n Results of ANOVA for graduation rates:\n")
    ANOVA( neighborhood_avg_graduation_rate )

    #Poverty Rates
    print("\n Results of ANOVA for poverty rates: \n")
    ANOVA( neighborhood_avg_poverty_rate )

    #Property Values
    print("\n Results of ANOVA for property values: \n")
    ANOVA( neighborhood_avg_property_value)

    
    #visualizations
    
    #average graduation rate by code
    averages_bar_chart(avg_graduation_for_code, "graduation rate",
                       "Graduation Rate by Code")
    #average poverty rate by code
    averages_bar_chart(avg_poverty_for_code,"poverty rate",
                      "Poverty Rate by Code")
    #average property values by code
    averages_bar_chart( avg_property_value_for_code,"property value",
                       "Average Property Value by Code")
    
    #graduation rates by neighborhood
    neighborhood_bar_chart( neighborhood_avg_graduation_rate, "Graduation Rate",
                           'Graduation Rates by Neighborhood')
    #poverty Rates by Neighborhood
    neighborhood_bar_chart( neighborhood_avg_poverty_rate, "Poverty Rate",
                            'Poverty Rates by Neighborhood')
    #Average Property Values by Neighborhood
    neighborhood_bar_chart(neighborhood_avg_property_value, "Average Property",
                           'Average Property Values by Neighborhood')
    
main()
