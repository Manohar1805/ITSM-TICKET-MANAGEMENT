from flask import Flask,render_template,request
import pickle
import sklearn
import pickle
import numpy as np


app=Flask(__name__)

with open('all_priority_model.pkl','rb') as file:
    model=pickle.load(file)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':
      # Convert form input data to appropriate data types
        # CI_cat = int(request.form.get('CI_cat'))
        CI_Subcat = int(request.form.get('CI_Subcat'))
        WBS = int(request.form.get('WBS'))
        Status = int(request.form.get('Status'))
        Impact = int(request.form.get('Impact'))
        number_cnt = float(request.form.get('number_cnt'))
        Category = int(request.form.get('Category'))
        KB_number = int(request.form.get('KB_number'))
        No_of_Reassignments = int(request.form.get('No_of_Reassignments'))
        No_of_Related_Interactions = int(request.form.get('No_of_Related_Interactions'))
        Handle_Time_hrs_conv = int(request.form.get('Handle_Time_hrs_conv'))
        
        input_data = [
            CI_Subcat, WBS, Status, Impact, number_cnt,
            Category, KB_number, No_of_Reassignments, No_of_Related_Interactions,
            Handle_Time_hrs_conv
        ]

        # Make the prediction using your model
        prediction_result = model.predict([input_data])  # Assuming 'model' is defined and loaded

        # Render the same HTML template with the prediction result
        return render_template('index.html', prediction_result=prediction_result)

    # If the request method is GET (initial page load), render the form template without prediction result
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

