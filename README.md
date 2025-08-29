#  POC Django + Domain Driven Design (DDD)

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