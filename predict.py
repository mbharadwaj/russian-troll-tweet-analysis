import csv
import json
import os
from os import mkdir
from os.path import exists
import settings

import boto3
from google.cloud import automl_v1beta1

AWS_ML_ENDPOINT = os.getenv("AWS_ML_ENDPOINT")
AWS_ML_MODEL_ID = os.getenv("AWS_ML_MODEL_ID")
GCP_AUTOML_PROJECT_ID = os.getenv("GCP_AUTOML_PROJECT_ID")
GCP_AUTOML_MODEL_ID = os.getenv("GCP_AUTOML_MODEL_ID")


def get_records(source_dir, source_file):
    records = []
    file_name = os.path.join(source_dir, source_file)
    with open(file_name, 'r') as file:
        records = file.readlines()
    return records


def save_results(classified_results, target_dir, source_file):
    target_filename = os.path.join(target_dir, source_file + ".csv")
    fieldnames = ['text', 'label']

    with open(target_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        rows = []
        for text, label in classified_results.items():
            rows.append({"text": text.strip(), "label": label})

        writer.writerows(rows)


class AWSPredict(object):
    def __init__(self):
        self.ml_client = boto3.client(service_name='machinelearning', use_ssl=True)

    def predict(self, source_dir, source_file, target_dir):
        records = get_records(source_dir, source_file)
        if not exists(target_dir):
            mkdir(target_dir)

        classified_results = {}
        for record in records:
            response = self.ml_client.predict(
                MLModelId=AWS_ML_MODEL_ID,
                Record={
                    'text': record
                },
                PredictEndpoint=AWS_ML_ENDPOINT
            )
            prediction = response['Prediction']['predictedLabel']
            classified_results[record] = prediction
            save_results(classified_results, target_dir, source_file)


class GCPPredict(object):
    def __init__(self):
        self.prediction_client = automl_v1beta1.PredictionServiceClient()

        self.prediction_api_name = 'projects/{}/locations/us-central1/models/{}'.format(GCP_AUTOML_PROJECT_ID,
                                                                                        GCP_AUTOML_MODEL_ID)

    def predict(self, source_dir, source_file, target_dir):
        records = get_records(source_dir, source_file)
        if not exists(target_dir):
            mkdir(target_dir)

        classified_results = {}
        for record in records:
            payload = {'text_snippet': {'content': record, 'mime_type': 'text/plain'}}
            params = {}
            response = self.prediction_client.predict(self.prediction_api_name, payload, params)
            prediction = response.payload[0].display_name
            classified_results[record] = prediction
            save_results(classified_results, target_dir, source_file)


if __name__ == '__main__':
    predict_obj = GCPPredict()
    predict_obj.predict("gcp_translated", "Russian_Russian_NonEnglish_622804.txt.1", "gcp_predicted")
