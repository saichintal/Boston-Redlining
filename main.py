import json
import pandas as pd

# Dataset file names and sheet names
HIGHSCHOOL_DATASET = 'Public_Highschool_Dataset.xlsx'
HIGHSCHOOL_DATASET_SHEET = 'Public_Schools'
POC2_DATASET = 'Boston_Social_Vulnerability.xlsx'
POC2_DATASET_SHEET = 'Climate_Ready_Boston_Social_Vul'
PROPERTY_DATASET = 'Property_values.xlsx'
PROPERTY_DATASET_SHEET = 'Sheet1'

# List of boston neighborhoods with zipcode, population, and redlining code
NEIGHBORHOODS = {
    'Allston': {'zipcode': ['02134'], 'population': 28821, 'code': 'B'},
    'Back Bay': {'zipcode': ['02116'], 'population': 21844, 'code': 'D'},
    'Beaconhill': {'zipcode': ['02108'], 'population': 9943, 'code': 'B'},
    'Brighton': {'zipcode': ['02135'], 'population': 45977, 'code': 'C'},
    'Chinatown': {'zipcode': ['02111'], 'population': 7510, 'code': 'D'},
    'Dorchester': {'zipcode': ['02121', '02122', '02124', '02125'], 
                   'population': 88333, 'code': 'C'},
    'East Boston': {'zipcode': ['02118'], 'population': 40508, 'code': 'B'},
    'Longwood': {'zipcode': ['02115'], 'population': 1754, 'code': 'D'},
    'Fenway': {'zipcode': ['02215'], 'population': 21174, 'code': 'D'},
    'Hyde Park': {'zipcode': ['02136'], 'population': 31845, 'code': 'C'},
    'Jamaica Plain': {'zipcode': ['02130'], 'population': 41262, 'code': 'A'},
    'Mattapan': {'zipcode': ['02126'], 'population': 34391, 'code': 'C'},
    'Mission Hill': {'zipcode': ['02120'], 'population': 13929, 'code': 'D'},
    'North End': {'zipcode': ['02113'], 'population': 10605, 'code': 'D'},
    'Roslindale': {'zipcode': ['02131'], 'population': 35945, 'code': 'C'},
    'Roxbury': {'zipcode': ['02119'], 'population': 63672, 'code': 'D'},
    'South Boston': {'zipcode': ['02127'], 'population': 35200, 'code': 'C'},
    'South End': {'zipcode': ['02118'], 'population': 33638, 'code': 'D'},
    'West End': {'zipcode': ['02114'], 'population': 5330, 'code': 'D'},
    'West Roxbury': {'zipcode': ['02132'], 'population': 30442, 'code': 'C'}
    }


def get_neighborhood_by_zipcode(zipcode):
    """
    Parameters: integer
    Returns: string
    Does: Checks which neighborhood the zipcode is in and returns neighborhood
    """
    for neighborhood, value in NEIGHBORHOODS.items():
        # converts list of string to list of ints
        results = list(map(int, value['zipcode']))
        # checks if zipcode is part of the neigborhood
        if zipcode in results:
            return neighborhood
    # zipcode is not in one of the neighborhoods above, none is returned
    return None


def get_avg_poverty_rate(df):
    """
    Parameters: panda dataframe
    Returns: dictionary of neighborhood to average poverty rate
    Does: Processes the dataframe by calculating the average poverty rate for
          each neighborhood in Boston.
    """
    neighborhood_poverty = {}

    # iterates through the list
    for i in df.index:
        neighborhood = df['Name'][i]
        num_of_low_income_people = df['Low_to_No'][i]
        # checks if we have seen this neighborhood before
        if neighborhood in neighborhood_poverty:
            curr_siz = neighborhood_poverty[neighborhood]['population']
            neighborhood_poverty[neighborhood] = {
                'population': curr_siz + num_of_low_income_people
            }
        else:
            # sets the poverty population for that neighborhood
            neighborhood_poverty[neighborhood] = {
                'population': num_of_low_income_people}

    # fiding the % of poverty in each neighborhood
    for neighborhood, value in NEIGHBORHOODS.items():
        neighborhood_pop = value['population']
        if neighborhood in neighborhood_poverty:
            pov_pop = neighborhood_poverty[neighborhood]['population']
            # compares the poverty population to the total population 
            neighborhood_poverty[neighborhood]['rate'] = (
                pov_pop / neighborhood_pop) * 100
            redlining_code = NEIGHBORHOODS[neighborhood]['code']
            neighborhood_poverty[neighborhood]['code'] = redlining_code

    return neighborhood_poverty


