{
'experiment_name': 'min_config', 
'D_blocks':[[]],
'U_blocks':[[]],
'B_blocks': [[('C',3)]],
'H': 1024,
'W': 2048,
'dropout_ratio': 0.1,
'momentum': 0.2,
'momentum_bn': 0.1,
'lr': 0.01,
'base_channels': 8,
'batch_size' : 2,
'num_samples': 1,
'debug':2,
'cpus_per_trial': 1,
}

# You can put furhter informatiom behind the above Python dictionary as illustrated here. Please begin every line with "#".
# 
# The above is a minimum viable configuration file that contains the minimum amount of key-value information that must be specified in any config file.
#
# What you may want to try out:
# 
# - add <'debug':2> to get more insights on what is going on under the hood
# 
# - add <num_samples:X> with X>1 to observe that now a search will be triggered. Of course, this only makes sense if you specify a search space in the above dictionary.
# Else the same architecture will be trained X times. This still may be a desirable behavior if you want to repeat the same experiment with different random seeds.
# 
# - modify 'H'/'W' to a e.g. half their previous values. This will interpolate the resolution of the data/labels to the specified solution.
# If you specify 'H', 'W' equal to the actual image size, no intperolation will take place. 


