import streamlit as st
import pickle
import numpy as np

with open('all_priority_model.pkl', 'rb') as file:
    model = pickle.load(file)

def predict(input_data):
    # Convert the input_data dictionary to a 2D array-like format
    input_array = np.array(list(input_data.values())).reshape(1, -1)
    return model.predict(input_array)

def main():
    st.title("TICKET PRIORITY PREDICTION")

    # Create a 6-row, 2-column layout
    col1, col2 = st.columns(2)

    # First column (col1)
    with col1:
        ci_subcat = st.number_input("CI Subcat", value=0, key="CI_Subcat", step=1)
        wbs = st.number_input("WBS", value=0, key="WBS", step=1)
        status = st.selectbox("Status", options=[0, 1], index=0, key="Status")
        impact = st.selectbox("Impact", options=[1,2,3,4,5], index=0, key="Impact")
        number_cnt = st.number_input("number_cnt", value=0.0, key="number_cnt")

    # Second column (col2)
    with col2:
        category = st.selectbox("Category", options=[1,2,3,4,5], index=0, key="Category")
        kb_number = st.number_input("KB_number", value=0, key="KB_number", step=1)
        num_reassignments = st.number_input("No_of_Reassignments", value=0, key="No_of_Reassignments", step=1)
        num_related_interactions = st.number_input("No_of_Related_Interactions", value=0, key="No_of_Related_Interactions", step=1)
        handle_time_hrs_conv = st.number_input("Handle_Time_hrs_conv", value=0, key="Handle_Time_hrs_conv", step=1)

    if st.button("Predict"):
        # Convert form inputs to appropriate data types
        input_data = {
            "CI_Subcat": int(ci_subcat),
            "WBS": int(wbs),
            "Status": int(status),
            "Impact": int(impact),
            "number_cnt": float(number_cnt),
            "Category": int(category),
            "KB_number": int(kb_number),
            "No_of_Reassignments": int(num_reassignments),
            "No_of_Related_Interactions": int(num_related_interactions),
            "Handle_Time_hrs_conv": int(handle_time_hrs_conv),
        }

        prediction_result = predict(input_data)
        st.write("Prediction:", prediction_result)

if __name__ == '__main__':
    main()
