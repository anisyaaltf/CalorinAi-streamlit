import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt     

st.set_page_config(
    page_title="Dashboard Kalorin AI",
    page_icon=":bar_chart:",
    layout="wide"
    )
st.markdown("""
<style>
.main{
    background-color: #0E1117;
}
h1, h2, h3, h4{
    font-family: sans-serif;
}
.stButtonBox>button{
    border-radius:10px;
    height: 3em;
    width:100%
    background-color: #00C853;
    color: white;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)
df_main = pd.read_csv("df_main_final.csv")
df_bmi = pd.read_csv("df_bmi_final.csv")

st.sidebar.title("Kalorin AI Dashboard")

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
    st.markdown("""
    <h1 style='text-align: center; color: #6BE675; font-size:60px;'>
                Welcome to Kalorin AI Dashboard
                </h1>
                """, unsafe_allow_html=True)
    st.markdown("""
    <h4 style='text-align: center; color: #white;'>
                AI Based Nutrition & BMI Recommendation System  
                </h4>
                """, unsafe_allow_html=True)
    st.write("")
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        st.image(
        "kalorinLogo.png",
        width=250
    )
    st.write("")
    st.write("")
    left, center, right = st.columns([1, 6, 1])
    with center:
        col1, col2, col3 = st.columns(3)
    with col1:
        st.info("""BMI Calculator""")
    with col2:
        st.success("""EDA Visualization""")
    with col3:
        st.warning("""Food Recomendation""")

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
            min_value=100,
            max_value=250, 
            value=170
            )
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
    fig, ax = plt.subplots(figsize=(8,5))
    ax.hist(
        df_main['calories'],
        bins=20, 
    )
    ax.set_title("Calories Distribution")
    ax.set_xlabel('Calories')
    ax.set_ylabel('Frequency')
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Top High Protein Foods")
    # visual top protein
    top_protein = df_main.sort_values(
        by='proteins',
        ascending=False
        ).head(10)
    fig2, ax2 = plt.subplots(figsize=(8,5))
    ax2.barh(
        top_protein['name'].head(10),
        top_protein['proteins'].head(10),
    )
    ax2.set_title("Top High Protein Foods")
    ax2.set_xlabel('Protein (g)')
    plt.tight_layout()
    st.pyplot(fig2)

    # Visual fat vs calories
    st.subheader("Fat vs Calories")
    fig3, ax3 = plt.subplots(figsize=(8,5))
    ax3.scatter(
        df_main['calories'],
        df_main['fat'],
        alpha=0.7
    )
    ax3.set_title("Fat vs Calories")
    ax3.set_xlabel('Fat (g)')
    ax3.set_ylabel('Calories')
    plt.tight_layout()
    st.pyplot(fig3)
    # Visual BMI Category Distribution
    st.subheader("BMI Category Distribution")
    def kategori_bmi(bmi):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obesity"
    df_bmi['Kategori'] = df_bmi['BMI'].apply(kategori_bmi)
    fig4, ax4 = plt.subplots(figsize=(8,5))
    df_bmi['Kategori'].value_counts().plot(
        kind='bar',
        ax=ax4,
    )
    ax4.set_title("BMI Category Distribution")
    ax4.set_xlabel('BMI Category')
    ax4.set_ylabel('Count')
    plt.tight_layout()
    st.pyplot(fig4)

    # Visual Gender Distribution
    st.subheader("Gender Distribution")
    fig5, ax5 = plt.subplots(figsize=(8,5))
    df_bmi['gender'].value_counts().plot(
        kind='bar',
        ax=ax5,
    )
    ax5.set_title("Gender Distribution")
    ax5.set_xlabel('Gender')
    ax5.set_ylabel('Count')
    plt.tight_layout()
    st.pyplot(fig5)

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
                df_main["food_category"] == "High Protein"
                ]
        # normal
        elif bmi_input < 25:
            hasil = df_main[
                df_main["food_category"] == "Healthy"
                ]
        # overweight
        else:
            hasil = df_main[
                (df_main["food_category"] == "Low Carb") |
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