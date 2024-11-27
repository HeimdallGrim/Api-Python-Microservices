from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import uvicorn, nest_asyncio

app = FastAPI()

def connect_db():
    return sqlite3.connect('database.db')

# Modèle Pydantic pour la création d'un livre
class LivreCreate(BaseModel):
    titre: str
    pitch: str
    auteur: str
    date_public: str

# Modèle Pydantic pour la création d'un utilisateur
class UtilisateurCreate(BaseModel):
    nom: str
    email: str

# Endpoint pour obtenir la liste complète des utilisateurs
@app.get('/utilisateurs', response_model=list)
async def get_utilisateurs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nom_utilisateur, email_utilisateur FROM utilisateurs')
    utilisateurs = cursor.fetchall()
    conn.close()
    return [{'id': u[0], 'nom': u[1], 'email': u[2]} for u in utilisateurs]

# Endpoint pour obtenir la liste complète des livres
@app.get('/livres', response_model=list)
async def get_livres():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, titre, pitch, auteur_id, date_public FROM livres')
    livres = cursor.fetchall()
    conn.close()
    return [{'id': l[0], 'titre': l[1], 'pitch': l[2], 'auteur_id': l[3], 'date_public': l[4]} for l in livres]

# Endpoint pour obtenir les détails d'un utilisateur par ID ou nom
@app.get('/utilisateur/{utilisateur}', response_model=dict)
async def get_utilisateur(utilisateur: str = Path(..., description="ID ou nom de l'utilisateur")):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        utilisateur_id = int(utilisateur)
        cursor.execute('SELECT id, nom_utilisateur, email_utilisateur FROM utilisateurs WHERE id = ?', (utilisateur_id,))
    except ValueError:
        cursor.execute('SELECT id, nom_utilisateur, email_utilisateur FROM utilisateurs WHERE nom_utilisateur = ?', (utilisateur,))

    result = cursor.fetchone()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {'id': result[0], 'nom': result[1], 'email': result[2]}

# Endpoint pour ajouter un livre
@app.post('/livres/ajouter', response_model=dict)
async def ajouter_livre(livre: LivreCreate):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM auteurs WHERE nom_auteur = ?', (livre.auteur,))
    auteur_result = cursor.fetchone()

    if not auteur_result:
        cursor.execute('INSERT INTO auteurs (nom_auteur) VALUES (?)', (livre.auteur,))
        auteur_id = cursor.lastrowid
    else:
        auteur_id = auteur_result[0]

    cursor.execute('INSERT INTO livres (titre, pitch, auteur_id, date_public) VALUES (?, ?, ?, ?)',
                   (livre.titre, livre.pitch, auteur_id, livre.date_public))
    conn.commit()
    conn.close()

    return {'message': 'Livre ajouté avec succès'}

# Endpoint pour ajouter un utilisateur
@app.post('/utilisateur/ajouter', response_model=dict)
async def ajouter_utilisateur(utilisateur: UtilisateurCreate):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM utilisateurs WHERE nom_utilisateur = ?', (utilisateur.nom,))
    utilisateur_result = cursor.fetchone()

    if not utilisateur_result:
        cursor.execute('INSERT INTO utilisateurs (nom_utilisateur, email_utilisateur) VALUES (?, ?)',
                       (utilisateur.nom, utilisateur.email))
        conn.commit()
        conn.close()
        return {'message': 'Utilisateur ajouté avec succès'}
    else:
        conn.close()
        raise HTTPException(status_code=400, detail="Utilisateur existant")

# Endpoint pour supprimer un utilisateur par ID
@app.delete('/utilisateur/{utilisateur_id}/supprimer', response_model=dict)
async def supprimer_utilisateur(utilisateur_id: int = Path(..., description="ID de l'utilisateur")):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM utilisateurs WHERE id = ?', (utilisateur_id,))
    conn.commit()
    conn.close()

    return {'message': 'Utilisateur supprimé avec succès'}

nest_asyncio.apply()
uvicorn.run(app, host='127.0.0.1', port=5009)
