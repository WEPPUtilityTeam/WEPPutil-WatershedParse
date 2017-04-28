


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
            
print t2w_dic
print w2t_dic['Hillslopes']