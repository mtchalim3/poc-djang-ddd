#  POC Django + Domain Driven Design (DDD)

## Introduction et explication du fonctionnement du DDD


## Introduction au Domain Driven Design (DDD)
Le Domain Driven Design est une approche de développement logiciel qui place le domaine métier au cœur de la conception. L'objectif est de créer un logiciel qui reflète précisément les concepts métier et les processus de l'organisation.

## Les trois couches principales en DDD :
### Domain Layer - Le cœur métier :
 Contient les entités, value objects, règles métier et services de domaine

### Application Layer - Orchestration :
 Coordonne les use cases et fait le lien entre le domaine et l'infrastructure

### Infrastructure Layer - Détails techniques :
Persistence, APIs, frameworks (Django dans notre cas)

## Structure du projet:
```
poc-django-ddd/
├── src/
│   ├── users/                       # DOMAIN LAYER - Cœur métier
│   │   ├── core/                   # Modèles métier purs
│   │   │   ├── models.py           # Entités et Value Objects
│   │   │   ├── exceptions.py       # Exceptions métier
│   │   │   └── commands.py         # Commandes (CQRS)
│   │   ├── services/               # SERVICES - Logique métier
│   │   │   └── user_services.py    # Services de domaine
│   │   └── adapters/               # ADAPTERS - Interfaces techniques
│   │       └── repository.py       # Interface de repository
│   └── interface_django/           # INFRASTRUCTURE LAYER - Django
│       ├── account/                # App Django
│       │   ├── models.py           # Modèles Django (persistence)
│       │   ├── views.py            # Contrôleurs API
│       │   └── urls.py             # Routes API
│       └── interface_django/
│           └── settings.py         # Configuration Django
├── tests/                          # Tests de toutes les couches
│   ├── unit/                       # Tests unitaires
│   └── integration/                # Tests d'intégration
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Explication Détaillée de Chaque Couche
### 1. Domain Layer - Le Cœur Métier

Le Domain Layer est le cœur métier d’une application, c’est là où réside toute la logique métier et les règles de l’organisation.
Il doit être indépendant de toute technologie, c’est-à-dire sans dépendances à Django, Flask, SQLAlchemy, PostgreSQL, Redis, ou toute autre librairie externe.

Caractéristiques principales :

Isolation totale :

Aucune dépendance à l’infrastructure (DB, frameworks web, API externes).

Écrit en Python pur dans notre cas.

Règles métier :

Les invariants (exemple : un email valide, un mot de passe doit respecter certaines règles).

Les règles de sécurité (exemple : un utilisateur inactif ne peut pas se connecter).

Les comportements métier (exemple : activer/désactiver un compte, valider un OTP, gérer des droits d’accès).

Éléments du Domain Layer :

Entités (Entities) : objets qui possèdent une identité unique (exemple : User, Order, Invoice).

Valeurs (Value Objects) : objets sans identité propre, mais définis uniquement par leurs attributs (exemple : Email, Money, Address).

Services de domaine : logique métier complexe qui ne se rattache pas directement à une entité (exemple : génération d’un token d’authentification, validation de rôles).

Événements de domaine (Domain Events) : événements significatifs du métier (exemple : UserRegistered, PasswordChanged).

Indépendance :

Tu pourrais exécuter le Domain Layer tout seul, sans base de données ni serveur web.

Si demain tu passes de Django à FastAPI, ou de PostgreSQL à MongoDB → le domaine reste inchangé.

NB: dans le domaine layer on oublie tous framework base de donnée ontravail en python pur c'est ici que toute les bonne pratique de programmation intervienne c'est ici que les tests unitaire ont lieu

users/core/models.py - Entités et Value Objects

```
import uuid
from datetime import datetime
import re

class User:
    """
    ENTITÉ MÉTIER - Représente un utilisateur dans le domaine
    Pure Python, aucune dépendance à Django
    """
    
    # Expression régulière pour validation email
    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    def __init__(self, email: str, password="Password123@#", is_active: bool = True, created_at: datetime = None):
        # Identité unique de l'entité
        self.id = str(uuid.uuid4())
        self.password = password
        self.email = self._validate_email(email)  # Validation métier
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.seen = set()  # Exemple de collection métier

    # Méthodes métier - comportements de l'entité
    def _validate_email(self, email: str) -> str:
        """RÈGLE MÉTIER: Validation du format email"""
        if not re.match(self.EMAIL_REGEX, email):
            raise ValueError("Email invalide")
        return email.lower().strip()

    def activate(self):
        """COMPORTEMENT MÉTIER: Activer un utilisateur"""
        self.is_active = True

    def deactivate(self):
        """COMPORTEMENT MÉTIER: Désactiver un utilisateur"""
        self.is_active = False

    # Méthodes techniques
    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, is_active={self.is_active}, created_at={self.created_at})"

    def __eq__(self, value):
        """IDENTITÉ: Deux users sont égaux s'ils ont le même ID"""
        if isinstance(value, User):
            return self.id == value.id
        return False

    def __hash__(self):
        """HASH: Basé sur l'ID unique"""
        return hash(self.id)
