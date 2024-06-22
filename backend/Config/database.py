from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Caminho para o arquivo SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"

# Criar o engine SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necessário para SQLite
    echo=True  # Ativar para ver saída detalhada
)

# Declarar a base para a definição dos modelos
Base = declarative_base()

# Criar uma sessão de banco de dados
SessionLocal = sessionmaker(
    autocommit=False,  # Desativar autocommit para controle transacional
    autoflush=False,   # Desativar autoflush para controle manual
    bind=engine       # Vincular a sessão ao engine criado
)

# Função para retornar uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para criar todas as tabelas
def create_tables():
    from Models.ModelsUser import User
    from Models.ModelsStorage import Storage
    from Models.ModelsProduct import Product
    from Models.ModelsProductSale import SalesByProduct
    from Models.ModelsSalesTags import SalesByTagModels
    from Models.ModelsOutPut import Output

    Base.metadata.create_all(bind=engine)

# Chamada para criar as tabelas
create_tables()
