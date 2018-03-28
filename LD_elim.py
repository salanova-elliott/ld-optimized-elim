#Input: SNP pairs on new lines separated by tabs
import os, sys, re

snp_pairs = open(sys.argv[1])

snp_catch = '(\d+\_\d+)\t(\d+\_\d+)'
elim_snps = []

def read_file(file_obj):
	
	snp_pos_dict = {}
	snp_count = []
	current_snp = 0
	
	for line in file_obj:
		
		snp_search = re.search(snp_catch, line)
	
		if snp_search:
	
			if snp_search.group(1) not in snp_pos_dict:
				 snp_pos_dict[snp_search.group(1)] = current_snp
				 snp_count.append( [1, snp_search.group(1)] )
			 
				 current_snp += 1
			 
			else:
				snp_count[snp_pos_dict[snp_search.group(1)]][0] += 1 
				
			if snp_search.group(2) not in snp_pos_dict:
				 snp_pos_dict[snp_search.group(2)] = current_snp
				 snp_count.append( [1, snp_search.group(2)] )
			 
				 current_snp += 1
			 
			else:
				snp_count[snp_pos_dict[snp_search.group(2)]][0] += 1 
	
	print "Total unique SNPs : " + str(current_snp + 1)
	
	return snp_count
			 
def find_new_snp(snp_count):

	snp_count_sort = list(snp_count)

	snp_target = sorted(snp_count_sort, reverse = True)[0]

	print "Eliminating " + snp_target[1] + " that occurs in " + str(snp_target[0]) + " match(es)..."
	
	return snp_target[1]

snp_list = read_file(snp_pairs)

while not elim_snps or snp_list:
	
	elim_snp = find_new_snp(snp_list)

	elim_snps.append(elim_snp)

	file_object_1 = open(sys.argv[1])

	scratch_file = open( 'workfile.txt' , 'w')
	for line in file_object_1:
	
			snp_search = re.search(snp_catch, line)
	
			if snp_search: 
			
				if snp_search.group(1) not in elim_snps and snp_search.group(2) not in elim_snps:
					scratch_file.write(snp_search.group(1) + "	" + snp_search.group(2) + "\n")
	scratch_file.close()
			
	snp_list = read_file(open("workfile.txt"))
	
print "Total Eliminated SNPs: " + str(len(elim_snps))

os.remove('workfile.txt')
output_file = open( "elim_snps.txt", "w")
for item in elim_snps:
	output_file.write(item + "\n")