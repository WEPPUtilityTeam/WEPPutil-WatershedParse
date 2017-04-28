import csv
from math import trunc
from itertools import groupby


'''
A script to identify the proper locations for splitting a WEPP hillslope file into multiple OFEs based
on topographic position index and burn severity class.



input lines in the form [id][tpi][barc]; 
id is all chars except for the last two, 
tpi is the second to last char, 
barc is the last char

ex.
OID    VALUE    COUNT
-1    2214    2
-1    2223    5
-1    2224    24
-1    2332    1
n/a   xxyz    c
     id|tpi|barc
'''

def find_majority(list):
    ''' Input in the form [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        Returns a summary of the majority burn severity class for each tpi value, 
        percent area of the burn class by tpi, and percent area of the tpi value
        
        Return: [(majority_bs,majority_area,total_tpi_area)...,total_hill_area ]
    '''
    summary_list = []
    hill_area = 0
    total_hill_area = sum([sum(i) for i in zip(*list)])
    for tpi in list:
        #find the majority bs for each tpi
        if sum(tpi) > 0:
            majority_bs = tpi.index(max(tpi))+1
            majority_area = max(tpi)
            total_area = sum(tpi)
            hill_area += total_area
            summary_list.append((majority_bs,majority_area,total_area))
        else:
            pass
    return summary_list, total_hill_area
    
def split_ofe(majority_list, total_hill_area):
    '''Returns a list of tuples for each tpi present as: 
    (burn severity class, pixels in majority bs class, 
    total pixels in tpi class, fraction of area on hillslope)
    '''
    ofe_list = []
    bs_list,bs_area_list,total_area_list = zip(*majority_list)
    grouped = ([list(j) for i, j in groupby(bs_list)])
    n = 0
    for bs in grouped:
        bs_area = sum(bs_area_list[n:len(bs)+n])
        total_area = sum(total_area_list[n:len(bs)+n])
        n+=len(bs)
        area_fraction = round(float(total_area)/total_hill_area,2)
        ofe_list.append((bs[0], bs_area, total_area, area_fraction))
    return ofe_list



def CatchmentParse(fin):
    #fin = "wil_TPI300_BARC_hist.csv"
    #fout = "wil_TPI300_BARC_hist_full.csv"
    fout = "test_out.csv"
    
    ofe_split_dic = {}
    
    with open(fin, 'rb') as filereader:
        hilldic = {} #{ID:[[],[],[],[]]}
        ofe_dic = {}
        f = csv.reader(filereader, delimiter=',')
        for row in f:
            try:
                value = row[1]
                count = int(row[2])
                bs = int(value[-1:])
                tpi = int(value[-2:-1])
                hid = int(value[:-2])
    
                if hid not in hilldic.keys():
                    #new hill hid
                    #                1        2          3        4          5        6          7
                    #                1,2,3,4
                    hilldic[hid] = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
                #find location in hilldic and replace default value
                #print "bs: %s   tpi: %s hid: %s count: %s"%(bs-1,tpi-1,hid, count)
                hilldic[hid][tpi-1][bs-1] = count
            except:
                #missing data, incorrect format..
                pass
        
        
        
        #o.write("ID,1,2,3,4,5,6,7\n")
        
        
        for id in hilldic.keys():
            maj = find_majority(hilldic[id])
            hilldic[id] = maj[0]
            total_hill_area = maj[1]
            ofe_tup = split_ofe(maj[0],maj[1])
            ofe_dic[id] = ofe_tup
            ofe_split_dic[id] = ofe_tup
            #print "Hillslope ID: %s   OFE Splits: %s" %(id,ofe_tup)
         
    return ofe_split_dic   
    