```
users/core/exceptions.py - Exceptions Métier

```
class UserAlreadyExists(Exception):
    pass


class UserNotFound(Exception):
    pass


```

### tests unitaire dans le domaine layer
#### test de création d'un nouveau utilsateur
 ```
 # nous testons ici le bon cas c'est a dire lorsque les informations sont bien forunie
 
 from users.core.models import User


def test_user_model():
    user = User(email="l9v3h@example.com", is_active=True)
    print(user)
    assert user.email == "l9v3h@example.com"
    assert user.is_active

 ```


Ce mini POC illustre comment appliquer une architecture **Domain Driven Design (DDD)** avec **Django**.  
L’objectif est de séparer clairement :
- Le **domaine métier** (`users/`) — indépendant de Django
- L’**infrastructure Django** (`interface_django/`) — persistence, API, configurations


## clone du poc

```
git clone https://github.com/mtchalim3/poc-djang-ddd.git

cd poc-django-ddd
pip install -r requirements.txt
# lancer les migrations
cd interface_django
python manage.py makemigrations
python manage.py migrate
cd ..
#lancer les tests
make test
#formatage
make black

```

video:
[Voir la démo du POC](docs/demo.mp4)


##  Points importants

### 1. Séparation du domaine et de l’infra
- Le **dossier `users/`** contient le **cœur métier** (core models, services, règles).  
- Le domaine **n’importe jamais Django** (il est framework-agnostic).  
- L’infra Django (`interface_django/`) ne fait qu’exposer le domaine via API et gérer la persistence.

---

### 2. Configuration Django
Dans `interface_django/interface_django/settings.py`, il faut déclarer vos apps avec leur **chemin complet** :

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "interface_django.account.apps.AccountConfig",  #  app Django
    "rest_framework",
]
```

Ainsi :

Le domaine ne dépend pas de Django ORM

Les tests sur User restent simples et rapides

4. Use Cases exposés dans Django

Les cas d’usage définis dans users/services sont appelés depuis les views.py de l’app Django (interface_django/account/views.py).

Cela permet :

Django gère les requêtes HTTP (API, REST, etc.)

Le domaine reste centré sur la logique métier

5. Tests

Tests unitaires du domaine (users/tests/test_user_core.py, test_user_services.py)

Tests des repositories Django (users/tests/test_django_repo.py)

Tests d’intégration via Django Views (dans account/tests/)

Exemple (pytest) :

```
import pytest
from users.adapters.django_repository import DjangoUserRepository
from users.core.models import User
from interface_django.account.models import UserModel

pytestmark = pytest.mark.django_db 

def test_save_and_get_user():
    repo = DjangoUserRepository()
    user = User(email="django@example.com", password="123456")

    saved_user = repo.save(user)

    assert saved_user.email == "django@example.com"
    assert repo.exists("django@example.com")

def test_get_by_email_returns_user():
    repo = DjangoUserRepository()
    user = User(email="test2@example.com", password="pwd")
    repo.save(user)

    fetched = repo.get_by_email("test2@example.com")

    assert fetched is not None
    assert fetched.email == "test2@example.com"

def test_list_users():
    repo = DjangoUserRepository()
    repo.save(User(email="u1@example.com", password="p1"))
    repo.save(User(email="u2@example.com", password="p2"))

    users = repo.list()
    assert len(users) == 2


```

Configuration du projet
1. setup.py

Contient la configuration standard pour packager le module Python.

2. pyproject.toml

Contient les configurations pour les outils (pytest, linters, etc.).
Important : définir le chemin Django pour les tests avec pytest-django :
```
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "interface_django.interface_django.settings"
python_files = ["tests.py", "test_*.py"]
```
Lancer le POC

Installer les dépendances :
```
pip install -r requirements.txt  
```

Résultat attendu

Domain (users/) totalement découplé de Django

Django utilisé uniquement comme infra (API + ORM)

Tests simples et rapides au niveau domaine, robustes côté infra

Architecture claire, conforme aux principes DDD

 Conclusion

Ce POC démontre comment :

Organiser un projet Django selon les principes DDD

Isoler le domaine métier du framework

Utiliser un repository pattern pour abstraire la persistence

Exposer les cas d’usage via Django Views / DRF