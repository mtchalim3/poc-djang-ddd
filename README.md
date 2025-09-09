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

### repository patterns

Définition du Repository Pattern

En DDD, le Repository est un service technique qui fait l’intermédiaire entre le domaine et la persistence (ex: base de données, fichiers, cache, API externe).

 En clair :

Le domaine ne connaît pas la base de données.

Le domaine demande juste au repository : "Donne-moi cet utilisateur", "Sauvegarde cet utilisateur".

Le repository se charge d’aller dans la DB (ou autre système) et de retourner un objet du domaine (User), pas un objet technique (UserModel Django).

 Rôle du Repository

Abstraction de la persistence :
Le domaine ne doit pas dépendre du choix de la DB ou de l’ORM.
(Aujourd’hui tu utilises Django ORM, demain tu peux passer à SQLAlchemy ou MongoDB sans changer le domaine.)

Interface métier simple :
Le repository expose des méthodes simples comme add, get_by_id, get_by_email, list, exists.

Retourner des objets du domaine uniquement :
Jamais d’objets Django ORM ou SQLAlchemy dans le domaine, toujours des entités User.

 Pourquoi deux versions ?

InMemoryRepository : utilisé pour les tests unitaires du domaine → rapide, pas besoin de base de données.

DjangoUserRepository : utilisé dans l’infrastructure → implémentation réelle qui utilise l’ORM Django.

Les deux implémentent la même interface AbstractUserRepository, donc le domaine peut travailler avec l’un ou l’autre sans rien changer.
NB: le repository pattern ne doit avoir en éalité quye deux fonction ) loa rigueur 3 car le repo ne fait ajouter(add) ou retoruner (get) des données dans la base de données

 Exemple simplifié : deux fonctions essentielles

Tu disais qu’un repository doit au moins avoir deux fonctions : add et get.
Exactement !
On peut réduire ça au minimum vital :


```
from abc import ABC, abstractmethod
from typing import Optional, List
from users.core.models import User
from typing import Optional, List


class AbstractUserRepository(ABC):
    """Interface du UserRepository dans le domaine"""

    def exists(self, email: str) -> bool:
        return self._exists(email)

    def get_by_email(self, email: str) -> Optional[User]:
        return self._get_by_email(email)

    def update(self, user: User) -> User:
        return self._save(user)

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._get_by_id(user_id)

    def list(self) -> List[User]:
        return self._list()

    def save(self, user: User) -> User:
        return self._save(user)

    @abstractmethod
    def _get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def _get_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def _list(self) -> List[User]:
        pass

    @abstractmethod
    def _save(self, user: User) -> User:
        pass

```

Puis deux implémentations :

🔹 En mémoire (tests unitaires)

```

class InMemoryRepository(AbstractUserRepository):
    def __init__(self):
        self._users = []

    def _exists(self, email: str) -> bool:
        return any(user.email == email for user in self._users)

    def _get_by_email(self, email: str) -> Optional[User]:
        return next((user for user in self._users if user.email == email), None)

    def _get_by_id(self, user_id: str) -> Optional[User]:
        return next((user for user in self._users if user.id == user_id), None)

    def _list(self) -> List[User]:
        return self._users

    def _save(self, user: User) -> User:
        self._users.append(user)
        return user

```
Avec Django ORM (prod)
```
from users.core.models import User
from interface_django.account.models import UserModel
from users.adapters.repository import AbstractUserRepository
from typing import Optional, List


class DjangoUserRepository(AbstractUserRepository):
    def exists(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()

    def _get_by_email(self, email: str) -> Optional[User]:
        obj = UserModel.objects.filter(email=email).first()
        return obj.to_domain() if obj else None

    def _get_by_id(self, user_id: str) -> Optional[User]:
        obj = UserModel.objects.filter(id=user_id).first()
        return obj.to_domain() if obj else None

    def _list(self) -> List[User]:
        return [u.to_domain() for u in UserModel.objects.all()]

    def _save(self, user: User) -> User:
        obj = UserModel.from_domain(user)
        obj.save()
        return obj.to_domain()

    def _exists(self, email: str) -> bool:
        return self.exists(email)

```

Test unitaire repository patterns

