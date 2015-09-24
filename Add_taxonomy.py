#!/usr/bin/env python

# import the modules
import sys, os

# Usage: Add_taxonomy.py [nodes.dmp] [taxon_id.txt] [blast.tsv] [output blast]

def create_tree_dic():

	# create the empty tree dic
	tree = {}
	#taxon_list = ['superkingdom', 'kingdom', 'phylum', 'superclass', 'class', 'subclass',
	#		'order', 'suborder', 'superfamily', 'family', 'genus', 'subgenus',
	#		'species', 'subspecies']
        taxon_list = ['phylum', 'class', 'order', 'family', 'genus', 'species']

	# for each node - parent relation: add it to the dictionary
	for line in open(sys.argv[1]):
		line = line.split('|')
		# if the node is an taxon found in the taxon list
		# add it to tree with a marking (!), else add it without
		if line[2].strip() in taxon_list:
			tree[line[0].strip() + '!'] = line[1].strip()
		else:
			tree[line[0].strip()] = line[1].strip()

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
	#output_blast = open(os.path.splitext(sys.argv[3])[0] + '_taxonomy.tsv', 'w')

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

	# get a list of the nested taxonIDs
	temp, taxonomy = [ID+'!'], []

	# keep adding higher taxons till the node (1) is reached
	while temp[-1] != '1!':
		try:
			try:
				# try to add a relevant node (including "!")
				temp.append(tree[temp[-1]])
			except:
				# if the previous node is not relevant remove the "!"
				# and try to add it again.
				temp[-1] = temp[-1][:-1]
				temp.append(tree[temp[-1]])
			# asume the next taxon is relevant and add a "!"
			temp[-1] = temp[-1] + '!'
		except:
			# if no higher taxon can be found assume taxon 1
			temp.append('1')

	# sort root -> node
	temp = temp[::-1][1:]

	# get the node names rather than IDs for each relevant node (includes !)
	for ID in temp:
		if '!' in ID:
			taxonomy.append(taxonID[ID.replace('!','')])


	#print taxonomy
	# return the taxonomy in string format
	return ' / '.join(taxonomy)

expand_blast(create_tree_dic(), read_taxonID())
