import pandas as pd

def read_file(file):
  input_df = pd.read_csv(file, header=None)
  return input_df