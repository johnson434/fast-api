import os
from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from database.connection import get_session
from main import app
from database.vms import VM

# 테스트용 인메모리 데이터베이스 URL 설정

# In-Memory SQLite 데이터베이스 엔진 생성
test_engine = create_engine(
    "sqlite:///:memory:", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

# FastAPI 종속성 오버라이드 설정
def override_get_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

# TestClient 인스턴스 생성
client = TestClient(app)

# 데이터베이스 초기화
@pytest.fixture(name="initialize_database")
def initialize_database_fixture():
    SQLModel.metadata.create_all(test_engine)  # 모든 테이블 생성
    yield
    SQLModel.metadata.drop_all(test_engine)  # 테스트 후 모든 테이블 삭제

def test_retrieve_all_vms_returns_empty_list_when_no_vms_exist(initialize_database):
    # 초기 상태에서 VM 목록이 비어 있는지 확인
    response = client.get("/vms/")
    assert response.status_code == 200
    assert response.json() == []
    
def test_retrieve_all_vms_returns_ten_vms_when_ten_vms_inserted(initialize_database):
    # 초기 상태에서 VM 목록이 비어 있는지 확인
    response = client.get("/vms/")
    assert response.status_code == 200
    assert response.json() == []

    # 데이터베이스에 새로운 VM 삽입
    with Session(test_engine) as session:
        for i in range(1, 11):
            vm = VM(id=i, title="Test VM", image="http://example.com/image", description="A test VM")
            session.add(vm)    
        session.commit()

    # 새로운 VM이 제대로 삽입되었는지 확인
    response = client.get("/vms/")
    assert response.status_code == 200
    assert len(response.json()) == 10
    assert response.json()[0]["title"] == "Test VM"

def test_create_vm_returns_200_when_normal_data_inserted(initialize_database):
    # 초기 상태에서 VM 목록이 비어 있는지 확인
    response = client.get("/vms/")
    assert response.status_code == 200
    assert response.json() == []

    # 데이터베이스에 새로운 VM 삽입
    with Session(test_engine) as session:
        new_vm = VM(id=1, title="Test VM", image="http://example.com/image", description="A test VM")
        session.add(new_vm)
        session.commit()
        session.refresh(new_vm)

    # 새로운 VM이 제대로 삽입되었는지 확인
    response = client.get("/vms/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test VM"
    
def test_create_vm_returns_422_when_title_is_none(initialize_database):
    response = client.post("/vms", json= {
        "image": "www.naver.com",
        "description": "설명"
    })
    assert response.status_code == 422
    
    vms = client.get("/vms")
    print(f"vms: {vms.json()}")
    assert len(vms.json()) == 0
    assert vms.status_code == 200
    
def test_retrieve_vms_throws_404_when_request_vm_not_exist(initialize_database):
    # response = client.get("/vms", params= {"id": 1})
    response = client.get("/vms/1")
    assert response.status_code == 404

def test_retrieve_vms_return_vm(initialize_database):
    # 초기 상태에서 VM 목록이 비어 있는지 확인
    response = client.get("/vms/")
    assert response.status_code == 200
    assert response.json() == []
    
    # 데이터베이스에 새로운 VM 삽입
    with Session(test_engine) as session:
        new_vm = VM(id=1, title="Test VM", image="http://example.com/image", description="A test VM")
        session.add(new_vm)
        session.commit()
        session.refresh(new_vm)
    
    response = client.get("/vms/1")
    vm = response.json()
    assert response.status_code == 200
    assert vm['id'] == 1
    assert vm['title'] == 'Test VM'
    assert vm['image'] == "http://example.com/image"
    assert vm['description'] == "A test VM"

def test_delete_vm_throws_404_when_request_vm_not_exist(initialize_database):
    response = client.delete("/vms/1")
    assert response.status_code == 404

def test_delete_vm_return_200_status_when_delete_success(initialize_database):
    with Session(test_engine) as session:
        new_vm = VM(id=1, title="Test VM", image="http://example.com/image", description="A test VM")
        session.add(new_vm)
        session.commit()
        session.refresh(new_vm)
        
    response = client.delete("/vms/1")
    assert response.status_code == 200
    
def test_update_vm_return_200_status_when_update_success(initialize_database):
    id = 1
    with Session(test_engine) as session:
        new_vm = VM(id=id, title="Test VM", image="http://example.com/image", description="A test VM")
        session.add(new_vm)
        session.commit()
        session.refresh(new_vm)
    
    response = client.put(f"/vms/{id}", json = {
        "title": "New title",
        "image": "New Image",
        "description": "New Description"        
    })
    
    assert response.status_code == 200
    
    with Session(test_engine) as session:
        vm = session.get(VM, id)
        assert vm.title == "New title"
        assert vm.image == "New Image"
        assert vm.description == "New Description"