import pickle
import warnings
import numpy as np
import pandas as pd
from model.feature import FeatureExtraction

warnings.filterwarnings("ignore")

def load_fake_url(file):

    with open(file, "r") as fileURL:
        url_list = fileURL.readlines()

    return url_list


def url_detection(url_list):

    for url in url_list:

        print(f"The url check is: {url}")

        if url == "https://elec0138-forum.0138019.xyz/":
            print(f"{url} is the original website") 


        obj = FeatureExtraction(url)

        with open("model/model.pkl", "rb") as file:
            mlp = pickle.load(file)
        
        x = np.array(obj.getFeaturesList()).reshape(1, 30)
        y_pred = mlp.predict(x)[0]
        y_prbability_phishing = mlp.predict_proba(x)[0, 0]
        print(f"The MLP model predicts that '{url}' has a phishing probability of {y_prbability_phishing}\n")

if __name__=="__main__":

    fakeURL_file = "URL_list.txt"
    url_list = load_fake_url(fakeURL_file)

    url_detection(url_list)
