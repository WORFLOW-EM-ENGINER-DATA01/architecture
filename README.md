# Clean Architecture

### 1. **Domain** : Entités, logique métier pure, et interfaces des services/repositories

La **logique métier** pure se trouve dans la couche **Domain**. Cela inclut :

- **Entités** : Les modèles d'objets métier comme `User`, `Product`, etc. Ces entités contiennent les règles métiers essentielles.
- **Services** : Ces services exécutent la logique métier complexe, par exemple, une validation métier ou des calculs complexes.
- **Interfaces des Repositories** : Elles définissent des méthodes pour interagir avec la base de données (ou d'autres sources de données), mais sans spécifier la manière de les implémenter.

Le **Domain** est la couche la plus centrale de l'architecture, indépendante des frameworks et des détails techniques (comme FastAPI, SQLAlchemy, etc.).

### 2. **Application** : Cas d'utilisation qui orchestrent la logique métier

La **couche Application** contient les **cas d'utilisation**, qui orchestrent la logique métier en appelant les entités du **Domain** et les services, puis en interagissant avec la couche **Infrastructure** pour obtenir ou manipuler des données.

Les cas d'utilisation sont responsables de **l'orchestration** et de l'exécution des règles métiers, mais **ne contiennent pas de logique métier complexe**. Ils communiquent avec les services du **Domain** pour exécuter des actions selon les besoins spécifiques de l'application.

### 3. **Infrastructure** : Implémentations concrètes

La **couche Infrastructure** contient des **implémentations concrètes** pour accéder aux données (par exemple, les repositories utilisant SQLAlchemy), gérer les services externes, et exposer des API (les routes FastAPI).

### Structure détaillée

Voici une structure révisée qui reflète mieux cette séparation :

```bash
/my_fastapi_project
│
├── /app
│   ├── /config                     # Configuration générale (DB, API, etc.)
│   ├── /domain                     # Contient les entités métier, services, et interfaces
│   │   ├── /users                  # Entités, services, interfaces pour les utilisateurs
│   │   └── /data_analysis          # Entités, services, interfaces pour l'analyse de données
│   │
│   ├── /application                # Contient les cas d'utilisation
│   │   ├── /users                  # Cas d'utilisation pour les utilisateurs
│   │   └── /data_analysis          # Cas d'utilisation pour l'analyse des données
│   │
│   ├── /infrastructure
│   │   ├── /db                     # Contient la configuration de la base de données (SQLAlchemy)
│   │   ├── /api                    # Contient les routes (contrôleurs)
│   │   └── /repository             # Implémentation des repositories pour interagir avec la base de données
│   │
│   ├── main.py                     # Point d'entrée FastAPI
│   └── startup.py                  # Initialisation des services et dépendances
│
└── /tests                          # Tests unitaires et fonctionnels
```

### **Détail des couches et de la logique métier** :

#### **Domain** (Entités et Services) :

1. **Entités** : Les entités contiennent les règles métiers essentielles.
   
   Exemple (`user.py` dans `domain/users`):

   ```python
   from pydantic import BaseModel

   class User(BaseModel):
       id: int
       name: str
       email: str
   ```

2. **Services** : Ils contiennent des règles métier complexes. Par exemple, un service de validation des utilisateurs, qui pourrait être une logique complexe que vous ne voulez pas mettre directement dans l'entité.

   Exemple (`user_service.py` dans `domain/users`):

   ```python
   from app.domain.users.models import User

   class UserService:
       def validate_email(self, email: str) -> bool:
           # Logique métier pour valider l'email
           return "@" in email
   ```

3. **Interfaces des Repositories** : Définissent des contrats pour accéder aux données, mais ne contiennent pas d'implémentation concrète.

   Exemple (`user_repository.py` dans `domain/users`):

   ```python
   from abc import ABC, abstractmethod
   from app.domain.users.models import User

   class UserRepository(ABC):
       @abstractmethod
       async def save(self, user: User) -> User:
           pass

       @abstractmethod
       async def get_by_id(self, user_id: int) -> User:
           pass
   ```

#### **Application** (Cas d'utilisation) :

Les cas d'utilisation orchestrent la logique métier et appellent les services et les repositories définis dans le **Domain**.

Exemple (`create_user.py` dans `application/users`):

```python
from app.domain.users.models import User
from app.domain.users.repository import UserRepository
from app.domain.users.services import UserService
from app.domain.users.schemas import UserCreate

class CreateUser:
    def __init__(self, user_repository: UserRepository, user_service: UserService):
        self.user_repository = user_repository
        self.user_service = user_service

    async def execute(self, user_create: UserCreate) -> User:
        if not self.user_service.validate_email(user_create.email):
            raise ValueError("Invalid email format")

        user = User(name=user_create.name, email=user_create.email)
        return await self.user_repository.save(user)
```

#### **Infrastructure** (Implémentation concrète des Repositories et Routes) :

1. **Repositories** : Cette couche implémente les interfaces des repositories définies dans **Domain** pour interagir avec la base de données via SQLAlchemy, par exemple.

Exemple (`user_repository.py` dans `infrastructure/repository`):

```python
from app.domain.users.repository import UserRepository
from app.domain.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def save(self, user: User) -> User:
        self.db_session.add(user)
        await self.db_session.commit()
        return user

    async def get_by_id(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()
```

2. **API Routes** : Les routes exposent les endpoints FastAPI et appellent les cas d'utilisation via **`Depends()`**.

Exemple (`user_routes.py` dans `infrastructure/api`):

```python
from fastapi import APIRouter, Depends
from app.application.users.create_user import CreateUser
from app.domain.users.schemas import UserCreate, UserResponse

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(user_create: UserCreate, create_user: CreateUser = Depends()):
    return await create_user.execute(user_create)
```

### Conclusion :

- **Domain** contient la logique métier pure, les entités et les services.
- **Application** orchestre cette logique métier avec des cas d'utilisation spécifiques.
- **Infrastructure** gère les détails concrets, tels que les repositories et les routes API.

Les **cas d'utilisation** dans **Application** ne contiennent pas de logique métier complexe, mais appellent les services du **Domain** pour orchestrer l'exécution de la logique métier. Les **contrôleurs** (ou **routes API**) sont dans **Infrastructure**, ils exposent les endpoints FastAPI et dépendent des cas d'utilisation pour la logique métier.