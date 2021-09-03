#!/bin/bash
module load matlab/2019a

mkdir -p compiled

log=compiled/commit_ids.txt
true > $log

cat > build.m <<END
addpath(genpath('.'));
addpath(genpath('./jsonlab'));
addpath(genpath('./vistasoft'));
addpath(genpath('./fine'));

mcc -m -R -nodisplay -d compiled main
exit
END

matlab -nodisplay -nosplash -r build && rm build.m
