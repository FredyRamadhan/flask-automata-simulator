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



#Fungsi Inputan Minimsasi DFA
import ast
from minimisasi_dfa import minimize_dfa
from pprint import pprint

print("=== INPUT DFA UNTUK DIMINIMALKAN ===")
print("Masukkan semua bagian secara terpisah sesuai instruksi di bawah ini.")

print("\nContoh input:")
print("  States          : q0,q1,q2")
print("  Alphabet        : 0,1")
print("  Start State     : q0")
print("  Accept States   : q1")
print("  Transition Fn   : {('q0', '0'): 'q2', ('q0', '1'): 'q1', ('q1', '0'): 'q2', ('q1', '1'): 'q1', ('q2', '0'): 'q2', ('q2', '1'): 'q1'}")

states = set(input("\nStates (pisahkan dengan koma): ").replace(" ", "").split(","))
alphabet = set(input("Alphabet (pisahkan dengan koma): ").replace(" ", "").split(","))
start_state = input("Start State: ").strip()
accept_states = set(input("Accept States (pisahkan dengan koma): ").replace(" ", "").split(","))
tf_raw = input("Transition Function (format dictionary Python): ").strip()

try:
    transition_function = ast.literal_eval(tf_raw)
    if not isinstance(transition_function, dict):
        raise ValueError
except Exception:
    print("❌ Format transition_function salah. Pastikan menggunakan format dictionary Python.")
    exit(1)

dfa_input = {
    'states': states,
    'alphabet': alphabet,
    'start_state': start_state,
    'accept_states': accept_states,
    'transition_function': transition_function
}

minimized = minimize_dfa(dfa_input)

print("\n=== DFA HASIL MINIMISASI ===")
pprint(minimized)
