# Import required libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from joblib import dump


def main():
    # Load the car data into a Pandas dataframe
    dataframe = pd.read_csv('final_cars_datasets.csv')

    # Select only numerical input features for the model
    numerical_features = ['year', 'mileage', 'engine_capacity']
    car_data = dataframe[numerical_features + ['price']]

    # Split the data into training and testing sets
    X = car_data.drop('price', axis=1)
    y = car_data['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the linear regression model on the training set
    model = LinearRegression()
    model.fit(X_train, y_train)

    dump(model, './pet/saveModels/model.joblib')

    # Evaluate the model on the testing set
    #score = model.score(X_test, y_test)
    #print("R-squared score:", score)

    # Use the model to make predictions on new data
    #new_car_data = np.array([2015, 10000, 1500]).reshape(1, -1)
    #predicted_price = model.predict(new_car_data)
    #print("Predicted price:", round(predicted_price[0],0))

if __name__ == "__main__":
    main()