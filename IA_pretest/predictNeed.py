import pandas as pd
import numpy as np
import streamlit as st
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from torch.utils.data import DataLoader, TensorDataset



def predict_drug_need(model, scaler, le_sexe, le_status, le_drugName, le_sellDayOfWeek, le_sellDateIsweekend, le_sellDateIsHoliday, le_sellDateSeason, le_prescriptionGivenDayOfWeek, le_prescriptionGivenDateIsweekend, le_prescriptionGivenDateIsHoliday, le_prescriptionGivenDateSeason, le_prescriptionExpirationDayOfWeek, le_prescriptionExpirationDateIsweekend, le_prescriptionExpirationDateIsHoliday, le_prescriptionExpirationDateSeason, features):
    # Transformer les caractéristiques utilisateur
    transformed_features = np.array([
        features['id_vente'],
        features['id_client'],
        le_sexe.transform([features['sexe']])[0],
        features['age'],
        features['PrescriptionGivenNb'],
        features['PrescriptionMaxGiven'],
        le_status.transform([features['PrescriptionStatus']])[0],
        le_drugName.transform([features['DrugName']])[0],
        features['SellPrice'],
        features['BuyPrice'],

        le_sellDayOfWeek.transform([features['SellDayOfWeek']])[0],
        features['SellDayOfMonth'],
        features['SellMonth'],
        features['SellYear'],
        le_sellDateIsweekend.transform([features['SellDateIsWeekend']])[0],
        le_sellDateIsHoliday.transform([features['SellDateIsHoliday']])[0],
        le_sellDateSeason.transform([features['SellDateSeason']])[0],

        le_prescriptionGivenDayOfWeek.transform([features['PrescriptionGivenDayOfWeek']])[0],
        features['PrescriptionGivenDay'],
        features['PrescriptionGivenMonth'],
        features['PrescriptionGivenYear'],
        le_prescriptionGivenDateIsweekend.transform([features['PrescriptiongivenDateIsWeekend']])[0],   
        le_prescriptionGivenDateIsHoliday.transform([features['PrescriptiongivenDateIsHoliday']])[0],
        le_prescriptionGivenDateSeason.transform([features['PrescriptionGivenSeason']])[0],

        le_prescriptionExpirationDayOfWeek.transform([features['PrescriptionExpirationDayOfWeek']])[0],
        features['PrescriptionExpirationDay'],
        features['PrescriptionExpirationMonth'],
        features['PrescriptionExpirationYear'],
        le_prescriptionExpirationDateIsweekend.transform([features['PrescriptionExpirationDateIsWeekend']])[0],
        le_prescriptionExpirationDateIsHoliday.transform([features['PrescriptionExpirationDateIsHoliday']])[0],
        le_prescriptionExpirationDateSeason.transform([features['PrescriptionExpirationSeason']])[0],

        features['Profit'],
    ])

    # Reshape transformed_features en un tableau 2D
    transformed_features = transformed_features.reshape(1, -1)
    transformed_features = scaler.transform(transformed_features)
    
    
    # Prédiction avec PyTorch
    with torch.no_grad():
        output = model(torch.FloatTensor(transformed_features))
        
    return output.item()

