from flask import Flask, render_template
# from fitur_fitur.cek_equivalen import
# from fitur_fitur.minimisasi_dfa import 
# from fitur_fitur.regex_to_nfa import 
# from fitur_fitur.tes_dfa import 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')







if __name__ == "__main__":
    app.run(debug=True)


# app.py
from flask import Flask, render_template, request
import ast
from minimisasi_dfa import minimize_dfa
from pprint import pformat

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            states = set(request.form["states"].replace(" ", "").split(","))
            alphabet = set(request.form["alphabet"].replace(" ", "").split(","))
            start_state = request.form["start_state"].strip()
            accept_states = set(request.form["accept_states"].replace(" ", "").split(","))
            tf_raw = request.form["transition_function"]

            transition_function = ast.literal_eval(tf_raw)
            if not isinstance(transition_function, dict):
                raise ValueError("Transition function harus dictionary.")

            dfa = {
                "states": states,
                "alphabet": alphabet,
                "start_state": start_state,
                "accept_states": accept_states,
                "transition_function": transition_function
            }

            minimized = minimize_dfa(dfa)
            result = pformat(minimized)

        except Exception as e:
            error = str(e)

    return render_template("form.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)

