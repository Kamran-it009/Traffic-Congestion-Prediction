import joblib
from tensorflow.keras.models import load_model
from datetime import timedelta
from datetime import date
from random import uniform
import pandas as pd
import numpy as np


def get_df(state_from_index, state_to_index):
    today_date = date.today()
    end_date = today_date + timedelta(15)
    today_date, end_date = str(today_date), str(end_date)
    forecast_range = pd.date_range(start=today_date, end=end_date, freq='H')

    state_from = [state_from_index] * len(forecast_range)
    state_to = [state_to_index] * len(forecast_range)

    unseen_df = {
        'Date': forecast_range,
        'State_from': state_from,
        'State_to': state_to
    }

    df1 = pd.DataFrame(unseen_df)
    df1 = df1.set_index('Date')
    return df1


def normalize_predictions(predictions):
    pred = []
    for prediction in predictions:
        error = uniform(-5, 10)
        normalize_result = 0 if (prediction[0] - error) < 0 else int(prediction[0] - error)
        pred.append(normalize_result)
    return pred


def main(state_from_index, state_to_index):
    scaler_filename = "models/scaler.pkl"
    scaler = joblib.load(scaler_filename)
    lstm_model = load_model('models/my_model.h5')

    df1 = get_df(state_from_index, state_to_index)
    transform_df = scaler.transform(df1)
    reshaped_df = np.reshape(transform_df, (transform_df.shape[0], transform_df.shape[1], 1))
    predictions = lstm_model.predict(reshaped_df)
    predictions = normalize_predictions(predictions)

    df1['Traffic Jam'] = predictions

    df1.reset_index(inplace=True)
    df1 = df1.rename(columns={'index': 'Date'})

    df1 = df1[df1.Date.dt.hour >= 7]
    df1 = df1[df1.Date.dt.hour < 19]

    working_days = [0, 1, 2, 3, 4]
    df1['day'] = df1['Date'].dt.dayofweek
    df1 = df1[df1['day'].isin(working_days)]
    print(df1)

    df1['Time'] = df1['Date'].dt.time
    df1['Date'] = df1['Date'].dt.date
    df1 = df1[['Date', 'Time', 'Traffic Jam']]
    df1['Time'] = df1['Time'].astype(str)
    return df1


if __name__ == '__main__':
    main(0, 1)


