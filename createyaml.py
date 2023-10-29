#!/usr/bin/env python3

import yaml

# data_yaml = """
# - 'pedro'
# - '/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1
# """

data_yaml = {"name" : "ola",
             "img_path" : "./Face_samples_dataset/0/WhatsApp Image 2023-10-26 at 23.10.45.jpeg"}


with open('data2.yaml', 'w') as file:
    yaml.dump(data_yaml, file)

print(open('data2.yaml').read())


