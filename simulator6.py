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


def find_cost_matrix():
    cost_matrix = numpy.zeros((7, 12))
    for r in regions:
        for m in months:
            all_path_costs = find_all_path_costs(r, m)
            min_path_cost = min(all_path_costs)
            cost_matrix[r][m] = min_path_cost
    return cost_matrix

def find_all_path_costs(region, month):
    num_paths = len(groves)*len(processing_centers)*len(storage_locations)*len(transportation_methods)
    all_path_costs_matrix = numpy.zeros(num_paths)
    i = 0
    for g in groves:
        for p in processing_centers:
            for s in storage_locations:
                for t in transportation_methods:
                    cost = find_path_cost(region, month, g, p, s, t)
                    all_path_costs_matrix[i] = cost
                    i = i+1
    return all_path_costs_matrix
      
def find_path_cost(region, month, grove, processing_center, storage_location, transportation_method):
    return -1
    

    
    