def ml_drug_need():
    df = pd.read_csv('outputSQL.csv')

    le_sexe = LabelEncoder()
    le_status = LabelEncoder()
    le_drugName = LabelEncoder()

    le_sellDayOfWeek = LabelEncoder()
    le_sellDateIsweekend = LabelEncoder()
    le_sellDateIsHoliday = LabelEncoder()
    le_sellDateSeason = LabelEncoder()

    le_prescriptionGivenDayOfWeek = LabelEncoder()
    le_prescriptionGivenDateIsweekend = LabelEncoder()
    le_prescriptionGivenDateIsHoliday = LabelEncoder()
    le_prescriptionGivenDateSeason = LabelEncoder()

    le_prescriptionExpirationDayOfWeek = LabelEncoder()
    le_prescriptionExpirationDateIsweekend = LabelEncoder()
    le_prescriptionExpirationDateIsHoliday = LabelEncoder()
    le_prescriptionExpirationDateSeason = LabelEncoder()



    # Transformer les colonnes catégorielles en numériques
    df['sexe'] = le_sexe.fit_transform(df['sexe'])
    df['PrescriptionStatus'] = le_status.fit_transform(df['PrescriptionStatus'])
    df['DrugName'] = le_drugName.fit_transform(df['DrugName'])
    
    df['SellDayOfWeek'] = le_sellDayOfWeek.fit_transform(df['SellDayOfWeek'])
    df['SellDateIsWeekend'] = le_sellDateIsweekend.fit_transform(df['SellDateIsWeekend'])
    df['SellDateIsHoliday'] = le_sellDateIsHoliday.fit_transform(df['SellDateIsHoliday'])
    df['SellDateSeason'] = le_sellDateSeason.fit_transform(df['SellDateSeason'])

    df['PrescriptionGivenDayOfWeek'] = le_prescriptionGivenDayOfWeek.fit_transform(df['PrescriptionGivenDayOfWeek'])
    df['PrescriptiongivenDateIsWeekend'] = le_prescriptionGivenDateIsweekend.fit_transform(df['PrescriptiongivenDateIsWeekend'])
    df['PrescriptiongivenDateIsHoliday'] = le_prescriptionGivenDateIsHoliday.fit_transform(df['PrescriptiongivenDateIsHoliday'])
    df['PrescriptionGivenSeason'] = le_prescriptionGivenDateSeason.fit_transform(df['PrescriptionGivenSeason'])

    df['PrescriptionExpirationDayOfWeek'] = le_prescriptionExpirationDayOfWeek.fit_transform(df['PrescriptionExpirationDayOfWeek'])
    df['PrescriptionExpirationDateIsWeekend'] = le_prescriptionExpirationDateIsweekend.fit_transform(df['PrescriptionExpirationDateIsWeekend'])
    df['PrescriptionExpirationDateIsHoliday'] = le_prescriptionExpirationDateIsHoliday.fit_transform(df['PrescriptionExpirationDateIsHoliday'])
    df['PrescriptionExpirationSeason'] = le_prescriptionExpirationDateSeason.fit_transform(df['PrescriptionExpirationSeason'])

    # Choisir les caractéristiques et la cible
    features = df.drop(['SellDate', 'PrescriptionGivenDate', 'PrescriptionExpirationDate', 'PrescriptionGivenNb'], axis=1)
    target = df['PrescriptionGivenNb']

    # Normalisation
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # Diviser les données
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.fc1 = nn.Linear(features.shape[1], 64)
            self.fc2 = nn.Linear(64, 32)
            self.fc3 = nn.Linear(32, 1)

        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = torch.relu(self.fc2(x))
            x = self.fc3(x)
            return x
    
    # Initialisation
    model = Net()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # DataLoader
    train_data = TensorDataset(torch.FloatTensor(X_train), torch.FloatTensor(y_train.values.astype(float)))
    train_loader = DataLoader(dataset=train_data, batch_size=32, shuffle=True)

    # Boucle d'entraînement
    for epoch in range(50):
        for batch_idx, (data, target) in enumerate(train_loader):
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output.view(-1), target.view(-1))
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        X_test_tensor = torch.FloatTensor(X_test)
        y_test_tensor = torch.FloatTensor(y_test.values.astype(float))
        prediction = model(X_test_tensor).view(-1)
        mse = mean_squared_error(y_test, prediction.numpy())
        r2 = r2_score(y_test, prediction.numpy())

    return model, scaler, le_sexe, le_status, le_drugName, le_sellDayOfWeek, le_sellDateIsweekend, le_sellDateIsHoliday, le_sellDateSeason, le_prescriptionGivenDayOfWeek, le_prescriptionGivenDateIsweekend, le_prescriptionGivenDateIsHoliday, le_prescriptionGivenDateSeason, le_prescriptionExpirationDayOfWeek, le_prescriptionExpirationDateIsweekend, le_prescriptionExpirationDateIsHoliday, le_prescriptionExpirationDateSeason, mse, r2

