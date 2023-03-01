import os
from glob import glob
import pandas as pd
import numpy as np
import json
from scipy.stats import entropy
import numba
from numba import jit


def create_dict_exps(folder_experiments, nav_str):

    dict_exps = {}

    folders= [f for f in os.listdir(folder_experiments) if not "ipynb_checkpoints" in f]

    for exp in folders:

        #retrieve sim parameters
        try:
            with open(folder_experiments+"/"+exp+"/log.json") as json_file:
                dict_json = json.load(json_file)

            demand_name = dict_json['route_filename'].split("/")[-1]
            pct_routed = demand_name.split(nav_str+"_")[1].split("_")[0]
            pct_non_routed = demand_name.split("dua_")[1].split("_")[0]
            n_rep = demand_name.split("rep_")[1].split("_")[0]

            key_de = pct_routed+"_"+pct_non_routed

            if key_de in dict_exps:
                dict_exps[key_de][n_rep] = exp
            else:
                dict_exps[key_de] = {n_rep: exp}
        except:
            pass
                
    return dict_exps



def create_dict_results_total(dict_exps, folder_experiments, measure, how, normalize_by=None):

    dict_final = {}

    for scenario in dict_exps.keys():

        sorted_dict = dict(sorted(dict_exps[scenario].items(), key=lambda item: item[0]))
        tmp_results = []
        
        for exp_run in sorted_dict: 
            df = pd.read_csv(glob(folder_experiments+sorted_dict[exp_run]+f"/{how}_measures.csv")[0])
            
            if normalize_by is not None:
                
                edge_length_list = []
                for e_id in zip(df["edge_id"]):
                    edge_length_list.append(normalize_by[e_id[0]])

                df["edge_length_m"] = edge_length_list
                value = (df[measure]/df["edge_length_m"]).sum()
            
            else:           
                value = df[measure].sum()
                
            tmp_results.append(value)

        dict_final[scenario] = tmp_results
        
    return dict_final




def create_dict_results_entropy(dict_exps, folder_experiments, measure, how, normalize_by=None):

    dict_final = {}

    for scenario in list(dict_exps.keys()):

        sorted_dict = dict(sorted(dict_exps[scenario].items(), key=lambda item: item[0]))
        tmp_results = []
        for exp_run in sorted_dict: 
            df = pd.read_csv(glob(folder_experiments+sorted_dict[exp_run]+f"/{how}_measures.csv")[0])
            
            if normalize_by is not None:
                
                edge_length_list = []
                for e_id in zip(df["edge_id"]):
                    edge_length_list.append(normalize_by[e_id[0]])

                df["edge_length_m"] = edge_length_list
                value_list = list(df[measure]/df["edge_length_m"])
            
            else:
                value_list = list(df[measure])

            
            entropy_value = entropy(np.array(value_list))
            tmp_results.append(entropy_value)

        dict_final[scenario] = tmp_results
    
    return dict_final






