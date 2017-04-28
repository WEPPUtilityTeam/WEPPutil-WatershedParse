import CatchmentParse

'''
This script reads in a WEPP watershed file (*.prw) and transforms some elements based on other input data

'''


def get_idDic(fin):
    '''
    Input name of the 'topaz2wepp.txt' file as string
    Returns two dictionaries, topaz to wepp, and wepp to topaz
    '''
    fin = 'topaz2wepp.txt'
    t2w_dic = {'Hillslopes':{},'Channels':{}}
    w2t_dic = {'Hillslopes':{},'Channels':{}}
    c_switch = 'Hillslopes'
    with open(fin, "rb") as f:
        file = [x.strip() for x in f.readlines()]
        for line in file:
            if line.startswith('#'):
                if 'Channels' in line:
                    c_switch = 'Channels'
            else:
                topaz, wepp, area = line.split()
                t2w_dic[c_switch][topaz] = wepp
                w2t_dic[c_switch][wepp] = topaz
   
    return t2w_dic,w2t_dic
    


def SlopeParse(slist, split_list):
    l1,l2,l3 = slist
    file_list = []
    
    ofe_split_list = split_list[::-1] #input from CatchmentParse.py; needs to be reversed, .slp files read from top of hill to bottom


    
    
    aspect, width = [float(i) for i in l1.split(' ')]
    ofes = int(l2.split(' ')[0])
    length = float(l2.split(' ')[1])
    
    ofe_list = []
    segment = l3.split('  ')
    for i in segment:
        a,b = i.split(', ')
        ofe_list.append((float(a),float(b)))
    
    seg_not = 0
    
    output_str = ''
    for ofe_split in ofe_split_list:
        uzofe_list = zip(*ofe_list)
        seg = sum(i < ofe_split for i in zip(*ofe_list)[0])
        ofe_length = ofe_split*length
        
        zip(*ofe_list)[0][seg_not:seg+seg_not]
        zip(*ofe_list)[1][seg_not:seg+seg_not]
        mi = min(uzofe_list[0][seg_not:seg+seg_not])
        ma = max(uzofe_list[0][seg_not:seg+seg_not])
        uzofe_list[1][seg_not:seg+seg_not]
        percent_list = []
        try:
            for i in uzofe_list[0][seg_not:seg+seg_not]:
                percent_list.append((i-mi)/(ma-mi))
            
            pairs = zip(percent_list,zip(*ofe_list)[1][seg_not:seg+seg_not])
            seg_not = seg
            
            output_str += '{} {}\n'.format(seg, ofe_length)
            ofe_str = ''
            for p in pairs:
                ofe_str +="{}, {} ".format(round(p[0],4),round(p[1],4))
            output_str += '{}\n'.format(ofe_str)
        except:
            pass
        
    return "{} {}\n{}".format(aspect, width, output_str.rstrip('\n'))
    o.close








#Global vars



dir = ""
fin = "ww2.prw"
fout = "wo1.prw"


headder = []
version = 0
name = 0
comments = []
slp_list = []
bracket = 0
tag_list = "None"




#Dictionaries
channel_dic = {} #ID as channel id
hill_dic = {} #dynamically set id as File Landuse, Length, Profile, Climate, Soil, Management, RunOptions
soil_dic = {}
manage_dic = {}
bs_dic = {1:"unb",2:"low",3:"mod",4:"high"}

