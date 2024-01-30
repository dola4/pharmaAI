import pandas as pd  
from sklearn.model_selection import train_test_split  
import streamlit as st  
from sklearn.preprocessing import StandardScaler, Normalizer, MinMaxScaler  
from sklearn.linear_model import LinearRegression  
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, median_absolute_error, r2_score 
from math import sqrt  
from sklearn.preprocessing import LabelEncoder, OneHotEncoder  





def train_model_for_drug(df, drug_name):
    df_single_drug = df[df[drug_name] == 1]
    
    X = df_single_drug.drop('Quantité', axis=1)
    Y = df_single_drug['Quantité']
    
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30, random_state=5)
    
    model = LinearRegression()
    
    model.fit(X_train, Y_train)
    
    return model



def predict_drug_needs(model, features):
    predicted_quantity = model.predict([features])[0]
    return predicted_quantity

def preprocess_df(df):
    labelencoder = LabelEncoder()
    df['Vendeur_encoded'] = labelencoder.fit_transform(df['Vendeur'])
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    df_daily = df.groupby(['Date', 'Médicament']).agg({'Quantité': 'sum'}).reset_index()
    
    df_daily['Prev_day_sales'] = df_daily.groupby('Médicament')['Quantité'].shift(1)
    
    df_daily['Prev_day_sales'].fillna(0, inplace=True)
    
    onehotencoder = OneHotEncoder(drop='first', sparse=False)
    onehot_cols = pd.DataFrame(onehotencoder.fit_transform(df_daily[['Médicament']]))
    onehot_cols.columns = onehotencoder.get_feature_names_out(['Médicament'])
    df_daily = pd.concat([df_daily, onehot_cols], axis=1)
    
    df_daily['Year'] = df_daily['Date'].dt.year
    df_daily['Month'] = df_daily['Date'].dt.month
    df_daily['Day'] = df_daily['Date'].dt.day
    
    df_daily.drop(['Date', 'Médicament'], axis=1, inplace=True)
    
    return df_daily


def ml_skLearn(df, target):
    df = preprocess_df(df)
    
    target = df['Quantité']

    st.subheader("Predictive Modelling")
    st.write("Choose a transform type and Model from the option below")

    task = "regression"
    
    X = df.values
    Y = target.values

    test_proportion = 0.30
    seed = 5

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_proportion, random_state=seed)
    
    transform_options = ["None", "StandardScaler", "Normalizer", "MinMaxScaler"]
    transform = st.selectbox("Select data transform", transform_options)
    
    if transform == "StandardScaler":
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
    elif transform == "Normalizer":
        scaler = Normalizer()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
    elif transform == "MinMaxScaler":
        scaler = MinMaxScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

    if task == "regression":
        model = LinearRegression()
        model.fit(X_train, Y_train)
        Y_pred = model.predict(X_test)

        evs = explained_variance_score(Y_test, Y_pred)
        meae = median_absolute_error(Y_test, Y_pred)
        mae = mean_absolute_error(Y_test, Y_pred)
        mse = mean_squared_error(Y_test, Y_pred)
        rmse = sqrt(mse)
        r2 = r2_score(Y_test, Y_pred)

        st.write("Voici les résultats d'une régression linéaire")
        st.write(f'Explained variance score : {evs}')
        st.write(f'median absolute error : {meae}')
        st.write(f'mean absolute error : {mae}')
        st.write(f'mean square error : {mse}')
        st.write(f'RMSE : {rmse}')
        st.write(f'R2 : {r2}')

    return model
