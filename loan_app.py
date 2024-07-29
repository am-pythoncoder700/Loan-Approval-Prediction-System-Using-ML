from flask import Flask, request, render_template
import joblib
import numpy as np
# from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predictnow", methods=["GET", "POST"])
def predictnow():
    if request.method == "GET":
        return render_template("predictnow.html")
    else:
        try:
            coapplicant = float(request.form["coapplicantIncome"])
            applicant = float(request.form["applicantIncome"])
            loan_amt = float(request.form["loanAmount"])
            credit_history = float(request.form["creditHistory"])
            education = int(request.form["education"])

            if coapplicant >= 0 and applicant >= 0 and loan_amt >= 0 and credit_history >= 0 and education >= 0:
                # Creating a 2D numpy array of input data
                input_data = np.array([[coapplicant, applicant, loan_amt, credit_history, education]])

                # Loading the model
                model = joblib.load(r"loan_approval/model_loan")  # Ensure the path is correct and accessible

                # Predicting the output
                prediction = model.predict(input_data)

                return render_template("predict.html", predict=prediction[0])
            else:
                return "<h1><center>You have entered invalid information</center></h1>"
        except ValueError:
            return "<h1><center>Invalid input. Please enter valid numbers.</center></h1>"
        except Exception as e:
            return f"<h1><center>An error occurred: {e}</center></h1>"

@app.route("/predict", methods=["GET"])
def predict():
    return render_template("predict.html")

if __name__ == "__main__":
    app.run(debug=True)