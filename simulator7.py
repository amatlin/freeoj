import numpy
import pandas

G_P = pandas.read_excel('Data/StaticData.xlsx', 'G->PS')
P_S = pandas.read_excel('Data/StaticData.xlsx', 'P->S')
S_M = pandas.read_excel('Data/StaticData.xlsx', 'S->M')

FCOJ = pandas.read_excel('Data/MomPop/Results/MomPop2015.xlsm', 'FCOJ')
grove = pandas.read_excel('Data/MomPop/Results/MomPop2015.xlsm', 'grove')

sales_index = FCOJ[FCOJ['Sales'] == 'Sales(tons) (by region and month)'].index.tolist()[0]
demand = FCOJ.iloc[sales_index+1:sales_index+10, 2:15]



regions = ['NE','MA','SE','MW','DS','NW','SW']
months = ['Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']

groves = ['FLA','CAL','TEX','ARZ','BRA','SPA']
processing_centers = ['P07']
storage_locations = ['S14','S61']
transportation_methods = ['carrier']



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
    grove_purchase_cost = grove_USprices[grove, month]

    return grove_purchase_cost
    
def get_processing_cost():
    if (product == 'POJ'):
        processing_cost = 2000
    elif (product == 'FCOJ'):
        processing_cost = 1000
    else:
        processing_cost = 0
    
    return processing_cost

def get_reconstitution_cost():
    if (product == 'ROJ'):
        reconstitution_cost = 650
    else:
        reconstitution_cost = 0
        
    return reconstitution_cost

def get_transportation_cost():
    if (grove != 'BRA' && grove != 'SPA'):
        t1_cost = G_P[processing_center, grove] * .22
        t2_cost = P_S[storage_location, processing_center] * .65
    else:
        t1_cost = 0
        t2_cost = -1
        #t2_cost = G_S[grove, storage_location] * .22
    
    t3_cost = S_M[region, storage_location]

    total_transportation_cost = t1_cost + t2_cost + t3_cost
    
    return total_transportation_cost
    
    
    



