from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)


# Funkce pro logování v administračním rozhraní
log = []

def log_request(request):
    log.append(f"[{datetime.now()}] {request.method} {request.path} {request.base_url} {request.data}")
    if request.method == 'POST':
        log.append(f"Form data: {request.form}")

# Funkce pro načtení dat ze souboru
def load_data():
    try:
        with open('IMIS-Mobilni_Robot-Batch_Response___v03.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

# Funkce pro uložení dat do souboru
def save_data(data):
    with open('IMIS-Mobilni_Robot-Batch_Response___v03.json', 'w') as file:
        json.dump(data, file, indent=4)

def add_data(data):
    with open('IMIS-Mobilni_Robot-Batch_Response___v03.json', 'a') as file:
        json.dump(data, file, indent=4)

#GET pro administrační rozhraní
@app.route('/')
def index():
    obsah_souboru = load_data()
    data = list()
    for json in obsah_souboru:
        data.append(json)
    log_request(request)
    return render_template('index.html', data=data, log=log)

#GET pro volání robotem (vrací jenom soubor)
@app.route("/odvolavka",methods=["GET"])
def get_odvolavka_robot():
    if request.method == "GET":
        data = load_data()
        return data
    else:
        return None

#POST pro volání robotem (přepíše lokální soubor)
@app.route("/odvolavka",methods=["POST"])
def set_odvolavka_robot():
    if request.method == "POST" and request.data != None:
        data = request.json
        with open('IMIS-Mobilni_Robot-Batch_Response___v03.json', 'w') as file:
            json.dump(data, file, indent=4)
        return "Data zapsána do souboru"

#Přidání záznamu do souboru v administračním rozhraní
@app.route('/add', methods=['POST'])
def add_entry():
    data = load_data()
    entry = {
        'batch-id': request.form['batch-id'],
        'demand-id': request.form['demand-id'],
        'article-nr': request.form['article-nr'],
        'demand-state': request.form['demand-state'],
        'pack-id': request.form['pack-id'],
        'storage': request.form['storage'],
        'pack-quantity': request.form['pack-quantity'],
        'sequence-place-of-usage': request.form['sequence-place-of-usage'],
        'request-time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        'pick-time': request.form['pick-time'],
        'delivery-time': request.form['delivery-time']
    }
    data.append(entry)
    save_data(data)
    return redirect(url_for('index'))

#Smazání záznamu ze souboru v administračním rozhraní
@app.route('/delete/<int:index>')
def delete_entry(index):
    data = load_data()
    if 0 <= index < len(data):
        del data[index]
        save_data(data)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
