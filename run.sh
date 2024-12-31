python syri_vcf_stat2.py -i syri_ordered.vcf -o out.xls > sv_simple.xls
awk '$4!="SNP"{print}' sv_simple.xls > sv_simple_no_SNP.xls
python Sv_Region_Stat.py -i sv_simple_no_SNP.xls -g pasa2.longest.filter.gff3 -o sv_stat.xls > log
python Sv_Region_Stat.py -i sv_simple_only_SNP.xls -g pasa2.longest.filter.gff3 -o snp_stat.xls > log2