def update_neighborhood_map(neighborhood_map, neighborhood, value):
    """
    Parameters: dictionary of neighborhood to number
    Returns: dictionary of neighborhood to number
    Does: Processes the dataframe by calculating the average
          high school graduation rate for each neighborhood in Boston.
    """
    # checks if we have seen this neighborhood before
    if neighborhood in neighborhood_map:
        curr_avg = neighborhood_map[neighborhood]['rate']
        curr_size = neighborhood_map[neighborhood]['size']
        # calculates average value for the neighborhood
        neighborhood_map[neighborhood] = {
            'rate': ((curr_avg * curr_size) + value) / (curr_size + 1),
            'size': curr_size + 1, 'code': NEIGHBORHOODS[neighborhood]['code']
        }
    else:
        # sets the value for that neighborhood
        neighborhood_map[neighborhood] = {
            'rate': value, 
            'size': 1,
            'code': NEIGHBORHOODS[neighborhood]['code']
        }

    return neighborhood_map


def get_average_grad_rate(df):
    """
    Parameters: panda dataframe
    Returns: dictionary of neighborhood to average high school grad rate
    Does: Processes the dataframe by calculating the average 
          high school graduation rate for each neighborhood in Boston.
    """
    neighborhood_avg_grad_rate = {}

    # iterates through public high school
    for i in df.index:
        zipcode = df['ZIPCODE'][i]
        graduation_rate = df['Graduation_Rate'][i]

        neighborhood = get_neighborhood_by_zipcode(zipcode)
        # checks if neighborhood is one of the neighborhoods we are examining
        if neighborhood == None:
            continue

        # updates the dictionary with the new graduation rate
        neighborhood_avg_grad_rate = update_neighborhood_map(
                                        neighborhood_avg_grad_rate,
                                        neighborhood, graduation_rate)

    return neighborhood_avg_grad_rate


def get_average_property_val(df):

    """
    Parameters: panda dataframe
    Returns: dictionary of neighborhood to average property value
    Does: Processes the dataframe by calculating the average property value
          for each neighborhood in Boston.
    """
    neighborhood_avg_property_val = {}

    # iterates through properties
    for i in df.index:
        zipcode = df['ZIPCODE'][i]
        property_value = df['AV_TOTAL'][i]

        neighborhood = get_neighborhood_by_zipcode(zipcode)
        # checks if neighborhood is one of the neighborhoods we are examining
        if neighborhood == None:
            continue

        # updates the dictionary with the new property value  
        neighborhood_avg_property_val = update_neighborhood_map(
            neighborhood_avg_property_val, neighborhood, property_value)

    return neighborhood_avg_property_val


def get_avg_value_for_each_code(data):
    """
    Parameters: dictionary of neighborhood to average number and code 
    Returns: dictionary of code to average value
    Does: Processes the given dicitonary by calculating the average value
          for each code. 
    """
    avg_code_value = {'A': {'avg': 0, 'size': 0}, 'B': {'avg': 0, 'size': 0},
                      'C': {'avg': 0, 'size': 0}, 'D': {'avg': 0, 'size': 0}}

    # iterates thorugh each neighborhood
    for neighborhood, value in data.items():
        code = value['code']
        rate = value['rate']
        curr_avg = avg_code_value[code]['avg']
        curr_size = avg_code_value[code]['size']
        # calculates the current running average and then the new average
        avg_code_value[code]['avg'] = (
            (curr_avg * curr_size) + rate) / (curr_size + 1)
        # increments the running size by 1
        avg_code_value[code]['size'] = avg_code_value[code]['size'] + 1

    return avg_code_value


def main():
    # processes high school graduation data
    high_school_data = pd.read_excel(
        HIGHSCHOOL_DATASET, sheet_name=HIGHSCHOOL_DATASET_SHEET)
    # calculates avgerage graduation rate for each neighborhood 
    neighborhood_avg_graduation_rate = get_average_grad_rate(high_school_data)
    # calculates avgerage graduation rate for each redlining code  
    avg_graduation_for_code = get_avg_value_for_each_code(
        neighborhood_avg_graduation_rate)
    print(avg_graduation_for_code)

    # processes low income/poverty data
    poverty_data = pd.read_excel(POC2_DATASET, sheet_name=POC2_DATASET_SHEET)
    # calculates avgerage low income/poverty value for each neighborhood 
    neighborhood_avg_poverty_rate = get_avg_poverty_rate(poverty_data)
     # calculates avgerage low income/poverty value for each redlining code     
    avg_poverty_for_code = get_avg_value_for_each_code(
        neighborhood_avg_poverty_rate)
    print(avg_poverty_for_code)

    # processes property value data
    property_data = pd.read_excel(
        PROPERTY_DATASET, sheet_name=PROPERTY_DATASET_SHEET)
    # calculates avgerage property value for each neighborhood 
    neighborhood_avg_property_value = get_average_property_val(property_data)
    # calculates avgerage property value for each redlining code     
    avg_property_value_for_code = get_avg_value_for_each_code(
        neighborhood_avg_property_value)
    print(avg_property_value_for_code)


main()