if __name__ == "__main__":
    
    t2w_dic,w2t_dic = get_idDic('topaz2wepp.txt')
    
    
    catchments_dic = CatchmentParse.CatchmentParse('wo1_tpibarc_hist.csv')
    
    
    
    with open(fin, "rb") as f:
        with open(fout, 'w') as o:
            file = [x.strip() for x in f.readlines()]
            
             
            for line in file:
                #bracket counter
                if "{" in line:
                    #increase bracket counter
                    bracket +=1
                if "}" in line:
                    #decrease bracket counter
                    bracket -=1
                
                
                '''
                1 - Number
                
                2 - HID
                
                    3 - File
                        3 - Landuse
                        3 - Length
                        
                        4 - Profile
                            5 - Data (slope)
                                5 - aspect, width
                                5 - segments, length
                                5 - fraction, slope .... repeat
                        4 - Climate, 
                            4 - File
                        4 - Soil
                            4 - Breaks
                            5 - default
                                5 - Distance
                                5 - File
                        4
                        3
                        4 - Management
                            4 - Breaks
                            5 - default
                                5 - Distance
                                5 - File
                        4
                        3
                        4 - RunOptions 
                            4 - Version
                            4 - SoilLossOutputType
                            4 - SoilLossOutputFile
                            4 - PlotFile
                            4 - SimulationYears
                            4 - SmallEventBypass
                        3
                        2 - Head, Direction, Angle, Base, Height
                        3 - Polygon
                    2
                    1
                    2 - HID
                    ....repeat
                
                
                '''
                
                
                #case logic for determining location in file:
                #sets tag tag_list as respective file tag
                if bracket == 1:
                    
                    if line.startswith("Comments"):
                        tag_list = ["Comments"]
                        
                    if line.startswith("Climate"):
                        tag_list = ["Climate"]
                    
                    if line.startswith("Channels"):
                        tag_list = ["Channels"]
                        
                    if line.startswith("Hillslopes"):
                        tag_list = ["Hillslopes"]
                        
                    if line.startswith("Network"):
                        tag_list = ["Network"]
                    
                    if line.startswith("RunOptions"):
                        tag_list = ["RunOptions"]
                
                    if line.startswith("#"):
                        #Line is a headder line
                        headder.append(line)
                
                
                if 'Comments' in tag_list and line.startswith('}'):
                    #last line of comments, insert new comment str
                    o.write("Soil and Management OFEs modified by WatershedParse.py\n")
                    print "Soil and Management OFEs modified by WatershedParse.py"
                
                
                
                
                if 'Hillslopes' in tag_list and bracket == 2:
                    #Beginning of a new hillslope set
                    try:
                        # add tag for hillslope number if new hillslope
                        int(line[1])
                        if len(tag_list) == 1:
                            tag_list.append(line.split(' ')[0]) # position 1
                        else:
                            
                            tag_list[1] = line.split(' ')[0] # position 1
                            
                        #reset hill_dic
                        hill_dic = {}
                    except:
                        pass
                
                if 'Hillslopes' in tag_list and len(tag_list) >= 2:
                    #in hillslope set with a set hill id     ===== hill_dic
                    
                    if line.startswith('RunOptions '):
                         tag_list.append('RunOptions') # position 2
                    if line.startswith('Length '):
                         tag_list.append('Length') # position 2
                    if line.startswith('Profile '):
                         tag_list.append('Profile') # position 2
                    if line.startswith('Climate '):
                         tag_list.append('Climate') # position 2     
                    if line.startswith('Soil '):
                         tag_list.append('Soil') # position 2          
                    if line.startswith('Management '):
                         tag_list.append('Management') # position 2     
                              
                    
                    if any(x in tag_list for x in ['File', 'Landuse', 'Length', 'Profile', 'Climate', 'Soil', 'Management', 'RunOptions']) and len(tag_list) and bracket == 3:
                        tag_list.pop()
                    
                    if 'Profile' in tag_list:
                        try:
                            int(line[0])
                            slp_list.append(line)
                            
                        except:
                            #skip non number lines
                            pass
                    
                        if len(slp_list) == 3:
                            
                            ofe_list = []
                            burn_list = []
                            id = w2t_dic['Hillslopes'][str(tag_list[1].strip('H'))]
                            for s in catchments_dic[int(id)]:
                                ofe_list.append(s[3])
                                burn_list.append(s[0])
                            
                            ofe_list = zip(ofe_list[::-1],burn_list[::-1]) #reverse order, top to bottom
                            
                            
                            #print SlopeParse(slp_list, ofe_list)
                            slp_list = []
                    
                    
                    if 'Soil' in tag_list:
                        
                        
                        if ' = ' in line:
                            var, val = line.strip(' {').split(' = ')
                            soil_dic[var] = val.strip('"')
                        if 'File' in soil_dic.keys():
                            soil_str = ''
                            length = float(soil_dic['Distance'])
                            name = soil_dic['File'].split('.sol')[0].split('\\')[1]
                            
                            file_name = soil_dic['File'].split('.sol')[0]
                            #at the end of soil, procede with modifications
                            
                                                        #br  name
                            soil_str = "Soil {{\nBreaks = {}\n".format(len(ofe_list))
                            for o_list in ofe_list:
                                ofe_soil_name = "{}_{}".format(name,bs_dic[o_list[1]])
                                dist_frac = length*o_list[0]
                                ofe_soil_file = "{}_{}.sol".format(file_name,bs_dic[o_list[1]])
                                
                                soil_str += "{} {{\nDistance = {}\nFile = \"{}\" \n}}\n".format(ofe_soil_name, dist_frac,ofe_soil_file)
                            soil_str += "\n"
                            print soil_str[:-1]
                            o.write(soil_str[:-1])
                            soil_dic = {} #reset dic for next hill
                            '''
                            
                            soil_name {
                            Distance = fraction_dist
                            File = "file_name.sol"
                            }
                            
                      '''                     
                            
                            
                    
                    if 'Management' in tag_list:  
                        if ' = ' in line:
                            var, val = line.strip(' {').split(' = ')
                            manage_dic[var] = val.strip('"')
                        if 'File' in manage_dic.keys():
                            manage_str = ''
                            length = float(manage_dic['Distance'])
                            name = manage_dic['File'].split('.rot')[0]
                            file_name = manage_dic['File'].split('.rot')[0]
                            #at the end of soil, procede with modifications
                            
                                                        #br  name
                            manage_str = "Management {{\nBreaks = {}\n".format(len(ofe_list))
                            for o_list in ofe_list:
                                ofe_man_name = "{}_{}".format(name,bs_dic[o_list[1]])
                                dist_frac = length*o_list[0]
                                ofe_man_file = "{}_{}.rot".format(file_name,bs_dic[o_list[1]])
                                
                                manage_str += "{} {{\nDistance = {}\nFile = \"{}\" \n}}\n".format(ofe_man_name, dist_frac,ofe_man_file)
                            manage_str += "\n"
                            print manage_str[:-1]
                            o.write(manage_str[:-1])
                            manage_dic = {}
                        
                        
                        
                    if ' = ' in line and len(tag_list)>=3:
                        var, val = line.strip(' {').split(' = ')
                        
                        if tag_list[2] not in hill_dic.keys():
                            hill_dic[tag_list[2]] = {}
                        if type(hill_dic[tag_list[2]]) == dict:
                            hill_dic[tag_list[2]][var] = val.strip('"')
                        else:
                            hill_dic[tag_list[2]] = {var:val.strip('"')}
                
                #File Landuse, Length, Profile, Climate, Soil, Management, RunOptions
                
                
                
                
                
                
                if set(['Soil','Management']).isdisjoint(tag_list):
                    #print "{: <60}    {}   {}".format(line, bracket, tag_list)
                    print "{}".format(line)
                    o.write("{}\n".format(line))
                    
            
       