```
import pytest
from users.core.models import User
from users.adapters.repository import InMemoryRepository


@pytest.fixture
def repo():
    return InMemoryRepository()


def test_save_and_get_by_id(repo):
    user = User(email="test@example.com")
    saved_user = repo.save(user)

    assert saved_user.email == "test@example.com"
    assert repo.get_by_id(saved_user.id) == saved_user


def test_exists_and_get_by_email(repo):
    user = User(email="exists@example.com")
    repo.save(user)

    assert repo.exists("exists@example.com") is True
    assert repo.exists("notfound@example.com") is False
    assert repo.get_by_email("exists@example.com") == user


def test_list_users(repo):
    u1 = User(email="a@example.com")
    u2 = User(email="b@example.com")
    repo.save(u1)
    repo.save(u2)

    users = repo.list()
    assert len(users) == 2
    assert u1 in users and u2 in users


```
Tests d'integration django

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
Résultat :

Dans les tests unitaires : on passes InMemoryUserRepository() → rapide, sans DB.

Dans Django (prod) : on passes DjangoUserRepository() → ça persiste en DB.

Le domaine n’a aucune idée de ce qu’il y a derrière.


## Service layer


Parfait ! Voici comment tu peux documenter **le Service Layer** dans ton README ou dans un tutoriel pour ton POC, en gardant le style DDD et en utilisant ton exemple `UserService`.

---

# 🛠 Service Layer – Orchestration des Use Cases

## 1. Définition

Le **Service Layer** (ou **Application Layer**) est la couche qui :

1. **Orchestre les cas d’usage (use cases)** : il manipule les entités du domaine pour exécuter un scénario métier complet.
2. **Coordonne le domaine et les repositories** : il ne connaît pas la DB directement, il interagit via des interfaces abstraites.
3. **Applique les règles métier** déjà définies dans les entités, mais sans les dupliquer.

> Le Service Layer ne contient pas de logique métier complexe lui-même, il orchestre les entités et leur comportement.

---

## 2. Fonctionnement

1. **Prendre une commande (Command)** : un objet qui encapsule les données nécessaires au use case (ex: `RegisterUserCommand`).
2. **Vérifier les règles métier** via les entités ou les exceptions (ex: vérifier si l’utilisateur existe déjà).
3. **Orchestrer le workflow** : créer ou modifier des entités.
4. **Appeler le Repository** pour persister ou récupérer des données.
5. **Retourner le résultat** sous forme d’entité ou de DTO.

---

## 3. Bonnes pratiques

* Chaque use case correspond à une **méthode du service** (ex: `register`, `authenticate`).
* Injecter les **repositories via le constructeur** pour pouvoir remplacer facilement la DB par un repository en mémoire (tests unitaires).
* Les méthodes doivent rester **cohérentes et simples** : pas de logique métier complexe dedans.
* Toujours travailler avec les **entités du domaine** et jamais avec des objets techniques comme un modèle Django.

---

## 4. Exemple concret – `UserService`

```python
import hashlib
from users.core.models import User
from users.core.exceptions import UserAlreadyExists, UserNotFound
from users.core.commands import RegisterUserCommand
from users.adapters.repository import AbstractUserRepository


class UserService:
    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    def register(self, cmd: RegisterUserCommand) -> User:
        """Créer un nouvel utilisateur"""
        if self.repo.exists(cmd.email):
            raise UserAlreadyExists(
                f"Un utilisateur avec l'email {cmd.email} existe déjà."
            )

        # Hash simple du mot de passe ( pour POC uniquement, pas en prod !)
        password_hash = self._hash_password(cmd.password)

        user = User(email=cmd.email)
        user.password_hash = password_hash  # on enrichit l'entity avec le hash
        return self.repo.save(user)

    def authenticate(self, email: str, password: str) -> User:
        """Vérifier login/password"""
        user = self.repo.get_by_email(email)
        if not user:
            raise UserNotFound("Utilisateur introuvable")

        if user.password_hash != self._hash_password(password):
            raise ValueError("Mot de passe incorrect")

        return user

    # ---------- Utils ----------
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

```

---

## 5. Exemple d’utilisation dans l’application

```python
# Création d'un repository (mémoire ou DB)
repo = InMemoryUserRepository()  # pour les tests
service = UserService(repo)

# 1. Enregistrer un nouvel utilisateur
cmd = RegisterUserCommand(email="alice@example.com", password="Secret123!")
user = service.register(cmd)
print(user)

# 2. Authentification
auth_user = service.authenticate("alice@example.com", "Secret123!")
print(auth_user)
```

