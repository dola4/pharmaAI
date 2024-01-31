import streamlit as st
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from datetime import datetime, timedelta
from .database.mongoDB import obtenir_info_medicaments, recuperer_medicaments


def add_data():
    existing_csv = "donnees_pharmacie_enrichies.csv"

    add_options = ["Choisi une option", "Ajouter une transaction", "Ajouter plusieurs transactions"]
    selected_option = st.selectbox("Choisir une option", add_options)

    if selected_option == "Ajouter une transaction":

        medicaments_options, prix_medicaments = obtenir_info_medicaments()
        date = st.date_input("Date de la transaction : ")
        date_str = date.strftime('%Y-%m-%d') 
        medicament = st.selectbox("Choisir un Médicament : ", medicaments_options)
        medicament_info = next((item for item in recuperer_medicaments() if item["nom"] == medicament), None)
        stock_max = medicament_info['stock'] if medicament_info else 0

        unit = st.number_input("Quantité voulue : ", min_value=1, max_value=stock_max)

        
        
        # Déterminer si la date est un jour férié
        cal = USFederalHolidayCalendar()
        holidays = cal.holidays(start=date, end=date)
        is_holiday = len(holidays) > 0
        unit_price = prix_medicaments[medicament]
        st.write("Prix unitaire : ", unit_price)
        total_price = unit * unit_price
        st.write("prix total : ", total_price)
        # Déterminer si la date est un weekend
        day_of_week = date.weekday() 
        day_of_month = date.day
        month = date.month
        # Saison
        if month in [12, 1, 2]:
            saison = "Hiver"
        elif month in [3, 4, 5]:
            saison = "Printemps"
        elif month in [6, 7, 8]:
            saison = "Été"
        else:
            saison = "Automne"
        if is_holiday == date in holidays :
            is_holiday = True
        else:
            is_holiday = False

        if day_of_week in [5, 6]:
            is_weekend = True
        else:
            is_weekend = False

        prix_quantite_ratio = round(unit_price / unit, 2)


        if (st.button("Ajouter", key="btn_add_one")):
            df_existing = pd.read_csv(existing_csv)

            # Ajouter une nouvelle ligne
            new_row = {
                'Date': date_str,
                'Medicament': medicament,
                'Quantite': unit,
                'PrixUnitaire': unit_price,
                'Total': total_price,
                'DayOfWeek': day_of_week,
                'DayOfMonth': day_of_month,
                'Month': month,
                'Saison': saison,
                'IsHoliday': is_holiday,
                'IsWeekend': is_weekend,
                'PrixQuantiteRatio': prix_quantite_ratio,
                }

            df_existing = df_existing.append(new_row, ignore_index=True)


            st.success("Transaction ajoutée avec succès")

    elif selected_option == "Ajouter plusieurs transactions":
        csv_file = st.file_uploader("Choisir un fichier CSV", type="csv")

        if st.button("Ajouter", key="btn_add_multiple"):
            if csv_file:
                df_new_data = pd.read_csv(csv_file)
                df_existing = pd.read_csv(existing_csv)
        
                # Concaténer les nouveaux et anciens DataFrames
                df_existing = pd.concat([df_existing, df_new_data], ignore_index=True)

                # Sauvegarder le DataFrame modifié
                df_existing.to_csv(existing_csv, index=False)
                st.success("Transactions ajoutées avec succès")
