import sqlite3
import json
import os

# Effacer le fichier de base de données s'il existe déjà
if os.path.exists("database.db"):
    os.remove("database.db")

# Création / ouverture d'une base de données SQLite3
with sqlite3.connect('database.db') as conn:
    cur = conn.cursor()
    
    # Création des tables auteurs, utilisateurs, et livres
    cur.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            email TEXT
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS auteurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_auteur TEXT UNIQUE
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS livres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT,
            pitch TEXT,
            date_public TEXT,
            auteur_id INTEGER,
            emprunter_id INTEGER,
            FOREIGN KEY(auteur_id) REFERENCES auteurs(id),
            FOREIGN KEY(emprunter_id) REFERENCES utilisateurs(id)
        )
    """)
    
    # Insertion des utilisateurs
    utilisateurs = [
        (1, 'Alice', 'nouveau.email.alice@example.com'),
        (2, 'John Doe', 'john.doe@example.com'),
        (3, 'Jane Smith', 'jane.smith@example.com')
    ]
    
    cur.executemany("INSERT INTO utilisateurs (id, nom, email) VALUES (?, ?, ?)", utilisateurs)

    # Insertion des auteurs et des livres
    livres = [
        ('Les Misérables', 'Un roman sur la société et la politique de l’époque', '1862', 'Victor Hugo'),
        ('Madame Bovary', 'L’histoire d’une femme qui rêve d’une vie idéale', '1857', 'Gustave Flaubert'),
        ('Germinal', 'Un roman sur la grève dans une mine de charbon', '1885', 'Émile Zola'),
        ('L\'Étranger', 'Le récit d’un homme indifférent aux conventions sociales', '1942', 'Albert Camus'),
        ('La Peste', 'L’histoire d’une épidémie qui frappe une ville', '1947', 'Albert Camus'),
        ('Les Fleurs du mal', 'Recueil de poèmes sur la beauté et la débauche', '1857', 'Charles Baudelaire'),
        ('Les Liaisons dangereuses', 'Un roman sur la manipulation et la séduction', '1782', 'Pierre Choderlos de Laclos'),
        ('Voyage au bout de la nuit', 'L’histoire de la guerre et de la misère humaine', '1932', 'Louis-Ferdinand Céline'),
        ('Les Choses', 'Un roman qui critique la société de consommation', '1965', 'Georges Perec'),
        ('Les Cerfs-volants', 'Un récit de guerre et de l’histoire de l’Afghanistan', '2003', 'Khaled Hosseini'),
        ('Le Nom de la rose', 'Un roman médiéval mêlant mystère et philosophie', '1980', 'Umberto Eco'),
        ('La Métamorphose', 'L’histoire d’un homme transformé en insecte', '1915', 'Franz Kafka'),
        ('Au bonheur des dames', 'Un roman sur la vie dans un grand magasin', '1883', 'Émile Zola'),
        ('La Horde du Contrevent', 'Un récit de science-fiction sur une quête impossible', '2004', 'Alain Damasio'),
        ('Les Rois maudits', 'Une série historique sur les rois de France', '1955', 'Maurice Druon'),
        ('Le Comte de Monte-Cristo', 'Un roman d’aventure et de vengeance', '1844', 'Alexandre Dumas'),
        ('La Guerre et la Paix', 'L’histoire de la guerre de Napoléon vue par les Russes', '1869', 'Léon Tolstoï'),
        ('Les Trois Mousquetaires', 'Un roman d’aventure sur quatre amis', '1844', 'Alexandre Dumas'),
        ('Le Parfum', 'Un roman sur un homme à la recherche de l’odeur parfaite', '1985', 'Patrick Süskind'),
        ('La Vie mode d\'emploi', 'Un roman qui raconte la vie d’un immeuble à travers ses habitants', '1978', 'Georges Perec'),
        ('Le Rouge et le Noir', 'Un roman sur les ambitions sociales d’un jeune homme', '1830', 'Stendhal'),
        ('Bel-Ami', 'L’histoire d’un jeune homme qui monte dans la société grâce à ses conquêtes', '1885', 'Guy de Maupassant'),
        ('L\'Assommoir', 'Le récit de la vie d’une femme dans la pauvreté à Paris', '1877', 'Émile Zola'),
        ('Le Grand Meaulnes', 'Un roman sur la jeunesse et la quête du bonheur', '1913', 'Alain-Fournier'),
        ('Madame Bovary', 'L’histoire d’une femme qui rêve d’une vie idéale', '1857', 'Gustave Flaubert')
    ]
    
    # Insérer les auteurs et les livres dans la base de données
    for titre, pitch, date_public, auteur in livres:
        # Insérer l'auteur si ce n'est pas déjà fait
        cur.execute("INSERT OR IGNORE INTO auteurs (nom_auteur) VALUES (?)", (auteur,))
        
        # Récupérer l'ID de l'auteur
        cur.execute("SELECT id FROM auteurs WHERE nom_auteur = ?", (auteur,))
        auteur_id = cur.fetchone()[0]
        
        # Insérer le livre avec l'ID de l'auteur
        cur.execute("""
            INSERT INTO livres (titre, pitch, date_public, auteur_id)
            VALUES (?, ?, ?, ?)
        """, (titre, pitch, date_public, auteur_id))
        
        print(f"{auteur} a été ajouté(e) à la base de données avec le livre '{titre}'")
    
    # Commit final pour enregistrer tous les ajouts
    conn.commit()

    # Sélectionner et afficher les données pour vérifier
    cur.execute("SELECT * FROM utilisateurs")
    utilisateurs_resultats = cur.fetchall()
    print("Utilisateurs:")
    for utilisateur in utilisateurs_resultats:
        print(utilisateur)

    cur.execute("SELECT * FROM auteurs")
    auteurs_resultats = cur.fetchall()
    print("\nAuteurs:")
    for auteur in auteurs_resultats:
        print(auteur)

    cur.execute("SELECT * FROM livres")
    livres_resultats = cur.fetchall()
    print("\nLivres:")
    for livre in livres_resultats:
        print(livre)

# Fermeture automatique de la connexion avec le 'with' statement
