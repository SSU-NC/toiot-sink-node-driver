import argparse

parser = argparse.ArgumentParser(description='PDK-sink-node-driver options')
parser.add_argument('--w', required=True, help='the raspbian webserver')
parser.add_argument('--k', required=True, help='kafka')
parser.add_argument('--b', required=True, help='mqtt broker ip')
args = parser.parse_args()
