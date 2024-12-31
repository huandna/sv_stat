#!/work1/Users/wangyaoxin/software/anaconda3/bin/python
"""
Put some general, high-level documentation here
"""
import argparse
import os
from collections import defaultdict
import re

def main():
    parser = argparse.ArgumentParser( description='Put a description of your script here')
    parser.add_argument('-i', '--sv_file', type=str, required=True, help='three colunm chr,start,end,type' )
    parser.add_argument('-g', '--gff_file', type=str, required=True, help='gff3 file,need exon and UTR message' )
    parser.add_argument('-o', '--out_file', type=str, required=True, help='Path to an output file to be read' )
    args = parser.parse_args()
    #tags="CDS exon five_prime_UTR gene mRNA three_prime_UTR"
    all_dic=defaultdict(list)
    with open(args.gff_file,'r') as f:
        for line in f.readlines():
            line=line.strip().split()
            chr,type,start,end,id=line[0],line[2],line[3],line[4],line[8]
            if type=='exon':
                all_dic.setdefault(chr,[]).append([start,end,id,type])
            elif type=='five_prime_UTR':
                all_dic.setdefault(chr,[]).append([start,end,id,type])
                if line[6]=="+":
                    end=start
                    start=int(start)-2000
                    all_dic.setdefault(chr,[]).append([start,end,id,'twokb_up_to_5_prime_UTR'])
                elif line[6]=="-":
                    start=int(end)
                    end=int(end)+2000
                    all_dic.setdefault(chr,[]).append([start,end,id,'twokb_up_to_5_prime_UTR'])
                else:
                    print("error",line)
                    break
            elif type=='three_prime_UTR':
                all_dic.setdefault(chr,[]).append([start,end,id,type])
                if line[6]=="+":
                    start=int(end)
                    end=int(end)+1000
                    all_dic.setdefault(chr,[]).append([start,end,id,'onekb_down_to_3_prime_UTR'])
                elif line[6]=="-":
                    end=int(start)
                    start=int(start)-1000
                    all_dic.setdefault(chr,[]).append([start,end,id,'onekb_down_to_3_prime_UTR'])
                else:
                    print("error",line)
                    break
            elif type=='mRNA':
                all_dic.setdefault(chr,[]).append([start,end,id,"mRNA"])
            else:
                continue

    g=open(args.out_file,'w')
    with open(args.sv_file,'r') as f:
        for line in f.readlines():
            line=line.strip().split()
            chr,type,start,end=line[0],line[3],line[1],line[2]
            if all_dic[chr]==[]:
                continue
            else:
                sv_region=[]
                id=[]
                for region in all_dic[chr]:
                    pos=sorted([int(i) for i in region[0:2]])
                    if (int(start)>=pos[0] and int(start)<=pos[1]) or (int(end)>=pos[0] and int(end)<=pos[1]):
                        sv_region.append(region[-1]) 
                        if region[-1]!="mRNA":
                            id.append(re.findall(r'Parent=(.+)',region[-2])[0])
                        else:
                            #print(region[-2])
                            id.append(re.findall(r'ID=(.+?);',region[-2])[0])                
                    else:
                        pass
            if sv_region==["mRNA"]:
                sv_region.append("intron")
                id.append("INTRON")
            elif sv_region==[]:
                sv_region.append("intergenic")
                id.append("INTER")
            else:
                pass
            print(f'{chr}\t{type}\t{start}\t{end}\t{";".join(id)}\t{";".join(sv_region)}',file=g)
    g.close()
                    
                        

if __name__ == '__main__':
    main()
