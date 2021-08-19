# -*- coding: utf-8 -*-


import os, re
import argparse
from vectorizers.tokenizationK import FullTokenizer

import pdb

# 상황에 따라서 다른 tokenizer를 사용해도 된다.
tokenizer = FullTokenizer(vocab_file="./bert-module/assets/vocab.korean.rawtext.list")


multi_spaces = re.compile(r"\s+")

def process_file(file_path, output_dir):
    """
    단방향 데이터가 있는 file_path을 argument로 주면 가공을 한 이후에
    output_dir 아래에 2개의 파일(seq.in, label)을 저장해 주는 함수.
    output_dir의 경우 만약 존재하지 않는다면 
    """
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    data = open(file_path).read().splitlines()

    # line별로 process를 해준 뒤,
    processed_data = [process_line(line, tokenizer) for line in data]

    intentions = list(map(lambda x: x[0], processed_data))
    tokens = list(map(lambda x: x[1], processed_data))

    # seq_in : 토큰들로만 이루어진 파일
    intention_file = os.path.join(output_dir, "label")
    seq_in = os.path.join(output_dir, "seq.in")

    with open(intention_file, "w") as f:
        f.write("\n".join(intentions) + "\n")

    with open(seq_in, "w") as f:
        f.write("\n".join(tokens)+ "\n")


def process_line(line, tokenizer):
    """
    데이터를 라인별로 처리해 주는 함수이다.

    """
    intention, sentence = line.split("\t")
    tokens = ""

    for word in sentence.split():
        word_tokens = " ".join(tokenizer.tokenize(word))
        tokens += word_tokens + " "

    tokens = multi_spaces.sub(" ", tokens.strip())

    return intention, tokens


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help = '단방향 데이터 형식의 텍스트 파일', type = str, required = True)
    parser.add_argument('--output', '-o', help = 'Path to data', type = str, required = True)

    args = parser.parse_args()
    file_path = args.input
    output_dir = args.output

    process_file(file_path, output_dir)
