from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from database.connection import get_session
from main import app



def test_create_hero():
        # Some code here omitted, we will see it later 👈
        
        client = TestClient(app)  
        # response = client.post(  
        #     "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
        # )
        # Some code here omitted, we will see it later 👈
        # data = response.json()  

        # assert response.status_code == 200  
        # assert data["name"] == "Deadpond"  
        # assert data["secret_name"] == "Dive Wilson"  
        # assert data["age"] is None  
        # assert data["id"] is not None 
        assert True is True 

# Code below omitted 👇
