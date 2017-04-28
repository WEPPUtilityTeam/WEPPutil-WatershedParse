



slope_file = "hill_22.slp" #the list of slope files ('H001_slp.txt'...)

fout = "hill_22_mod.slp"
file_list = []

ofe_split_list = [.06,.55,.39][::-1] #input from CatchmentParse.py; needs to be reversed, .slp files read from top of hill to bottom


with open(slope_file, "rb") as f:
    o = open(fout, 'w')
    
    file = [x.strip() for x in f.readlines()] 
    ftype = file[0]
    num = file[1]
    aspect, width = [float(i) for i in file[2].split(' ')]
    ofes = int(file[3].split(' ')[0])
    length = float(file[3].split(' ')[1])
    
    ofe_list = []
    segment = file[4].split('  ')
    for i in segment:
        a,b = i.split(', ')
        ofe_list.append((float(a),float(b)))
    
    
    
    
    o.write('{}\n'.format(ftype))
    o.write('{}\n'.format(len(ofe_split_list)))
    o.write('{} {}\n'.format(aspect, width))
    
    
    print ftype 
    print len(ofe_split_list)
    print "{} {}".format(aspect, width)
    
    seg_not = 0
    for ofe_split in ofe_split_list:
        uzofe_list = zip(*ofe_list)
        seg = sum(i < ofe_split for i in zip(*ofe_list)[0])
        ofe_length = ofe_split*length
        
        zip(*ofe_list)[0][seg_not:seg+seg_not]
        zip(*ofe_list)[1][seg_not:seg+seg_not]
        mi = min(uzofe_list[0][seg_not:seg+seg_not])
        ma = max(uzofe_list[0][seg_not:seg+seg_not])
        
        
        uzofe_list[1][seg_not:seg+seg_not]
        #print "{}   {}   length {}".format(ofe_split, seg,ofe_split*length)
        
        #print "{} {} {}".format(seg_not,seg+seg_not,zip(*ofe_list)[0][seg_not:seg+seg_not])
        #print "{} {} {}".format(seg_not,seg+seg_not,zip(*ofe_list)[1][seg_not:seg+seg_not])
        percent_list = []
        for i in uzofe_list[0][seg_not:seg+seg_not]:
            percent_list.append((i-mi)/(ma-mi))
        
        pairs = zip(percent_list,zip(*ofe_list)[1][seg_not:seg+seg_not])
        seg_not = seg
        
        o.write('{} {}\n'.format(seg, ofe_length))
        
        print "{} {}".format(seg, ofe_length)
        ofe_str = ''
        for p in pairs:
            ofe_str+="{}, {} ".format(round(p[0],2),round(p[1],2))
        o.write('{}\n'.format(ofe_str))
        print ofe_str
        
    o.close

    