function [] = generate_networkneuro(config)

if ~isdeployed
    disp('loading path')
    addpath(genpath('/N/u/hayashis/git/vistasoft'))
    addpath(genpath('/N/u/brlife/git/jsonlab'))
    addpath(genpath('/N/u/brlife/git/wma_tools'))
    addpath(genpath('/N/u/bacaron/git/fine'))
end

% load the config.json
config = loadjson(config);

% load .tck streamlines without downsampling
fg = dtiImportFibersMrtrix(config.track, 0.5);

% load netw.mat file containing important info
netw = load('netw.mat');

% set and make outdir if not already generated
outdir = fullfile(pwd,'output','roipairs');

if ~exist(outdir,'dir')
	mkdir(outdir);
end

% run function to create networkneuro information
[ jout, ofib ] = fnEdgesToJson(netw,fg,outdir);

