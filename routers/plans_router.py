from fastapi import APIRouter, HTTPException, Path, Query
from models.plans import Plan, PlanRequest
from uuid import uuid4
import os
import json

router = APIRouter(
    prefix="/plans",
    tags=["Plans"]
)

def get_plans_json():
    file_path = os.path.join("data", "plans.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

plans = get_plans_json()

# --- GET METHODS ---

@router.get('/')
async def first_api():
    return 'Welcome to the Satellite Plans Manager'

@router.get('/all')
async def plans_api():
    return plans

@router.get("/id/{plan_id}")
async def read_plan_by_id(plan_id: str = Path()):
    for plan in plans:
        if plan.get("id") == plan_id:
            return plan
    raise HTTPException(status_code=404, detail="Plan not found")

@router.get('/category/')
async def read_plans_by_category(category: str = Query()):
    plans_to_return = []
    for plan in plans:
        if plan.get('category').casefold() == category.casefold():
            plans_to_return.append(plan)
    return plans_to_return

@router.get('/status/')
async def read_plans_by_status(status: str = Query()):
    plans_to_return = []
    for plan in plans:
        if plan.get('status').casefold() == status.casefold():
            plans_to_return.append(plan)
    return plans_to_return

# --- POST METHOD ---

@router.post('/create_plan')
async def post_plan(plan_req: PlanRequest):
    new_plan = Plan(
        id=str(uuid4()),
        **plan_req.model_dump()
    )
    plans.append(new_plan.model_dump())
    return {"message": "Plan created", "plan_id": new_plan.id}

# --- PUT METHOD ---

@router.put('/{plan_id}/update_plan')
async def put_plan(plan_id: str, updated_plan: PlanRequest):
    for i in range(len(plans)):
        if plans[i].get('id') == plan_id:
            updated = Plan(
                id=plan_id,
                **updated_plan.model_dump()
            )
            plans[i] = updated.model_dump()
            return {"message": "Plan updated"}
    raise HTTPException(status_code=404, detail="Plan not found")

# --- DELETE METHOD ---

@router.delete('/delete/{plan_id}')
async def delete_plan(plan_id: str):
    for i in range(len(plans)):
        if plans[i].get('id') == plan_id:
            plans.pop(i)
            return {"message": "Plan deleted"}
    raise HTTPException(status_code=404, detail="Plan not found")