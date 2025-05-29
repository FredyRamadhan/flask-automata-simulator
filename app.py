from flask import Flask, render_template, redirect, request, url_for
from fitur_fitur.cek_equivalen import are_equivalent_dfas
from fitur_fitur.minimisasi_dfa import minimize_dfa
# from fitur_fitur.regex_to_nfa import 
from fitur_fitur.tes_dfa import run_dfa
from fitur_fitur.dfa_to_diagram import dfa_to_diagram
import ast
from pprint import pformat

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('beranda.html')

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
            result = dfa_to_diagram(minimized)

        except Exception as e:
            error = str(e)

    return render_template("minimisasi.html", result=result, error=error)

@app.route("/uji-dfa", methods=["GET", "POST"])
def tes_dfa_page():
    result = None
    diag = None
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
            diag = dfa_to_diagram(dfa)

            accepted, log = run_dfa(dfa, input_string)
            result = "Ya" if accepted else "Tidak"

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("uji_dfa.html", result=result, log=log, diag=diag)

# CEK EKUIVALENSI DFA

@app.route('/cek-ekuivalen', methods=["GET", "POST"])
def cek_ekuivalen():
    result = None
    diag = None
    diag2 = None
    if request.method == "POST":
        try:
            states = set(request.form["states"].replace(" ", "").split(","))
            alphabet = set(request.form["alphabet"].replace(" ", "").split(","))
            start_state = request.form["start_state"].strip()
            accept_states = set(request.form["accept_states"].replace(" ", "").split(","))
            tf_raw = request.form["transition_function"]
            
            states2 = set(request.form["states_2"].replace(" ", "").split(","))
            alphabet2 = set(request.form["alphabet_2"].replace(" ", "").split(","))
            start_state2 = request.form["start_state_2"].strip()
            accept_states2 = set(request.form["accept_states-2"].replace(" ", "").split(","))
            tf_raw2 = request.form["transition_function_2"]

            transition_function = ast.literal_eval(tf_raw)
            if not isinstance(transition_function, dict):
                raise ValueError("Transition function harus dictionary.")

            transition_function2 = ast.literal_eval(tf_raw2)
            if not isinstance(transition_function2, dict):
                raise ValueError("Transition function harus dictionary.")

            dfa = {
                'states': states,
                'alphabet': alphabet,
                'start_state': start_state,
                'accept_states': accept_states,
                'transition_function': transition_function
            }

            dfa2 = {
                'states': states2,
                'alphabet': alphabet2,
                'start_state': start_state2,
                'accept_states': accept_states2,
                'transition_function': transition_function2
            }
            result = are_equivalent_dfas(dfa, dfa2).upper()
            diag = dfa_to_diagram(dfa)
            diag2 = dfa_to_diagram(dfa2)
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("cek_ekuivalen.html", result=result, diag=diag, diag2=diag2)


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(f"404 Not Found: {request.url}")
    return render_template('404.html', error_message=error.description), 404

if __name__ == "__main__":
    app.run(debug=True)

