import argparse
from typing import List


variables = {
    'variables': {
        'DOCKER_DRIVER': 'overlay2'
    }
}



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates pipeline configuration in YAML format')
    parser.add_argument('-o', '--out', help='filename of output yml', required=True)

    args = vars(parser.parse_args())


