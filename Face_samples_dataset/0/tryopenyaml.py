#!/usr/bin/env python3

import yaml


def main():
    
    with open('data.yaml', 'r') as file:
        data_yaml = yaml.safe_load(file)

    print(data_yaml[0])
    print(data_yaml[1])
    


if __name__ == '__main__':
    main()


