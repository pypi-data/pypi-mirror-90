# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2020
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------
import json
import pandas as pd
import numpy as np
from lime.lime_tabular import LimeTabularExplainer

class PerturbationsUtil():
    ''' Generates scoring perturbations for the given input data point'''

    def __init__(self, training_stats:json, input_row: list, mode: str, num_perturbations=5000):
        """
        Arguments:
            training_stats:
                The training statistics required for Explainability
            input_row:
                The input row for which the perturbations need to be generated
            mode:
                The problem type of the machine learning model. mode value can be either classification
                or regression
            num_perturbations:
                The number of pertubations to be generated
        """
        self.training_stats = training_stats
        self.input_row = input_row
        self.mode = mode
        self.num_perturbations = num_perturbations
        revised_stats = self.__compute_revised_stats()
        self.__parse_training_stats(revised_stats)

    def __compute_revised_stats(self):
        revised_stats = {}
        for key, value in self.training_stats.items():
            if type(value) == dict:
                dict_value = {}
                for key1, value1 in value.items():
                    dict_value[int(key1)] = value1
                revised_stats[key] = dict_value
            else:
                revised_stats[key] = value
        return revised_stats
    
    def __parse_training_stats(self, revised_stats):
        self.training_labels = revised_stats.get("class_labels")
        self.feature_names = revised_stats.get("feature_columns")
        self.categorical_features = list(dict(revised_stats.get(
            "categorical_columns_encoding_mapping")).keys())
        self.categorical_names = revised_stats.get("categorical_columns_encoding_mapping")
        self.training_data_stats = revised_stats
        data_frame = pd.DataFrame(
            np.zeros((1, len(self.feature_names))), columns=self.feature_names)
        self.data = data_frame[self.feature_names].values
        self.categorical_features1 = [int(x) for x in self.categorical_features]
        self.stats = {
            "means": revised_stats.get("d_means"),
            "mins": revised_stats.get("d_mins"),
            "maxs": revised_stats.get("d_maxs"),
            "stds": revised_stats.get("d_stds"),
            "feature_values": revised_stats.get("feature_values"),
            "feature_frequencies": revised_stats.get("feature_frequencies")
        }

    def get_encoded_input_data_point(self, input_row):
        encoding_map = self.categorical_names
        for i in self.categorical_features1:
            value = input_row[i]
            encoded_value = encoding_map[i].index(
                        value)
            input_row[i] = encoded_value
        return input_row

    def generate_perturbations(self):
        data_row = self.get_encoded_input_data_point(self.input_row)
        lime_tabular = LimeTabularExplainer(self.data, feature_names=np.asarray(self.feature_names),
                                    categorical_features=self.categorical_features1,
                                    categorical_names=self.categorical_names,
                                    mode=self.mode,
                                    random_state=10,
                                    training_data_stats=self.stats)
        _, response = lime_tabular._LimeTabularExplainer__data_inverse(np.array(data_row), self.num_perturbations)
        response_data = response[1:]
        for feature in self.feature_names:
            feature_values = response_data[:, self.feature_names.index(feature)]
        df = pd.DataFrame(response_data, columns=self.feature_names)
        df = self.__get_decoded_value(df)
        return df
    
    def __get_decoded_value(self, df):
        for key, value in self.categorical_names.items():
            feature_value = df[self.feature_names[key]]
            feature_value_decoded = [value[int(x)] for x in feature_value]
            df[self.feature_names[key]] = pd.Series(feature_value_decoded)
        return df

