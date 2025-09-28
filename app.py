from fastapi import FastAPI,HTTPException
from typing import Dict,List,Optional
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse

import json

app=FastAPI()

class Patient(BaseModel):
    # name:str=Field(...,title="Enter your name",max_length=50)
    # city:str=Field(...,title='Enter your city',max_length=50)
    # height:int=Field(...,title="Enter your height",gt=0)
    # weight:int=Field(...,title="Enter your weight",gt=0)
    # age:int=Field(...,title='enter your age',gt=0)
    # gender:str=Field(...,title='enter your gender',default='Male')
    id:str
    name:str
    city:str
    height:float
    weight:float
    age:int
    gender:str
    
    @computed_field
    @property
    def bmi(self)->float:
        return round((self.weight/self.height**2),2)
    @computed_field
    @property    
    def verdict(self)->str:
        if self.bmi<18:
            return "underweight"
        elif self.bmi<25:
            return "normal"
        else:
            return "overweight"
        



class update_patient(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    
    @computed_field
    @property
    def bmi(self) -> Optional[float]:
        if self.height is not None and self.weight is not None:
            return round(self.weight / self.height**2, 2)
        return None

    @computed_field
    @property
    def verdict(self) -> Optional[str]:
        bmi = self.bmi
        if bmi is None:
            return None
        if bmi < 18:
            return "underweight"
        elif bmi < 25:
            return "normal"
        else:
            return "overweight"


        
        
        

    
    
    
def get_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

def save_data(data): 
    with open('patients.json','w') as f: 
        json.dump(data,f)





@app.get('/')
def index():
    return {'message':'you are in home page'}

@app.get('/read/{patient_id}')
def read_patient(patient_id):
    data=get_data()
    return data[patient_id]


# we are directly passing the request body to this
@app.post('/create')
def create_patient(patient:Patient):
    data=get_data()
    if patient.id in data:
        raise HTTPException(status_code=401,detail={'message':'user already exists'})
    temp=patient.model_dump()
    data[patient.id]=temp
    save_data(data)
    
    return JSONResponse(status_code=201,content={'message':'patient_created'})

@app.post('/update/{patient_id}')
def updatepatient(patient_id,patient:update_patient):
    data=get_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="user does not exists")
    
    real_data=data[patient_id] 
    patient_updated=patient.model_dump(exclude_unset=True)
    for key,value in patient_updated.items():
        real_data[key]=value
        
    data[patient_id]=real_data
        
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'updated sucessfully'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id):
    data=get_data()
    if patient_id not in data:
        raise HTTPException(status_code=401,detail="user does not exist")
    
    del data[patient_id]
    save_data(data)
    
    return JSONResponse(status_code=201,content={'message':'sucessfully deleted'})
    
    
        