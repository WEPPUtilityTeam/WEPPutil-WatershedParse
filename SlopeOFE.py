


slfilelist = "slope_file_list" #the list of slope files ('H001_slp.txt'...)

file_list = []

with open(slfilelist, "rb") as filereader:
    f = reader(filereader)
    for row in f:
        f[1:].split('_')[0]
        file_list.append((f,row))


for fid,file in file_list:
    with open(file, "rb") as filereader:
        f = reader(filereader)
        for row in f:
        
'''


#!/usr/bin/perl

#  This program takes a WEPP hillslope files with multiple break points with one OFE and converts it
#  to a WEPP hillslope file with multiple OFEs defined by the break point of the single OFE file.
#  Erin Brooks 3/3/06

#  The program looks for all files ending in "_slp.txt" and converts them to "*.out" files
#  Caution the program deletes all files ending in "*.out" before it starts

print `rm slope_file_list`;
print `rm *.out`;
print `ls *_slp.txt >slope_file_list`;

open (LIST, "<slope_file_list") || "Can't open file\n";
while (<LIST>) {
    chop($_);
    ($slope_file) = split;
    ($junk) = split(/_slp.txt/, $slope_file);
    ($slope_number) = substr($junk, 1);
    print "$junk\n";

open (SLOPE, "<$slope_file") || "Can't open file\n";
$version=<SLOPE>;
$p1=<SLOPE>;
$p2=<SLOPE>;
$p3=<SLOPE>;
$p4=<SLOPE>;
$constant=<SLOPE>;
$line=<SLOPE>;
chop($line);
($aspect,$width) = split (' ', $line);
$line2=<SLOPE>;
chop($line2);
($nofp,$length) = split (' ', $line2);
$line3=<SLOPE>;
chop($line3);
($length{1},$slope{1},$length{2},$slope{2},$length{3},$slope{3},$length{4},$slope{4},$length{5},$slope{5},$length{6},$slope{6},$length{7},$slope{7},$length{8},$slope{8},$length{9},$slope{9},$length{10},$slope{10},$length{11},$slope{11},$length{12},$slope{12},$length{13},$slope{13},$length{14},$slope{14},$length{15},$slope{15},$length{16},$slope{16},$length{17},$slope{17},$length{18},$slope{18},$length{19},$slope{19},$length{20},$slope{20}) = split (' ', join (' ', split (/,/, $line3)));

close (SLOPE);

$nofe = $nofp - 1;    

open(OUT, ">>$slope_number.out") || die("Cannot Open File");
        print OUT "$version";
        print OUT "$p1";
        print OUT "$p2";
        print OUT "$p3";
        print OUT "$p4";
        print OUT "$nofe\n";
        print OUT "$aspect $width\n";

    $counter = $nofe;
    $length_index = 2;
    $slope_index = 1;
    $slope_index2 = 2;
    $cumulative_length = 0.0;
    while ($counter != 0.0) {
        $ofe_length = $length * $length{$length_index} - $cumulative_length;
        print OUT "2 $ofe_length\n";
        print OUT "0.0, $slope{$slope_index} 1.0, $slope{$slope_index2}\n";
        $slope_index = $slope_index + 1;
        $slope_index2 = $slope_index2 + 1;
        $length_index = $length_index + 1;
        $cumulative_length = $cumulative_length + $ofe_length;
        $counter = $counter - 1.0;
        };
close(OUT);

$area = $width * $cumulative_length;

open(OUT2, ">>slope_ofe.out") || die("Cannot Open File");
        print OUT2 "$slope_number $nofe $width $cumulative_length $area\n";
close(OUT2)

};


'''