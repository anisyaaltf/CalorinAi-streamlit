import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt     

st.set_page_config(
                   page_title="Dashboard Kalorin AI",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )
df_main = pd.read_csv("df_bmi_final.csv")
df_bmi = pd.read_csv("df_main_final.csv")

menu = st.sidebar.selectbox(
    "Menu", 
    [
        "Home",
        "BMI Calculator", 
        "EDA Visualization", 
        "Food Recomendation"
    ]
    )
if menu == "Home":
    st.title("Welcome to Kalorin AI Dashboard")
    st.write("""Kalorin AI & BMI Recommendation System 
    fitur:
    - BMI Calculatpr
    - EDA Visualization
    - Food Recomendation
    """)
set.image(
        "https://cdn-icons-png.flaticon.com/512/1046/1046784.png",
        width=200
)
# BMI Calculator    
elif menu == "BMI Calculator":
    st.title("BMI Calculator")
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input(
            "Enter your weight (kg)", 
            min_value=20,
            max_value=300,
            value=60
            )
    with col2:
        height = st.number_input(
            "Enter your height (cm)",
            min_value=1000,
            max_value=250, 
            value=170)
    if st.button("Calculate BMI"):
        bmi = weight / ((height / 100) ** 2)
        st.success(f"Your BMI is: {bmi:.2f}")

        if bmi < 18.5:
            bmi_category = "Underweight"
        elif bmi < 25:
            bmi_category = "Normal"
        elif bmi < 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obesity"
        st.info(f"Category:{bmi_category}")

# Distribusi Kalori
elif menu == "EDA Visualization":
    st.title("EDA Visualization")
    st.subheader("Calories Distribution")
    fig, ax = plt.subplots()
    df_main['calories'].hist(ax=ax)
    ax.set_xlabel('Calories')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
    st.subheader("Top High Protein Foods")

    top_protein = df_main.sort_values(
        by='proteins',
        ascending=False
        ).head(10)
    fig2, ax2 = plt.subplots()

    ax2.barh(
        top_protein['name'],
        top_protein['proteins']
        )
    ax2.set_xlabel('Protein (g)')
    st.pyplot(fig2)

# Food Recomendation
elif menu == "Food Recomendation":
    st.title("Food Recomendation")
    bmi_input = st.number_input(
        "Enter your BMI",
        min_value=10.0,
        max_value=50.0,
        value=22.0
        )
    if st.button("Get Food Recommendations"):
        #Underweight
        if bmi_input < 18.5:
            hasil = df_main[
                df_main["food_category"] == "High Calorie"
                ]
        # normal
        elif bmi_input < 25:
            hasil = df_main[
                df_main["food_category"] == "Regular"
                ]
        # overweight
        else:
            hasil = df_main[
                df_main["food_category"] == "Low Carb" |
                (df_main["food_category"] == "Low sugar")
                ]
        st.dataframe(
            hasil[
                [
                    "name",
                    "calories",
                    "proteins",
                    "carbohydrate", 
                    "fat"
                    ]
                    ].head(10)
                    )