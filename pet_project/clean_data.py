from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import plotly.express as px
import math
import requests
import csv

def get_car_images(car_brands):
    car_images = {}
    for brand in car_brands:
        response = requests.get(f"https://source.unsplash.com/500x500/?{brand}")
        car_images[brand] = response.url
    return car_images

def main():

    df = pd.read_csv("final_cars_datasets.csv")
    
    # Loop through each row in the dataframe
    for index, row in df.iterrows():

        # Check the value in the third column of the row
        brand = row[2]

        # Get an image URL from Unsplash using the brand name
        response = requests.get(f"https://source.unsplash.com/500x500/?{brand}")

        # Replace the value in the 11th column of the row with the image URL
        df.at[index, 'image_url'] = response.url

    # Write the updated dataframe back to the CSV file
    df.to_csv('final_cars_datasets.csv', index=False)


def plotPerColumnDistribution(df, nGraphPerRow):
    """
    This function plots the distribution of each column in a pandas dataframe.
    
    :param df: The input dataframe that contains the data to be plotted
    :param nGraphShown: The number of columns to display in the plot
    :param nGraphPerRow: The number of graphs to display per row in the plot
    """
    nunique = df.nunique()
    #df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    if nCol % nGraphPerRow == 0:
        nGraphRow = nCol  / nGraphPerRow
    else:
        nGraphRow = math.ceil(nCol  / nGraphPerRow)
    nGraphRow = int(nGraphRow)
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(nCol):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    plt.show()
    
# Correlation matrix
def plotCorrelationMatrix(df, graphWidth):
    filename = df.dataframeName
    df = df.dropna('columns') # drop columns with NaN
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum = 1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix for {filename}', fontsize=15)
    plt.show()



if __name__ == "__main__":
    main()
