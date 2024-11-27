from flask import Flask, render_template, request, redirect, url_for, flash, session
import os, waitress, requests, json, sqlite3

app = Flask(__name__)

api_service_url = os.environ.get("API_SERVICE_URL", "http://api:5000")
URL_EXO = api_service_url + "/"

# Créez 4 endpoints basés sur base.j2 pour consulter la bibliothèque : accueil, emprunts, livres et resultats

@app.route('/')
def accueil():
    return render_template('accueil.j2')

@app.route('/emprunts')
def emprunts():
    return render_template('emprunts.j2')

@app.route('/livres', methods=['GET', 'POST'])
def livres():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
    
        résultats = requests.get(URL_EXO + 'livres', params={'keyword': keyword}).json()
        return render_template('livres.j2', keyword=keyword, résultats=résultats)
    else:
        return render_template('livres.j2')

@app.route('/resultats')
def resultats():
    résultats = []
    return render_template('resultats.j2', résultats=résultats)

# Configuration de waitress pour le serveur de production
waitress.serve(app, host='127.0.0.1', port=5000)
