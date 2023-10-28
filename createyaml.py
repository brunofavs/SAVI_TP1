#!/usr/bin/env python3

import yaml



    
data_yaml = """
- 'pedro'
- '/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Face_samples_dataset/0/WhatsApp Image 2023-10-26 at 23.10.45.jpeg'

"""

data = yaml.safe_load(data_yaml)

with open('data.yaml', 'w') as file:
    yaml.dump(data, file)

print(open('data.yaml').read())


