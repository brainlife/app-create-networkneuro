addpath(genpath('.'));
addpath(genpath('./jsonlab'));
addpath(genpath('./vistasoft'));
addpath(genpath('./fine'));

mcc -m -R -nodisplay -d compiled generate_networkneuro 
exit
