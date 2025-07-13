from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from models import Product, Category
from schemas import ProductRead, ProductCreate, CategoryRead
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ProductRead])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).options(joinedload(Product.categories)).all()
    return products

@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Validate categories
    categories = db.query(Category).filter(Category.id.in_(product.category_ids)).all()
    if len(categories) != len(product.category_ids):
        raise HTTPException(status_code=400, detail="Некорректный category_id")

    db_product = Product(name=product.name, price=product.price, categories=categories)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product 