Tests Unitaire inmemrory
```
import pytest
from users.core.commands import RegisterUserCommand
from users.services.user_services import UserService
from users.core.exceptions import UserAlreadyExists, UserNotFound
from users.adapters.repository import InMemoryRepository


@pytest.fixture
def service():
    return UserService(InMemoryRepository())


def test_register_user(service):
    cmd = RegisterUserCommand(email="test@example.com", password="secret")
    user = service.register(cmd)

    assert user.email == "test@example.com"
    assert hasattr(user, "password_hash")


def test_register_duplicate_user(service):
    cmd = RegisterUserCommand(email="dup@example.com", password="secret")
    service.register(cmd)
    with pytest.raises(UserAlreadyExists):
        service.register(cmd)


def test_authenticate_success(service):
    cmd = RegisterUserCommand(email="login@example.com", password="mypassword")
    user = service.register(cmd)

    authenticated = service.authenticate("login@example.com", "mypassword")
    assert authenticated == user


def test_authenticate_fail(service):
    cmd = RegisterUserCommand(email="fail@example.com", password="rightpass")
    service.register(cmd)

    with pytest.raises(ValueError):  # mauvais password
        service.authenticate("fail@example.com", "wrongpass")

    with pytest.raises(UserNotFound):  # mauvais email
        service.authenticate("notfound@example.com", "whatever")

```
Tests d'inegration django

```
import pytest
from users.services.user_services import UserService
from users.adapters.django_repository import DjangoUserRepository
from users.core.commands import RegisterUserCommand
from users.core.exceptions import UserAlreadyExists, UserNotFound

pytestmark = pytest.mark.django_db


@pytest.fixture
def service():
    return UserService(DjangoUserRepository())


def test_register_user(service):
    cmd = RegisterUserCommand(email="new@example.com", password="mypassword")
    user = service.register(cmd)
    assert user.email == "new@example.com"


def test_register_duplicate_user(service):
    cmd = RegisterUserCommand(email="dup@example.com", password="secret")
    service.register(cmd)
    with pytest.raises(UserAlreadyExists):
        service.register(cmd)

```

 Avec cette architecture :
>
> * Le **Service Layer** orchestre la logique métier sans connaître la DB.
> * Le **Domain Layer** reste indépendant et testable.
> * Le code est **testable, maintenable et évolutif**.

---

## Service Layer + Unit of Work (UoW) dans DDD
Qu’est-ce que le Unit of Work ?

Le Unit of Work est un pattern qui garantit que toutes les opérations sur la base de données sont exécutées dans un seul contexte transactionnel.

Il regroupe toutes les modifications (création, mise à jour, suppression) dans une transaction.

Si une erreur survient, il permet de rollback toutes les modifications.

Il est particulièrement utile pour les use cases complexes qui touchent plusieurs entités à la fois.

Dans notre architecture DDD avec Django, le Unit of Work sert de couche entre le Service Layer et les Repositories.

si le repository patterns perme de faire la persistence 
UOW permet d'assurer le principe ACID sur la base de donnée
exemple:
```
from abc import ABC, abstractmethod
from users.adapters.repository import AbstractUserRepository, InMemoryRepository
from users.adapters.django_repository import DjangoUserRepository


class AbstractUnitOfWork(ABC):
    users: AbstractUserRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class DjangoUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.users = DjangoUserRepository()

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def commit(self):
       
        pass
           

    def rollback(self):
   
        pass


class InMemoryUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.users = InMemoryRepository()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass  # rien à rollback

    def commit(self):
        pass  # pas de DB réelle

    def rollback(self):
        pass

#ici nous ne gerons pas les commit et roolback car django le gere bien deja maios demain vous travailler avec sqlalchemy ou autre vous devez ajouter self.commit() et self.rollback()
```
le service layer devient:

```
import hashlib
from users.core.models import User
from users.core.exceptions import UserAlreadyExists, UserNotFound
from users.core.commands import RegisterUserCommand
from users.adapters.repository import AbstractUserRepository
from users.services.unit_of_work import AbstractUnitOfWork
class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    # ---------- Use Case 1 : Register ----------
    def register(self, cmd: RegisterUserCommand) -> User:
        with self.uow:
            if self.uow.users.exists(cmd.email):
                raise UserAlreadyExists(
                    f"Un utilisateur avec l'email {cmd.email} existe déjà."
                )

            password_hash = self._hash_password(cmd.password)
            user = User(email=cmd.email)
            user.password_hash = password_hash

            saved_user = self.uow.users.save(user)
      
            return saved_user

    # ---------- Use Case 2 : Authenticate ----------
    def authenticate(self, email: str, password: str) -> User:
        with self.uow:
            user = self.uow.users.get_by_email(email)
            if not user:
                raise UserNotFound("Utilisateur introuvable")

            if user.password_hash != self._hash_password(password):
                raise ValueError("Mot de passe incorrect")

            # Pas besoin de commit ici, juste lecture
            return user

    # ---------- Utils ----------
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
```

Parfait ! Dans ton **README.md**, tu peux introduire la **couche Infrastructure** de manière claire et pédagogique pour les autres développeurs. L’idée est de montrer **son rôle dans l’architecture DDD**, comment elle se connecte au **Domain**, et donner un exemple concret (ici avec Django). Voici un exemple de texte que tu peux mettre dans ton README :

---

## 📦 Infrastructure Layer

La **couche Infrastructure** est responsable de tout ce qui est lié aux **technologies externes**, à la **persistance des données** et aux **interfaces avec le monde extérieur**. Elle ne contient **aucune logique métier**, mais fournit des **adaptateurs** pour que le domaine puisse interagir avec le système (base de données, API, fichiers, services externes…).

### 🔑 Objectifs principaux

1. **Connexion avec la base de données**

   * Gérer le stockage et la récupération des entités du domaine.
   * Fournir des **repositories** conformes aux interfaces du domaine (`AbstractUserRepository`).

2. **Isolation du domaine**

   * La couche **domain** ne connaît pas Django ou d’autres frameworks.
   * L’infrastructure adapte le domaine à la technologie choisie.

3. **Support pour les Use Cases / Services**

   * Permet aux services applicatifs (`UserService`) d’utiliser les repositories sans savoir comment les données sont stockées.
   * Exemple : la même interface peut être utilisée pour **tests unitaires** avec `InMemoryRepository` ou en production avec `DjangoUserRepository`.

4. **Gestion des transactions**

   * Les unités de travail (`UnitOfWork`) sont implémentées ici pour garantir la cohérence de la base.

---

### 🛠 Exemple avec Django

**Modèle Django qui sert d’adaptateur pour le domaine :**

```python
from django.db import models
import uuid
from users.core.models import User

class UserModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"

    # --- MAPPING vers le domaine ---
    def to_domain(self) -> User:
        user = User(
            email=self.email,
            password=self.password,
            is_active=self.is_active,
            created_at=self.created_at,
        )
        user.id = str(self.id)
        return user

    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        return cls(
            id=user.id,
            email=user.email,
            password=user.password,
            is_active=user.is_active,
        )
```

**Repository Django (Infrastructure) :**

```python
from users.core.models import User
from interface_django.account.models import UserModel
from users.adapters.repository import AbstractUserRepository
from typing import Optional, List


class DjangoUserRepository(AbstractUserRepository):
    def exists(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()

    def _get_by_email(self, email: str) -> Optional[User]:
        obj = UserModel.objects.filter(email=email).first()
        return obj.to_domain() if obj else None

    def _get_by_id(self, user_id: str) -> Optional[User]:
        obj = UserModel.objects.filter(id=user_id).first()
        return obj.to_domain() if obj else None

    def _list(self) -> List[User]:
        return [u.to_domain() for u in UserModel.objects.all()]

    def _save(self, user: User) -> User:
        obj = UserModel.from_domain(user)
        obj.save()
        return obj.to_domain()

    def _exists(self, email: str) -> bool:
        return self.exists(email)

```

**Utilisation dans un service :**

```python
from users.services.user_services import UserService
from users.adapters.django_repository import DjangoUserRepository

repo = DjangoUserRepository()
service = UserService(repo)

user = service.register(RegisterUserCommand(email="a@example.com", password="123"))
```

---

 **À retenir** :

* La couche **Infrastructure** ne fait que **mapper et persister** les entités du domaine.
* Toute la logique métier reste dans la couche **Domain** (`User`, `Email`, etc.).
* Cela permet de changer facilement de technologie ou de base de données sans toucher au cœur métier.


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