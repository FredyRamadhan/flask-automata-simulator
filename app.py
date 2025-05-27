from flask import Flask, render_template, redirect, request, url_for
# from fitur_fitur.cek_equivalen import
from fitur_fitur.minimisasi_dfa import minimize_dfa
# from fitur_fitur.regex_to_nfa import 
from fitur_fitur.tes_dfa import run_dfa
import ast
from pprint import pformat

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('beranda.html')

# @app.route("/submit-form", methods=["POST"])
# def submit_form():
#     selected_option = request.form.get("selected_option")
#     if selected_option:
#         # Redirect ke route sesuai pilihan di dropdown
#         return redirect(selected_option)
#     return redirect(url_for('home'))

@app.route("/minimisasi", methods=["GET", "POST"])
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

    return render_template("minimisasi.html", result=result, error=error)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route("/uji-dfa", methods=["GET", "POST"])
def tes_dfa_page():
    result = None
    log = []

    if request.method == "POST":
        try:
            # Ambil data dari form
            states = set(request.form["states"].replace(" ", "").split(","))
            alphabet = set(request.form["alphabet"].replace(" ", "").split(","))
            start_state = request.form["start_state"].strip()
            accept_states = set(request.form["accept_states"].replace(" ", "").split(","))
            tf_raw = request.form["transition_function"]
            input_string = request.form["input_string"]

            # Parse transition_function
            transition_function = ast.literal_eval(tf_raw)
            if not isinstance(transition_function, dict):
                raise ValueError("Transition function harus dictionary.")

            # Bentuk DFA
            dfa = {
                'states': states,
                'alphabet': alphabet,
                'start_state': start_state,
                'accept_states': accept_states,
                'transition_function': transition_function
            }

            accepted, log = run_dfa(dfa, input_string)
            result = "True" if accepted else "False"

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("uji_dfa.html", result=result, log=log)



@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(f"404 Not Found: {request.url}")
    return render_template('404.html', error_message=error.description), 404

if __name__ == "__main__":
    app.run(debug=True)

