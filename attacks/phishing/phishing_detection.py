import pickle
import warnings
import numpy as np
import pandas as pd
from model.feature import FeatureExtraction

warnings.filterwarnings("ignore")

def load_fake_url(file):
    """ Loads the url list from a text file
    
        input: url list text file
        output: url list
    
    """

    # Open text file and readlines into a list
    with open(file, "r") as fileURL:
        url_list = fileURL.readlines()

    return url_list


def url_detection(url_list):

    """ Iterates through each url and runs the MLP neural network model to check the 
    phishing probability
    
        input: url list
        output: phishing probability
    
    """

    for url in url_list:

        print(f"The url check is: {url}")

        if url == "https://elec0138-forum.0138019.xyz/":
            print(f"{url} is the original website") 

        # Call FeatureExtraction function from feature.py
        obj = FeatureExtraction(url)

        # Load the trained Neural network model
        with open("model/model.pkl", "rb") as file:
            mlp = pickle.load(file)
        
        # Run the model
        x = np.array(obj.getFeaturesList()).reshape(1, 30)
        y_pred = mlp.predict(x)[0]
        y_prbability_phishing = mlp.predict_proba(x)[0, 0]
        print(f"The MLP model predicts that '{url}' has a phishing probability of {y_prbability_phishing}\n")


if __name__=="__main__":

    fakeURL_file = "URL_list.txt"
    url_list = load_fake_url(fakeURL_file)

    url_detection(url_list)
