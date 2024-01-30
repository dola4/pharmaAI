
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from sklearn.preprocessing import OneHotEncoder


def get_high_correlations(df, threshold=0.8):
    # Calcul de la matrice de corrélation
    corr_matrix = df.corr()

    # Initialisation d'une liste pour stocker les paires de corrélations élevées
    high_corr_list = []

    # Parcourir la matrice de corrélation
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > threshold:
                high_corr_list.append({
                    'Feature 1': corr_matrix.columns[i],
                    'Feature 2': corr_matrix.columns[j],
                    'Correlation': corr_matrix.iloc[i, j]
                })

    # Créer un DataFrame à partir de la liste
    high_corr = pd.DataFrame(high_corr_list)
    return high_corr




def encode_categorical_columns(df):
    encoder = OneHotEncoder(sparse=False)
    categorical_columns = df.select_dtypes(include=['object']).columns
    encoded_data = encoder.fit_transform(df[categorical_columns])
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_columns))
    return pd.concat([df.drop(categorical_columns, axis=1), encoded_df], axis=1)



def eda(df, feature_names, target):
    st.subheader("Exploratory Data Analysis and Visualization")

    st.write("Choose a plot type from the options below")

    if st.checkbox("Show raw data"):
        st.write(df)

    if st.checkbox("Show missing values"):
        st.write(df.isna().sum())

    if st.checkbox("Show Data types"):
        st.write(df.dtypes)

    if st.checkbox("Show descriptive statistics"):
        st.write(df.describe())
        print(f'descriptive statistics : {df.describe()}')



    if st.checkbox("Show correlation Matrix including Categorical Attributes"):
        #df_encoded = encode_categorical_columns(df)
        corr = df.corr()
        print(get_high_correlations(df, threshold=0.015))
        st.write(get_high_correlations(df, threshold=0.015))
        plt.figure(figsize=(60, 60))  
        mask = np.triu(np.ones_like(corr, dtype=bool))
    
        sns.heatmap(corr, mask=mask, annot=True, cmap="coolwarm", annot_kws={"size": 40}) 

        plt.xticks(rotation=90, fontsize=70)  
        plt.yticks(rotation=0, fontsize=70)  

        #st.pyplot()


    if st.checkbox("Show histogram for each attribute"):
        for col in df.columns:
            if df[col].dtype == 'bool':
                # Traiter les colonnes booléennes séparément
                fig, ax = plt.subplots()
                ax.bar(['True', 'False'], [df[col].sum(), len(df) - df[col].sum()])
                ax.set_title(col)
                st.pyplot(fig)
            else:
                fig, ax = plt.subplots()
                ax.hist(df[col], bins=20, density=True, alpha=0.5)
                ax.set_title(col)
                st.pyplot(fig)

    if st.checkbox("Show Density for each attribute"):
        for col in df.select_dtypes(include=[np.number]).columns:
            fig, ax = plt.subplots()        
            sns.kdeplot(df[col], fill=True)
            ax.set_title(col)        
            st.pyplot(fig)

        if st.checkbox("Show Scatter plot"):
            fig = px.scatter(df, x=feature_names[0], y=feature_names[1], color=target)
            st.plotly_chart(fig)

    

