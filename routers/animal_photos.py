from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from database.session import get_db
from models.animal import Animal
from models.animal_photos import AnimalPhotos
from schemas import animal
from schemas.animal import AnimalResponse,AnimalCreate, AnimalUpdate
from schemas.animal_photos import PhotoOut, PhotoCreate, PhotoUpdate
from services.auth import hash_password, authenticate_user

router_photos = APIRouter(prefix="/photos", tags=["photos"])

# Get all photos
@router_photos.get("/", response_model=list[PhotoOut])
def get_all_photos(db: Session = Depends(get_db)):
    photos = db.query(AnimalPhotos).all()
    if not photos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No photos found")
    return photos

# Get photos by id
@router_photos.get("/{photo_id}", response_model=PhotoOut)
def get_photo_by_id(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(AnimalPhotos).filter_by(id=photo_id).first()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo

# Create a new photo
@router_photos.post("/add", response_model=PhotoOut)
def create_photo(photo: PhotoCreate, db: Session = Depends(get_db)):
    # Create an AnimalPhotos instance with received data
    db_photo = AnimalPhotos(
        animal_id=photo.animal_id,
        photo_url=photo.photo_url,
        caption=photo.caption,
        order_index=photo.order_index
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

# Delete a photo by ID 
@router_photos.delete("/{photo_id}", status_code=status.HTTP_200_OK)
def delete_photo_by_id(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(AnimalPhotos).filter_by(id=photo_id).first()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    db.delete(photo)
    db.commit()
    return {"success": True, "message": f"Photo with ID '{photo_id}' deleted successfully"}

# Modify a photo
@router_photos.put("/{photo_id}", response_model=PhotoOut)
def modify_photo(photo_id: int, photo_newattributes: PhotoUpdate, db: Session = Depends(get_db)):
    photo = db.query(AnimalPhotos).filter_by(id=photo_id).first()
    print("Photo to update:", photo)
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    
    updated_photo = photo_newattributes.model_dump(exclude_unset=True)
    
    for attr, value in updated_photo.items():
        setattr(photo, attr, value)
    db.commit()
    db.refresh(photo)
    #return photo
    return photo
