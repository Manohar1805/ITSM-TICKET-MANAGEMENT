import streamlit as st
import pickle
import numpy as np

with open('all_priority_model.pkl', 'rb') as file:
    model = pickle.load(file)

def predict(input_data):
    return model.predict([input_data])

def main():
    st.title("Your App Name")

    # Create a 6-row, 2-column layout
    col1, col2 = st.columns(2)

    # First column (col1)
    with col1:
        st.number_input("CI Subcat", value=0, key="CI_Subcat")
        st.number_input("WBS", value=0, key="WBS")
        st.number_input("Status", value=0, key="Status")
        st.number_input("Impact", value=0, key="Impact")
        st.number_input("number_cnt", value=0.0, key="number_cnt")
        
    # Second column (col2)
    with col2:
        st.number_input("Category", value=0, key="Category")
        st.number_input("KB_number", value=0, key="KB_number")
        st.number_input("No_of_Reassignments", value=0, key="No_of_Reassignments")
        st.number_input("No_of_Related_Interactions", value=0, key="No_of_Related_Interactions")
        st.number_input("Handle_Time_hrs_conv", value=0, key="Handle_Time_hrs_conv")

    if st.button("Predict"):
        # Retrieve the input data from the form fields
        input_data = {
            "CI_Subcat": st.session_state["CI_Subcat"],
            "WBS": st.session_state["WBS"],
            "Status": st.session_state["Status"],
            "Impact": st.session_state["Impact"],
            "number_cnt": st.session_state["number_cnt"],
            "Category": st.session_state["Category"],
            "KB_number": st.session_state["KB_number"],
            "No_of_Reassignments": st.session_state["No_of_Reassignments"],
            "No_of_Related_Interactions": st.session_state["No_of_Related_Interactions"],
            "Handle_Time_hrs_conv": st.session_state["Handle_Time_hrs_conv"],
        }
        prediction_result = predict(input_data)
        st.write("Prediction:", prediction_result)

if __name__ == '__main__':
    main()
