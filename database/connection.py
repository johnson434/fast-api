from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool 

database_file = "planner.db"
database_connection_string = f"sqlite:///{database_file}"
connect_args = {"check_same_thread": False} 
engine = create_engine(
    database_connection_string,  
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  
)

def conn():
    # SQLModel을 상속받은 모든 클래스를 기반으로 데이터베이스에 테이블을 생성
    SQLModel.metadata.create_all(engine)

def get_session():
    # Session => 데이터베이스와 상호작용(CRUD)을 관리하는 객체 
    with Session(engine) as session:
        yield session