import numpy
import pandas

# read excel spreasheets using pandas
# -------------------------------------------------------------------------- #

G_P = pandas.read_excel('Data/StaticData.xlsx', 'G->PS')
P_S = pandas.read_excel('Data/StaticData.xlsx', 'P->S')
S_M = pandas.read_excel('Data/StaticData.xlsx', 'S->M')
FCOJ = pandas.read_excel('Data/MomPop/Results/MomPop2015.xlsm', 'FCOJ')
grove = pandas.read_excel('Data/MomPop/Results/MomPop2015.xlsm', 'grove')

# -------------------------------------------------------------------------- #




# pull specific tables into pandas and set indices/columns
# -------------------------------------------------------------------------- #

# Sales(tons) (by region and month)
index = FCOJ[FCOJ['Sales'] == 'Sales(tons) (by region and month)'].index.tolist()[0]
demand = FCOJ.iloc[index+1:index+10, 2:15]

# US$ Prices of oranges at the Spot Market($/lb) ORA
index = grove[grove['Grove'] == 'US$ Prices of oranges at the Spot Market($/lb) ORA'].index.tolist()[0]
grove_USprices = grove.iloc[index+1:index+8, 1:14]
grove_USprices.set_index(grove_USprices['Grove'], inplace=True)
grove_USprices.columns = grove_USprices.iloc[0]
grove_USprices.drop('Grove:Month', inplace=True)
grove_USprices.drop('Grove:Month', inplace=True, axis=1)

# G->PS
G_P.set_index(G_P['To:Fr'], inplace=True)
G_P.drop('To:Fr', inplace=True, axis=1)

# P->S
P_S.set_index(P_S['To:Fr'], inplace=True)
P_S.drop('To:Fr', inplace=True, axis=1)

# S->M
S_M.set_index(S_M['To:Fr'], inplace=True)
S_M.drop('To:Fr', inplace=True, axis=1)

# -------------------------------------------------------------------------- #




# vectors
# -------------------------------------------------------------------------- #
regions = ['NE','MA','SE','MW','DS','NW','SW']
months = ['Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']

groves = ['FLA','CAL','TEX','ARZ','BRA','SPA']
processing_centers = ['P07']
storage_locations = ['S14','S61']
transportation_methods = ['carrier']

# -------------------------------------------------------------------------- #




# functions
# -------------------------------------------------------------------------- #

def find_cost_matrix(product):
    cost_matrix = numpy.zeros((7, 12))
    for r in regions:
        for m in months:
            all_path_costs = find_all_path_costs(r, m)
            min_path_cost = min(all_path_costs)
            cost_matrix[r][m] = min_path_cost
    return cost_matrix

def find_all_path_costs(product, region, month):
    num_paths = len(groves)*len(processing_centers)*len(storage_locations)*len(transportation_methods)
    all_path_costs_matrix = numpy.zeros(num_paths)
    i = 0
    for g in groves:
        for p in processing_centers:
            #for option in every product changing # product_changes = ['change in FCOJ', 'dont change']
            for s in storage_locations:
                for t in transportation_methods:
                    cost = find_path_cost(product, region, month, g, p, s, t)
                    all_path_costs_matrix[i] = cost
                    i = i+1
    return all_path_costs_matrix
      
def find_path_cost(product, region, month, grove, processing_center, storage_location, transportation_method):
    grove_purchase_cost = get_grove_purchase_cost(grove, month)
    processing_cost = get_processing_cost(product)
    reconstitution_cost = get_reconstitution_cost(product)
    transportation_cost = get_transportation_cost(region, grove, processing_center, storage_location)
    
    total_cost = grove_purchase_cost + processing_cost + reconstitution_cost + transportation_cost
    
    return total_cost
      
def get_grove_purchase_cost(grove, month):
    grove_purchase_cost = grove_USprices.loc[grove,month]

    return grove_purchase_cost
    
def get_processing_cost(product):
    if (product == 'POJ'):
        processing_cost = 2000
    elif (product == 'FCOJ'):
        processing_cost = 1000
    else:
        processing_cost = 0
    
    return processing_cost

def get_reconstitution_cost(product):
    if (product == 'ROJ'):
        reconstitution_cost = 650
    else:
        reconstitution_cost = 0
        
    return reconstitution_cost

def get_transportation_cost(region, grove, processing_center, storage_location):
    if ((grove != 'BRA') & (grove != 'SPA')):
        t1_cost = G_P.loc[processing_center, grove] * .22
        t2_cost = P_S.loc[storage_location, processing_center] * .65
    else:
        t1_cost = 0
        t2_cost = -1
        #t2_cost = G_S[grove, storage_location] * .22
    
    t3_cost = S_M.loc[region, storage_location]

    total_transportation_cost = t1_cost + t2_cost + t3_cost
    
    return total_transportation_cost
    
# -------------------------------------------------------------------------- #
    



# test code
# -------------------------------------------------------------------------- #

#test = get_transportation_cost('NE', 'FLA', 'P07', 'S61')
#print( test )

# -------------------------------------------------------------------------- #




# action items / new thoughts
# -------------------------------------------------------------------------- #

# was testing get_transportation_cost function and just realized we can't 
# iterate through regions, have to iterate through every single market

# action item: change region to market in most places in code I think

# actiomn item: test all functions

# also found out groves DO have production limits (BRA/SPA don't)

# action item: add table for price just like demand
# (for now still just estimating as last years 2015 data)

# action item: create giant list of profit from every path, sort list

# action item: while (storage/processing facilities not full, continue down list):
    # if grove out of product, eliminate those choices from list
    # when demand filled, eliminate paths to that market from list
    # when 1 storage filled, elimainate all paths through that storage
    # so on

# -------------------------------------------------------------------------- #





