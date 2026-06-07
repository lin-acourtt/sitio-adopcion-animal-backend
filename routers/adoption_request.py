from fastapi import APIRouter, Depends, HTTPException, status
from httpx import request
from sqlalchemy.orm import Session


from database.session import get_db
from models.animal import Animal
from models.adoption_request import AdoptionRequest
from schemas.adoption_request import AdoptionRequestCreate, AdoptionRequestOut, AdoptionStatusUpdate

router_adoptionrequest = APIRouter(prefix="/adoption-request", tags=["adoption_request"])

# Get all adoption requests
@router_adoptionrequest.get("/", response_model=list[AdoptionRequestOut])
def get_all_adoption_requests(db: Session = Depends(get_db)):
    adoption_requests = db.query(AdoptionRequest).all()
    if not adoption_requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No adoption requests found")

    adoption_requests_out = []

    for request in adoption_requests:
        # Need to get the animal name for each request to include it in the response
        animal = db.query(Animal).filter_by(id=request.animal_id).first()
        animal_name = animal.name if animal else "Unknown"
        adoption_requests_out.append(
            AdoptionRequestOut(
                **request.__dict__,
                animal_name=animal_name
                
            )
        )
    
    return adoption_requests_out

# Get adoption request by ID
@router_adoptionrequest.get("/{adoption_request_id}", response_model=AdoptionRequestOut)
def get_adoption_request_by_id(adoption_request_id: int, db: Session = Depends(get_db)):
    adoption_request = db.query(AdoptionRequest).filter_by(id=adoption_request_id).first()
    if not adoption_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adoption request not found")
    
    animal = db.query(Animal).filter_by(id=adoption_request.animal_id).first()
    animal_name = animal.name if animal else "Unknown"

    adoption_request_out = AdoptionRequestOut(
                                            **adoption_request.__dict__,
                                            animal_name=animal_name
                                            )       
                                            
 
    return adoption_request_out


# Create a new adoption request
@router_adoptionrequest.post("/add", response_model=AdoptionRequestOut)
def create_adoption_request(adoption_request: AdoptionRequestCreate, db: Session = Depends(get_db)):
    # Create an AdoptionRequest instance with received data
    db_adoption_request = AdoptionRequest(
        animal_id=adoption_request.animal_id,
        full_name=adoption_request.full_name,
        email=adoption_request.email,
        phone=adoption_request.phone,
        city=adoption_request.city,
        housing_type=adoption_request.housing_type,
        has_yard=adoption_request.has_yard,
        has_other_pets=adoption_request.has_other_pets,
        other_pets_description=adoption_request.other_pets_description,
        has_children=adoption_request.has_children,
        children_ages=adoption_request.children_ages,
        previous_pet_experience=adoption_request.previous_pet_experience,
        reason_for_adoption=adoption_request.reason_for_adoption,
        hours_alone_per_day=adoption_request.hours_alone_per_day,
        agrees_to_responsibilities=adoption_request.agrees_to_responsibilities
    )
    db.add(db_adoption_request)
    db.commit()
    db.refresh(db_adoption_request)

    animal = db.query(Animal).filter_by(id=db_adoption_request.animal_id).first()
    animal_name = animal.name if animal else "Unknown"

    adoption_request_out = AdoptionRequestOut(
                                            **db_adoption_request.__dict__,
                                            animal_name=animal_name
                                            )  
    return adoption_request_out


# Delete an adoption request by ID 
@router_adoptionrequest.delete("/{adoption_request_id}", status_code=status.HTTP_200_OK)
def delete_adoption_request_by_id(adoption_request_id: int, db: Session = Depends(get_db)):
    adoption_request = db.query(AdoptionRequest).filter_by(id=adoption_request_id).first()
    if not adoption_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adoption request not found")
    db.delete(adoption_request)
    db.commit()
    return {"success": True, "message": f"Adoption request with ID '{adoption_request_id}' deleted successfully"}

# Modify an adoption request's status
@router_adoptionrequest.put("/{adoption_request_id}/status", response_model=AdoptionRequestOut)
def modify_adoption_request_status(adoption_request_id: int, status_update: AdoptionStatusUpdate, db: Session = Depends(get_db)):
    adoption_request = db.query(AdoptionRequest).filter_by(id=adoption_request_id).first()
    if not adoption_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adoption request not found")
    
    adoption_request.status = status_update.status
    db.commit()
    db.refresh(adoption_request)

    animal = db.query(Animal).filter_by(id=adoption_request.animal_id).first()
    animal_name = animal.name if animal else "Unknown"

    adoption_request_out = AdoptionRequestOut(
                                            **adoption_request.__dict__,
                                            animal_name=animal_name
                                            )  
    
    return adoption_request_out
