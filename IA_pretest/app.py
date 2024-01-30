import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import streamlit as st
import plotly.express as px
from pandas.tseries.holiday import USFederalHolidayCalendar
import calendar
import time 


from eda import eda
from predictProfit import ml_profit, predict_profit
from predictNeed import predict_drug_need, ml_drug_need
from models.drug import Drug

st.set_option('deprecation.showPyplotGlobalUse', False)

dfSQL = pd.read_csv('outputSQL.csv')

feature_names = [
    'id_vente',
    'id_client',
    'sexe',
    'age',
    'SellDate',
    'PrescriptionGivenDate',
    'PrescriptionExpirationDate',
    'PrescriptionGivenNb',
    'PrescriptionMaxGiven',
    'PrescriptionStatus',
    'DrugName',
    'SellPrice',
    'BuyPrice',
    'SellDayOfWeek',
    'SellDayOfMonth',
    'SellMonth',
    'SellYear',
    'SellDateIsWeekend',
    'SellDateIsHoliday',
    'SellDateSeason',
    'PrescriptionGivenDayOfWeek',
    'PrescriptionGivenDay',
    'PrescriptionGivenMonth',
    'PrescriptionGivenYear',
    'PrescriptiongivenDateIsWeekend',
    'PrescriptiongivenDateIsHoliday',
    'PrescriptionGivenSeason',
    'PrescriptionExpirationDayOfWeek',
    'PrescriptionExpirationDay',
    'PrescriptionExpirationMonth',
    'PrescriptionExpirationYear',
    'PrescriptionExpirationDateIsWeekend',
    'PrescriptionExpirationDateIsHoliday',
    'PrescriptionExpirationSeason',
    'Profit',
    ]

target_name = 'Profit'

target = dfSQL[target_name]

