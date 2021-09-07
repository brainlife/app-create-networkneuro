#!/usr/bin/env python3

###### this is a python port of fnEdgesToJson.m function from the FINE toolbox developed by Brent McPherson (IU 2021)
###### the intended usecase for this function is to be paired with an assignments.csv file provided by mrtrix3's tck2connectome function

import sys
import os
import json
import pandas as pd
import numpy as np
import nibabel as nib
from dipy.io.streamline import load_tractogram
	
def generate_networkneuro():

	# load config
	print('loading top variables')
	with open('config.json','r') as config_f:
		config = json.load(config_f)

	# load label.json
	with open(config['label'],'r') as label_f:
		labels = json.load(label_f)

	# set and make output dir
	outdir = './netneuro/roipairs/'
	if not os.path.isdir(outdir):
		os.mkdir(outdir)
	print('top variables loaded')

	# identify label nodes and names
	print('grabbing node information, including streamline assignments and unique edges')
	label_nodes = [ f['voxel_value'] for f in labels ]
	label_names = [ f['name'] for f in labels ]

	# load assignments csv indicating the roi pair for each streamline
	assignments = pd.read_csv('assignments.csv',header=None)
	assignments.rename(columns={0: 'pair1', 1: 'pair2'},inplace=True)
	assignments = assignments.loc[(assignments['pair1'] != 0) & (assignments['pair2'] != 0)]
	assignments = assignments.loc[(assignments['pair1'].isin(label_nodes)) & (assignments['pair2'].isin(label_nodes))]
	assignments = assignments.loc[assignments['pair1'] != assignments['pair2']]
	assignments = assignments.sort_values(by=['pair1','pair2'])

	# grab node labels
	node_labels = np.sort(assignments['pair1'].unique())

	# generate edge inices assignemnts
	streams_indices = assignments.index.tolist()
	unique_edges_unclean = assignments.groupby(['pair1','pair2']).count().index.values
	unique_edges_ordered = np.sort([ (f[1],f[0]) if f[0] > f[1] else f for f in unique_edges_unclean ])
	unique_edges = []
	for f in range(len(unique_edges_ordered)):
		if f == 0:
			unique_edges.append(list(unique_edges_ordered[f]))
		else:
			if list(unique_edges_ordered[f]) not in unique_edges:
				unique_edges.append(list(unique_edges_ordered[f]))
	unique_edges = np.sort(unique_edges)
	print('node information loaded')

	# load conmats
	print('loading conmats')
	conmats = ['count','length','density','denlen']
	conmats_dict = {}
	for i in conmats:
		conmats_dict[i] = pd.read_csv('./output/'+i+'.csv',header=None).values
	print('conmats loaded')

	# load wholebrain tractogram in parc space
	print('loading tractogram')
	ref_anat = nib.load(config['parc'])
	wholebrain = load_tractogram(config['track'],ref_anat)
	del ref_anat # save space
	print('tractogram loaded')

	# loop through edges and generate structure
	jj = 1
	count = 1
	jout = {}
	jout['roi_pairs'] = []
	ofib = []
	coords = []

	print('building networkneuro data structures')
	for i in unique_edges:

		# grab the edge information from assignments
		st_ind = assignments.loc[(assignments['pair1'] == i[0]) & (assignments['pair2'] == i[1]) | (assignments['pair1'] == i[1]) & (assignments['pair2'] == i[0])]

		# once 50 have been stored. this is to make loading for visualizer much quicker
		if jj > 50:
			# iterate the object / reset the count
			count = count + 1
			jj = 1
			coords = []

		if jj == 1:
			print(str(count))

		# pull roi indices
		ridx1 = i[0]
		ridx2 = i[1]

		# store node names
		tmp = {}
		tmp['roi1'] = [ int(f['label']) for f in labels if f['voxel_value'] == ridx1 ][0]
		tmp['roi2'] = [ int(f['label']) for f in labels if f['voxel_value'] == ridx2 ][0]
		
		# grab weights
		tmp['weights'] = {}
		tmp['weights']['density'] = conmats_dict['density'][ridx1-1][ridx2-1]
		tmp['weights']['count'] = len(st_ind)
		tmp['weights']['length'] = conmats_dict['length'][ridx1-1][ridx2-1]
		tmp['weights']['denlen'] = conmats_dict['denlen'][ridx1-1][ridx2-1]

		## grab streamlines
		# coords = {}
		tcoord = wholebrain.streamlines[st_ind.index.tolist()]

		# output coords in nested structure and round to 2 decimal places
		coords_kk = []
		for kk in range(len(tcoord)):
			# coords[jj-1].insert(kk,np.transpose(np.round(tcoord[kk],2).tolist()).tolist())
			coords_kk.append(np.transpose(np.round(tcoord[kk],2).tolist()).tolist())
			# coords[jj-1][kk] = np.transpose(np.round(tcoord[kk],2).tolist()).tolist()
		coords.append(coords_kk)

		# create filename to store streamline data
		tname = 'conn_'+str(count)+'.json'

		# store information
		tmp['filename'] = tname
		tmp['idx'] = jj-1
		jj = jj+1
		jout['roi_pairs'] = jout['roi_pairs'] + [ tmp ]
		ofib.append(coords)
	print('networkneuro data structures built')

	## writing out json outputs
	# for every collection of 50 files
	print('saving outputs')
	jj = 1
	count = 1
	for i in range(1,len(ofib)+1):
		if jj > 50:
			# iterate the object / reset the count
			count = count + 1
			jj = 1
			coords = []

		tname = 'conn_'+str(count)+'.json'
		with open(outdir+'/'+tname,'w') as out_f:
			json.dump(ofib[i-1],out_f)
		jj = jj+1

	# total index
	with open(outdir+'/index.json','w') as out_f:
		json.dump(jout,out_f)
	print('outputs saved')

if __name__ == '__main__':
	generate_networkneuro()