#!/work1/Users/wangyaoxin/software/anaconda3/bin/python
"""
Put some general, high-level documentation here
"""
import argparse
import os
import re
from collections import defaultdict

#Chr1    15617252        SNP41482        A       G       .       PASS    END=15617252;ChrB=Chr1;StartB=14910793;EndB=14910793;Parent=SYN2;VarType=ShV;DupType=.

def main():
    parser = argparse.ArgumentParser( description='Put a description of your script here')
    parser.add_argument('-i', '--in_file', type=str, required=True, help='Path to an input file to be read' )
    parser.add_argument('-o', '--out_file', type=str, required=True, help='Path to an input file to be read' )
    args = parser.parse_args()
    dic=defaultdict(int)
    with open(args.in_file,"r") as f:
        for line in f.readlines():
            line=line.strip()
            if line[0]=="#":
                continue
            else:
                line=line.split()
                if re.match(r'([A-Z]+)',line[2]):
                    ID=re.findall(r'([A-Z]+)',line[2])[0]
                    end=re.findall(r'END=([\d]+);',line[7])[0]
                    print(f'{line[0]}\t{line[1]}\t{end}\t{ID}')
                    dic[ID]+=1
                else:
                    print("error",line[2])
    g=open(args.out_file,"w")
    print(f'Type\tNumber',file=g)
    for i,v in dic.items():
        print(f'{i}\t{v}',file=g)
    g.close()
if __name__ == '__main__':
    main()