st.set_page_config(
    page_title="Dashboard d'analyse des données et de modélisation prédictive pour une pharmacie",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("Dashboard d'analyse des données et de modélisation prédictive pour une pharmacie")

option = [
    "Ajout de données",
    "Analyse exploratoire des données (EDA)",
    "Prediction pour une journee",
    ]

selected_option = st.sidebar.selectbox("Choisir une option", option)

if selected_option == "Ajout de données":
    pass
    #add_data()

elif selected_option == "Analyse exploratoire des données (EDA)":
    eda(dfSQL, feature_names, target)
         

elif selected_option == "Prediction pour une journee":

    predict_option = ["Prédiction de profit", "Prédiction de stock nécessaire"]
    prediction_option = st.selectbox('Choisir une option', predict_option)

    if prediction_option == "Prédiction de profit":

        start_time = time.time()
        profit_model, profit_scaler, le_sexe, le_status, le_drugName, le_sellDayOfWeek, le_sellDateIsweekend, le_sellDateIsHoliday, le_sellDateSeason, le_prescriptionGivenDayOfWeek, le_prescriptionGivenDateIsweekend, le_prescriptionGivenDateIsHoliday, le_prescriptionGivenDateSeason, le_prescriptionExpirationDayOfWeek, le_prescriptionExpirationDateIsweekend, le_prescriptionExpirationDateIsHoliday, le_prescriptionExpirationDateSeason, mse, r2 = ml_drug_need()
        ml_profit_time = time.time() - start_time
        st.subheader("Prédiction des profit generés pour une journée")

        min_date = datetime.today()
        selected_date = st.date_input("Choisir une date", min_value=min_date)
        day_of_week = selected_date.weekday()
        if day_of_week == 0:
            day_of_week = "Sunday"
        elif day_of_week == 1:
            day_of_week = "Monday"
        elif day_of_week == 2:
            day_of_week = "Tuesday"
        elif day_of_week == 3:
            day_of_week = "Wednesday"
        elif day_of_week == 4:
            day_of_week = "Thursday"
        elif day_of_week == 5:
            day_of_week = "Friday"
        elif day_of_week == 6:
            day_of_week = "Saturday"
        
        day_of_month = selected_date.day
        year = selected_date.year
        month = selected_date.month
        if month in [1, 2, 12]:
            season = 'Winter'
        elif month in [3, 4, 5]:
            season = 'Spring'
        elif month in [6, 7, 8]:
            season = 'Summer'
        else:  # 9, 10, 11
            season = 'Fall'
        cal = USFederalHolidayCalendar()
        holidays = cal.holidays(start=min_date, end=selected_date)
        is_holiday = selected_date in holidays

        unique_drugs = sorted(dfSQL['DrugName'].unique())

        result_profit_dfSQL = pd.DataFrame(columns=['Drug Name', 'Profit Prediction'])
    
        features_profit_list = []
        total_predicted_profit = 0
        for drug_profit in unique_drugs:
            drug_data = dfSQL[dfSQL['DrugName'] == drug_profit].iloc[0]
            features_profit = {
                'id_vente' : dfSQL[dfSQL['DrugName'] == drug_profit]['id_vente'].iloc[0],
                'id_client': dfSQL[dfSQL['DrugName'] == drug_profit]['id_client'].iloc[0],
                'sexe': dfSQL[dfSQL['DrugName'] == drug_profit]['sexe'].iloc[0],
                'age': dfSQL[dfSQL['DrugName'] == drug_profit]['age'].iloc[0],
                'PrescriptionGivenNb': drug_data['PrescriptionGivenNb'],
                'PrescriptionMaxGiven': drug_data['PrescriptionMaxGiven'],
                'PrescriptionStatus': drug_data['PrescriptionStatus'],
                'DrugName': drug_data['DrugName'],
                'SellPrice': drug_data['SellPrice'],
                'BuyPrice': drug_data['BuyPrice'],

                'SellDayOfWeek': day_of_week,
                'SellDayOfMonth': day_of_month,
                'SellMonth': month,
                'SellYear': year,
                'SellDateIsWeekend': day_of_week in ['Sunday', 'Saturday'],
                'SellDateIsHoliday': is_holiday,
                'SellDateSeason': season, 

                'PrescriptionGivenDayOfWeek': drug_data['PrescriptionGivenDayOfWeek'],
                'PrescriptionGivenDay': drug_data['PrescriptionGivenDay'],
                'PrescriptionGivenMonth': drug_data['PrescriptionGivenMonth'],
                'PrescriptionGivenYear': drug_data['PrescriptionGivenYear'],
                'PrescriptiongivenDateIsWeekend': drug_data['PrescriptiongivenDateIsWeekend'],
                'PrescriptiongivenDateIsHoliday': drug_data['PrescriptiongivenDateIsHoliday'],
                'PrescriptionGivenSeason': drug_data['PrescriptionGivenSeason'],

                'PrescriptionExpirationDayOfWeek': drug_data['PrescriptionExpirationDayOfWeek'],
                'PrescriptionExpirationDay': drug_data['PrescriptionExpirationDay'],
                'PrescriptionExpirationMonth': drug_data['PrescriptionExpirationMonth'],
                'PrescriptionExpirationYear': drug_data['PrescriptionExpirationYear'],
                'PrescriptionExpirationDateIsWeekend': drug_data['PrescriptionExpirationDateIsWeekend'],
                'PrescriptionExpirationDateIsHoliday': drug_data['PrescriptionExpirationDateIsHoliday'],
                'PrescriptionExpirationSeason': drug_data['PrescriptionExpirationSeason'],
            }
            print(f"features _profit : {features_profit}")
            profit_prediction = predict_drug_need(profit_model,
                                                profit_scaler,
                                                le_sexe,
                                                le_status,
                                                le_drugName,
                                                le_sellDayOfWeek,
                                                le_sellDateIsweekend,
                                                le_sellDateIsHoliday,
                                                le_sellDateSeason,
                                                le_prescriptionGivenDayOfWeek,
                                                le_prescriptionGivenDateIsweekend,
                                                le_prescriptionGivenDateIsHoliday,
                                                le_prescriptionGivenDateSeason,
                                                le_prescriptionExpirationDayOfWeek,
                                                le_prescriptionExpirationDateIsweekend,
                                                le_prescriptionExpirationDateIsHoliday,
                                                le_prescriptionExpirationDateSeason,
                                                features_profit
                                                )
        
            total_predicted_profit += profit_prediction

        
            result_profit_dfSQL = result_profit_dfSQL.append({
                'Drug Name': drug_profit,
                'Profit Prediction': str(int(round(profit_prediction, 2))) + ' $',
            }, ignore_index=True)

        end_time = time.time()
        total_duration = end_time - start_time
        st.write(f'Temps de traitement pour la prédiction des profits : {ml_profit_time:.2f} secondes')
        st.write(f'duree total : {total_duration:.2f} secondes')
        st.write(f'Erreur Quadratique Moyenne pour la prédiction des profits : {mse}')
        st.write(f'Coefficient de Détermination pour la prédiction des profits : {r2}')
        st.write(f'Total des profits prédits : {total_predicted_profit:.2f} $')
        st.table(result_profit_dfSQL)
    
    elif prediction_option == "Prédiction de stock nécessaire":

        start_time = time.time()
        profit_model, profit_scaler, le_sexe, le_status, le_drugName, le_sellDayOfWeek, le_sellDateIsweekend, le_sellDateIsHoliday, le_sellDateSeason, le_prescriptionGivenDayOfWeek, le_prescriptionGivenDateIsweekend, le_prescriptionGivenDateIsHoliday, le_prescriptionGivenDateSeason, le_prescriptionExpirationDayOfWeek, le_prescriptionExpirationDateIsweekend, le_prescriptionExpirationDateIsHoliday, le_prescriptionExpirationDateSeason, mse, r2 = ml_profit()
        ml_profit_time = time.time() - start_time
        st.subheader("Prédiction des besoin en médicaments pour une journée")

        min_date = datetime.today()
        selected_date = st.date_input("Choisir une date", min_value=min_date)
        day_of_week = selected_date.weekday()
        if day_of_week == 0:
            day_of_week = "Sunday"
        elif day_of_week == 1:
            day_of_week = "Monday"
        elif day_of_week == 2:
            day_of_week = "Tuesday"
        elif day_of_week == 3:
            day_of_week = "Wednesday"
        elif day_of_week == 4:
            day_of_week = "Thursday"
        elif day_of_week == 5:
            day_of_week = "Friday"
        elif day_of_week == 6:
            day_of_week = "Saturday"
        
        day_of_month = selected_date.day
        year = selected_date.year
        month = selected_date.month
        if month in [1, 2, 12]:
            season = 'Winter'
        elif month in [3, 4, 5]:
            season = 'Spring'
        elif month in [6, 7, 8]:
            season = 'Summer'
        else:  # 9, 10, 11
            season = 'Fall'
        cal = USFederalHolidayCalendar()
        holidays = cal.holidays(start=min_date, end=selected_date)
        is_holiday = selected_date in holidays

        unique_drugs = sorted(dfSQL['DrugName'].unique())

        result_profit_dfSQL = pd.DataFrame(columns=['Drug Name', 'Quantite nessessaire', 'Quantite en stock'])
    
        features_profit_list = []
        total_predicted_profit = 0
        for drug_profit in unique_drugs:
            drug_data = dfSQL[dfSQL['DrugName'] == drug_profit].iloc[0]
            features_profit = {
                'id_vente' : dfSQL[dfSQL['DrugName'] == drug_profit]['id_vente'].iloc[0],
                'id_client': dfSQL[dfSQL['DrugName'] == drug_profit]['id_client'].iloc[0],
                'sexe': dfSQL[dfSQL['DrugName'] == drug_profit]['sexe'].iloc[0],
                'age': dfSQL[dfSQL['DrugName'] == drug_profit]['age'].iloc[0],
                'PrescriptionGivenNb': drug_data['PrescriptionGivenNb'],
                'PrescriptionMaxGiven': drug_data['PrescriptionMaxGiven'],
                'PrescriptionStatus': drug_data['PrescriptionStatus'],
                'DrugName': drug_data['DrugName'],
                'SellPrice': drug_data['SellPrice'],
                'BuyPrice': drug_data['BuyPrice'],

                'SellDayOfWeek': day_of_week,
                'SellDayOfMonth': day_of_month,
                'SellMonth': month,
                'SellYear': year,
                'SellDateIsWeekend': day_of_week in ['Sunday', 'Saturday'],
                'SellDateIsHoliday': is_holiday,
                'SellDateSeason': season, 

                'PrescriptionGivenDayOfWeek': drug_data['PrescriptionGivenDayOfWeek'],
                'PrescriptionGivenDay': drug_data['PrescriptionGivenDay'],
                'PrescriptionGivenMonth': drug_data['PrescriptionGivenMonth'],
                'PrescriptionGivenYear': drug_data['PrescriptionGivenYear'],
                'PrescriptiongivenDateIsWeekend': drug_data['PrescriptiongivenDateIsWeekend'],
                'PrescriptiongivenDateIsHoliday': drug_data['PrescriptiongivenDateIsHoliday'],
                'PrescriptionGivenSeason': drug_data['PrescriptionGivenSeason'],

                'PrescriptionExpirationDayOfWeek': drug_data['PrescriptionExpirationDayOfWeek'],
                'PrescriptionExpirationDay': drug_data['PrescriptionExpirationDay'],
                'PrescriptionExpirationMonth': drug_data['PrescriptionExpirationMonth'],
                'PrescriptionExpirationYear': drug_data['PrescriptionExpirationYear'],
                'PrescriptionExpirationDateIsWeekend': drug_data['PrescriptionExpirationDateIsWeekend'],
                'PrescriptionExpirationDateIsHoliday': drug_data['PrescriptionExpirationDateIsHoliday'],
                'PrescriptionExpirationSeason': drug_data['PrescriptionExpirationSeason'],

                'Profit': dfSQL[dfSQL['DrugName'] == drug_profit]['Profit'].iloc[0],
            }
            print(f"features_profit : {features_profit}")
            profit_prediction = predict_profit(profit_model,
                                                profit_scaler,
                                                le_sexe,
                                                le_status,
                                                le_drugName,
                                                le_sellDayOfWeek,
                                                le_sellDateIsweekend,
                                                le_sellDateIsHoliday,
                                                le_sellDateSeason,
                                                le_prescriptionGivenDayOfWeek,
                                                le_prescriptionGivenDateIsweekend,
                                                le_prescriptionGivenDateIsHoliday,
                                                le_prescriptionGivenDateSeason,
                                                le_prescriptionExpirationDayOfWeek,
                                                le_prescriptionExpirationDateIsweekend,
                                                le_prescriptionExpirationDateIsHoliday,
                                                le_prescriptionExpirationDateSeason,
                                                features_profit
                                                )
        
            total_predicted_profit += profit_prediction

        
            result_profit_dfSQL = result_profit_dfSQL.append({
                'Drug Name': drug_profit,
                'Quantite nessessaire': str(int(round(profit_prediction))) + ' Units',
                 'Quantite en stock': Drug.get_drug_by_name(drug_profit).stock + ' Units'
            }, ignore_index=True)

        end_time = time.time()
        total_duration = end_time - start_time

        

        st.write(f'Temps de traitement pour la prédiction des stocks: {ml_profit_time:.2f} secondes')
        st.write(f'duree total : {total_duration:.2f} secondes')
        st.write(f'Erreur Quadratique Moyenne pour la prédiction des stocks : {mse}')
        st.write(f'Coefficient de Détermination pour la prédiction des stocks : {r2}')
        st.write(f'Total des stocks prédits : {round(total_predicted_profit)} Units')
        st.table(result_profit_dfSQL)
