import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn import metrics
import pickle


def data_preprocessing(file):

    """ Loads the csv data, converts it into a dataframe. Then preprocess it
    
        input: csv file
        output: processed data
    
    """

    # Read the csv file
    df = pd.read_csv(file)

    #  Remove any leading or trailing spacees from all column names
    df.columns = df.columns.str.strip()

    # Select all rows from Labek column and return an array of uniques values in that columns
    df.loc[:, 'Label'].unique()

    # Remove any NaN values
    df = df.dropna()

    #checking column data types
    (df.dtypes == 'objects')

    # Mapping the labels to a value of 0 and 1
    df['Label'] = df['Label'].map({'BENIGN': 0, 'DDoS': 1})

    # Remove rows with any values that are not finite
    df_new = df[np.isfinite(df).all(1)]


    # plot the bar
    plt.bar([0, 1], df_new['Label'].value_counts(), edgecolor='black')
    plt.xticks([0, 1], labels=['BENIGN=0', 'DDoS=1'])
    plt.xlabel('Classes')
    plt.ylabel('Count')
    plt.title('Distribution of Classes')
    plt.savefig('classes_distribution.png')

    return df_new



def data_splitting(df):

    """ Splits the data into training and testing datasets
    
        input: processed dataframe data
        output: splitted data
    
    """

    # Create  X (parameters) and Y (labels) variables 
    X = df.drop('Label', axis=1)
    Y = df['Label']

    # Perform a dataset split to: 70% training and 30% test
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

    print("The train dataset size = ", X_train.shape)
    print("The test dataset size = ", X_test.shape)

    return X_train, X_test, y_train, y_test



def nn_model(X_train, X_test, y_train, y_test):

    """ Collects the splitted data and trains the NN model. Then test it.
    
        input: training and testing datasets
        output: model's accuracy and confusion matrix figure
    
    """

    # Train the neural network model
    nn_model = MLPClassifier(hidden_layer_sizes=(10,), max_iter=40, random_state=42)
    nn_model.fit(X_train, y_train)

    # Save the trained model
    with open("model.pkl", "wb") as file:
        pickle.dump(nn_model, file)

    # Test the trained model into a test set
    nn_pred = nn_model.predict(X_test)

    # Evaluate the model
    print('\nNeural Network Metrics:')
    print(f'Accuracy: {metrics.accuracy_score(y_test, nn_pred)}')
    print(f'F1 Score: {metrics.f1_score(y_test, nn_pred)}')
    print(f'Precision: {metrics.precision_score(y_test, nn_pred)}')
    print(f'Recall: {metrics.recall_score(y_test, nn_pred)}')

     # Performs classification report
    print("Classification report : ")
    print(metrics.classification_report(y_test, nn_pred, target_names=['BENIGN', 'DDoS']))

    # Generates confusion matrix
    matrix = metrics.confusion_matrix(y_test, nn_pred)
    plt.figure(figsize=(10, 7), dpi=200)
    metrics.ConfusionMatrixDisplay(matrix, display_labels=['BENIGN', 'DDoS']).plot(cmap=plt.cm.Blues, xticks_rotation='vertical')
    plt.title("Confusion Matrix for NN",  fontsize=20)
    plt.savefig('Confusion_Matrix_NN.png', bbox_inches = 'tight')
    


if __name__=="__main__":

    # Dataset csv file
    file = "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"

    df = data_preprocessing(file)

    X_train, X_test, y_train, y_test = data_splitting(df)

    nn_model(X_train, X_test, y_train, y_test)