from readers.data_reader import Reader
from vectorizers import tokenizationK as tk

import argparse
import os
import pdb

# read command-line parameters
parser = argparse.ArgumentParser('Get the vectors from tokens')
parser.add_argument('--data', '-d', help = 'Path to data', type = str, required = True)
parser.add_argument('--tsv', '-t', help = 'Path to {meta,vecs}.tsv', type = str, required = True)

args = parser.parse_args()
data_folder_path = args.data
tsv_folder_path  = args.tsv

# read tokenized data from ${data_folder_path}
with open(os.path.join(data_folder_path, 'seq.in'), encoding='utf-8') as f:
    text_arr = f.read().splitlines()

# read tsvs from ${tsv_folder_path}
with open(os.path.join(tsv_folder_path, 'vecs.tsv'), encoding='utf-8') as f:
    vecs = f.read().splitlines()

with open(os.path.join(tsv_folder_path, 'meta.tsv'), encoding='utf-8') as f:
    meta = f.read().splitlines()

# tokenizer
tokenizer = tk.FullTokenizer('./bert-module/assets/vocab.korean.rawtext.list')

# get all token ids that is used in the data
print('collecting token_ids from tokenized data...')
token_id_set = set()
for text in text_arr:
    token_id_set.update(tokenizer.convert_tokens_to_ids(text.split()))

# token_ids = sorted(map(lambda x: x+1, token_id_set)) # add 1 since id starts from 0..?
token_ids = sorted(token_id_set)

# get vecs and meta from 
vecs_appeared = [vecs[i] for i in token_ids]
meta_appeared = [meta[i] for i in token_ids]

# save 
print('saving vecs and meta that appeared in the dataset')
with open(os.path.join(data_folder_path, 'vecs_appeared.tsv'), 'w') as f:
    f.write('\n'.join(vecs_appeared))

with open(os.path.join(data_folder_path, 'meta_appeared.tsv'), 'w') as f:
    f.write('\n'.join(meta_appeared))
