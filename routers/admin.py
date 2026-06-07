from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from database.session import get_db
from models.admin import Admin
from schemas.admin import AdminCreate, AdminLogin, AdminResponse, Token
from services.auth import hash_password, authenticate_user

router_admin = APIRouter(prefix="/admin", tags=["admin"])

# Get all admins
@router_admin.get("/", response_model=list[AdminResponse])
def get_all_admins(db: Session = Depends(get_db)):
    admins = db.query(Admin).all()
    if not admins:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No admins found")
    return admins

# Get admin by id
@router_admin.get("/{admin_id}", response_model=AdminResponse)
def get_admin_by_id(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter_by(id=admin_id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return admin

# Create a new admin
@router_admin.post("/register", response_model=AdminResponse)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(admin.password)
    # Create an Admin instance with received data
    db_admin = Admin(
        username=admin.username,
        hashed_password=hashed_pw
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

# Delete an admin by ID 
@router_admin.delete("/{admin_id}", status_code=status.HTTP_200_OK)
def delete_admin_by_id(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter_by(id=admin_id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    db.delete(admin)
    db.commit()
    return {"success": True, "message": f"Admin with ID {admin_id} and username '{admin.username}' deleted successfully"}

# Delete an admin by username (Alternative endpoint)
@router_admin.delete("/username/{username}", status_code=status.HTTP_200_OK)
def delete_admin_by_username(username: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter_by(username=username).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    db.delete(admin)
    db.commit()
    return {"success": True, "message": f"Admin with ID {admin.id} and username '{admin.username}' deleted successfully"}

# Modify admin's password
@router_admin.put("/{admin_username}", response_model=AdminResponse)
def update_admin_password(admin_username: str, new_password: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter_by(username=admin_username).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    admin.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(admin)
    return admin

# Get authentication status 
@router_admin.post("/login", response_model=Token)
def login(admin: AdminLogin, db: Session = Depends(get_db)):
    user = authenticate_user(admin.username, admin.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # For simplicity, we return a dummy token. In production, generate a JWT or similar token.
    return Token(access_token="dummy_token", token_type="bearer")