import pandas as pd
import numpy as np
import glob
import pickle
import os
import json

from sklearn.metrics import classification_report
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--exp', type=str, default="test", help='Experiment name')

args = parser.parse_args()

folders = glob.glob('./{}_seed*'.format(args.exp))
results = []

for folder in folders:
  runs = glob.glob('{}/*'.format(folder))
  for run in runs:
    model_file = "{}/model.pkl".format(run)
    args_file = "{}/commandline_args.json".format(run)
    preds_file = "{}/prediction_TESTSET.csv".format(run)

    if os.path.exists(args_file):
      df = pd.read_csv(preds_file)
      acc = accuracy_score(df['truth'], df['prediction'])
      f1 = f1_score(df['truth'], df['prediction'], average="micro")
      
      with open(args_file, 'r') as f:
        configs = json.load(f)

      tmp = {}
      tmp['Model Name'] = run.replace(folder + '/','')
      tmp['Accuracy'] = acc
      tmp['F1'] = f1

      for k in configs:
        tmp["config_" + k] = configs[k]
        
      results.append(tmp)