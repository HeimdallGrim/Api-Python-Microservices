from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import hashlib
import jwt

app = FastAPI()

CLE_SECRETE = "ma_cle_secrete"
ALGORITHME = "HS256"

database = {
    "users": [
        {
            "username": "John Doe",
            "password": hashlib.sha256("password123".encode()).hexdigest(),
        }
    ]
}

# OAuth2 pour l'authentification par token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modèles Pydantic
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str

# Fonctions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si un mot de passe correspond au hash."""
    return hashed_password == hashlib.sha256(plain_password.encode()).hexdigest()

def get_password_hash(password: str) -> str:
    """Retourne le hash d'un mot de passe."""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(database: dict, username: str, password: str):
    """Authentifie un utilisateur dans la base de données."""
    user = next((u for u in database["users"] if u["username"] == username), None)
    if not user or not verify_password(password, user["password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Crée un token JWT avec une durée de validité."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, CLE_SECRETE, algorithm=ALGORITHME)
    return encoded_jwt

def verify_token(token: str):
    """Vérifie et décode un token JWT."""
    try:
        payload = jwt.decode(token, CLE_SECRETE, algorithms=[ALGORITHME])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Le token a expiré")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

# Endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint pour obtenir un token JWT."""
    user = authenticate_user(database, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    """Endpoint pour récupérer les informations d'un utilisateur."""
    username = verify_token(token)
    return {"username": username}

@app.get("/oauth/.well-known/jwks.json")
async def get_jwks():
    """Endpoint pour envoyer la clé publique (exemple simplifié)."""
    return {
        "keys": [
            {
                "kty": "oct",
                "k": CLE_SECRETE,
                "alg": ALGORITHME,
                "use": "sig",
            }
        ]
    }
