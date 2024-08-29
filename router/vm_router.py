from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlmodel import select
from database.connection import get_session
from database.vms import VM, VMUpdate, VMInsert


vm_router = APIRouter(
    tags=["VM"]
)

@vm_router.get("/", response_model=List[VM], status_code=status.HTTP_200_OK)
async def retrieve_all_vms(session = Depends(get_session)) -> List[VM]:
    statement = select(VM)
    vms = session.exec(statement)
    vm_list = vms.all()
    
    if len(vm_list) == 0:
        return []
    
    return vm_list

@vm_router.post("/", status_code=status.HTTP_200_OK)
async def create_vm(vm: VMInsert, session = Depends(get_session)) -> None:
    if not vm.title:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail = "타이틀이 존재하지 않습니다")
    
    session.add(vm)
    session.commit()
    return { "status": 200 }

@vm_router.get("/{id}", response_model=VM, status_code=status.HTTP_200_OK)
async def retrieve_vms(id: int, session = Depends(get_session)) -> VM:
    vm = session.get(VM, id)
    if not vm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 VM입니다")
    return vm

@vm_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_vm(id: int, session = Depends(get_session)) -> None:
    vm = session.get(VM, id)
    if not vm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일치하는 이벤트가 존재하지 않습니다.")
    session.delete(vm)
    session.commit()

@vm_router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_vm(id: int, data: VMUpdate, session = Depends(get_session)) -> None:
    vm = session.get(VM, id)
    if vm:
        event_data = data.model_dump()
        for key, value in event_data.items():
            setattr(vm, key, value)  # 데이터 수정

        session.add(vm)      # 데이터베이스에 데이터 추가
        session.commit()        # 변경사항 저장
        session.refresh(vm)  # 최신 데이터로 갱신
        return
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail="일치하는 이벤트가 존재하지 않습니다.")