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
	if isinstance(label_nodes[0],str):
		label_nodes = [ int(f) for f in label_nodes ]
	label_names = [ f['name'] for f in labels ]

	# load assignments csv indicating the roi pair for each streamline
	assignments_index = pd.read_csv(config['index'],header=None).rename(columns={0: "index"})
	assignments_names = pd.read_csv(config['names'],header=None).rename(columns={0: "names"})
	assignments = pd.concat([assignments_index, assignments_names], axis=1)
	assignments.to_csv('./netneuro/output/assignments.csv',index=False)

	# identify unique node pairings
	unique_edges = [ [int(f.split('_')[0]),int(f.split('_')[1])] for f in assignments.loc[assignments["names"] != "not-classified"].names.unique().tolist() ]

	# generate edge inices assignemnts
	streams_indices = assignments.index.tolist()

	# load conmats
	print('loading conmats')
	conmats = ['count','length','density','denlen']
	conmats_dict = {}
	for i in conmats:
		path = config[i]+'/correlation.csv'
		conmats_dict[i] = pd.read_csv(path,header=None).values
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

		combined_name = str(i[0])+'_'+str(i[1])
		# grab the edge information from assignments
		st_ind = assignments.loc[assignments['names'] == combined_name]

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
		tmp['roi1'] = ridx1
		tmp['roi2'] = ridx2

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
