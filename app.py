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



