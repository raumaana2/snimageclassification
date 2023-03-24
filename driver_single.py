from input import Input
import os, argparse
from sys import path

path.append(f'{os.getcwd()}/utils')
path.append(f'{os.getcwd()}/noiseprint2')
path.append(f'{os.getcwd()}/cnn_single')

from utils.load_iplab import load_iplab
from utils.load_fodb import load_fodb
from utils.preprocessor import builder
from cnn_single.cnn_train import train
from cnn_single.cnn_test import test


# parse cli args to pick preprocessing, train, test and domain
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--process", help="preprocess flag", action='store_true')
parser.add_argument("-t", "--train", help="train model", action='store_true')
parser.add_argument("-e", "--test", help="evaluate model", action='store_true')
args = parser.parse_args()

# input variables
classes = ['facebook', 'instagram', 'orig', 'telegram', 'twitter',  'whatsapp']
dataset = 'fodb'
h_input = Input(dataset, patch_size=0, sf=[1,10], his_range=[-50, 50], domain="Histogram")
n_input = Input(dataset, domain="Noise", patch_size=64)

input = h_input


if args.process:
    dset = {'fodb': load_fodb, 'iplab': load_iplab}.get(dataset, load_iplab)(classes, os.getcwd())
    builder(input, dset)



epochs = 10 
batch_size = 32
architecture = 'dct_cnn'
location = 'dct_models'
name = f'cnn_{architecture}_{input.input_shape}_{epochs}_{batch_size}'
path = f'models/{name}/{name}'

if args.train:
    train(epochs, batch_size, architecture, location, input, classes, path)
if args.test:
    test(path, input, classes)
