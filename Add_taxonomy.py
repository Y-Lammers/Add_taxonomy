#!/usr/bin/env python

# import the modules
import sys, os

# Usage: Add_taxonomy.py [nodes.dmp] [taxon_id.txt] [blast.tsv] [output blast]

def create_tree_dic():

	# create the empty tree dic
	tree = {}

	taxon_list = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']

	# for each node - parent relation: add it to the dictionary
	for line in open(sys.argv[1]):
		line = line.split('|')

		# add the rank and next ID to the tree dic
		tree[line[0].strip()] = [line[1].strip(), line[2].strip()]

	# return the tree dic
	return tree


def read_taxonID():

	# create the empty taxonID dic
	taxonID = {}
	
	# fill the dic with the taxonIDs + names
	for line in open(sys.argv[2]):
		line = line.strip().split('\t')
		taxonID[line[0]] = line[1]

	return taxonID


def expand_blast(tree, taxonID):

	# open the blast output file and expand the results with the number of reads per cluster
	
	# open the blast file and create a new file
	blast_list = [line.strip().split('\t') for line in open(sys.argv[3])]
	output_blast = open(sys.argv[4], 'w')

	# parse throuth the input blast hits
	for line in blast_list:
		if 'Query' in line[0]: line.append('Taxonomy')
		# grab the query sequence and look in the cluster_dic how many reads the cluster contains
		# insert this number in the second column and write the file
		else: line.append(get_taxonomy(tree, taxonID, line[-2]))
		output_blast.write('\t'.join(line) + '\n')

	# close the new blsat file
	output_blast.close()


def get_taxonomy(tree, taxonID, ID):

	# create an empty dic that will be filled up with the relevant ranks
	taxon_dic = {'kingdom':'unknown kingdom', 'phylum':'unknown phylum', 'class':'unknown class',
			'order':'unknown order', 'family':'unknown family', 'genus':'unknown genus', 'species':ID}

	# empty variables for the full taxonomy and the temporary taxonIDs
	temp, taxonomy, cur_ID = [ID], [], ID
	
	# Keep adding higher taxonIDs to the temp list till the rood node (1) is reached
	while temp[-1] != '1':

		# if first rank is added after the initial species rank
		if len(temp) != 1:
			# check if the previous rank is in the taxon dictionary
			# if so, add the ID to the dic
			if rank in taxon_dic:
				taxon_dic[rank] = cur_ID

			# check if the kingdom rank is filled in, if not use superkingdom
			if rank == 'superkingdom' and taxon_dic['kingdom'] == 'N/A':
				taxon_dic['kingdom'] = cur_ID

			cur_ID = next_ID

		# get the previous rank + ID
		next_ID, rank = tree[temp[-1]]

		# add the ID to the temp list
		temp.append(next_ID)

	# convert the taxonIDs in the taxon_dic to names for the taxonomy list
	for rank in ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']:
		if 'unknown' not in taxon_dic[rank]:
			taxonomy.append(taxonID[taxon_dic[rank]])
		else:
			taxonomy.append(taxon_dic[rank])

	# return the taxonomy
	return ' / '.join(taxonomy)

expand_blast(create_tree_dic(), read_taxonID())
