from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from database.session import get_db
from models.animal import Animal
from schemas.animal import AnimalResponse,AnimalCreate, AnimalUpdate
from services.auth import hash_password, authenticate_user

router_animal = APIRouter(prefix="/animal", tags=["animal"])

# Get all animals
@router_animal.get("/", response_model=list[AnimalResponse])
def get_all_animals(db: Session = Depends(get_db)):
    animals = db.query(Animal).all()
    if not animals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No animals found")
    return animals

# Get animals by id
@router_animal.get("/{animal_id}", response_model=AnimalResponse)
def get_animal_by_id(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter_by(id=animal_id).first()
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    return animal

# Create a new animal
@router_animal.post("/add", response_model=AnimalResponse)
def create_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    # Create an Animal instance with received data
    db_animal = Animal(
        name=animal.name,
        species=animal.species,
        breed=animal.breed,
        age_years=animal.age_years,
        age_months=animal.age_months,
        gender=animal.gender,
        is_neutered=animal.is_neutered,
        is_vaccinated=animal.is_vaccinated,
        personality=animal.personality,
        story=animal.story,
        adopter_responsibilities=animal.adopter_responsibilities,
        is_available=animal.is_available
    )
    # Animal is created with no photos. Photos can be added later using the /photo endpoint.
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

# Delete an animal by ID 
@router_animal.delete("/{animal_id}", status_code=status.HTTP_200_OK)
def delete_animal_by_id(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter_by(id=animal_id).first()
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    db.delete(animal)
    db.commit()
    return {"success": True, "message": f"Animal with ID '{animal_id}' and name '{animal.name}' deleted successfully"}

# Modify an animal
@router_animal.put("/{animal_id}", response_model=AnimalResponse)
def modify_animal(animal_id: int, animal_newattributes: AnimalUpdate, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter_by(id=animal_id).first()
    print("Animal to update:", animal)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    
    updated_animal = animal_newattributes.model_dump(exclude_unset=True)
    
    for attr, value in updated_animal.items():
        setattr(animal, attr, value)
    db.commit()
    db.refresh(animal)
    #return animal
    return animal
