import streamlit as st
import numpy as np
import pickle
import os
from pathlib import Path

project_root = Path(__file__).parent  
model_path = project_root / 'best_model_bagging.pkl'
# Load the trained model
with open(model_path, 'rb') as f:
    model = pickle.load(f)


st.set_page_config(page_title="Loan Prediction App", layout="centered")

st.title("🏦 Loan Approval Prediction")
st.write("Enter applicant's information to check if the loan is likely to be approved.")

# User input
with st.container(height=520):
    st.header('Application Details')
    col1 , col2 = st.columns(2)
    with col1 :
        gender = st.selectbox("Gender", ["Male", "Female"])
        married = st.selectbox("Married", ["Yes", "No"])
        dependents = st.selectbox("Number of Dependents", ["0", "1", "2", "3+"])
        education = st.selectbox("Education Level", ["Graduate", "Not Graduate"])
        self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    with col2 :
        applicant_income = st.number_input("Applicant Income", min_value=0)
        coapplicant_income = st.number_input("Coapplicant Income", min_value=0.0)
        loan_amount = st.number_input("Loan Amount (in thousands)", min_value=0.0)
        loan_term = st.number_input("Loan Term (in months)", min_value=0.0)
        credit_history = st.selectbox("Credit History", [1.0, 0.0])
    

# Prediction logic
if st.button("Predict Loan Status"):

    # Convert categorical values to numerical
    gender = 1 if gender == "Male" else 0
    married = 1 if married == "Yes" else 0
    dependents = 4 if dependents == "3+" else int(dependents)
    education = 1 if education == "Graduate" else 0
    self_employed = 1 if self_employed == "Yes" else 0

    # Prepare input for prediction
    input_data = np.array([[
        gender, married, dependents, education, self_employed,
        applicant_income, coapplicant_income, loan_amount, loan_term,
        credit_history
    ]])

    # Make prediction
    prediction = model.predict(input_data)

    # Show result
    if prediction[0] == 1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Not Approved")

