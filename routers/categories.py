from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from models import Category, Product
from schemas import CategoryCreate, CategoryRead, CategoryWithProducts
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CategoryRead])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/{category_id}", response_model=CategoryWithProducts)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = (
        db.query(Category)
        .options(joinedload(Category.products))
        .filter(Category.id == category_id)
        .first()
    )
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(name=category.name)
    db.add(db_category)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Не удалось создать категорию (вероятно, имя уже используется)")
    db.refresh(db_category)
    return db_category

@router.post("/{category_id}/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_product_to_category(category_id: int, product_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    if product in category.products:
        raise HTTPException(status_code=400, detail="Продукт уже находится в этой категории")

    category.products.append(product)
    db.commit()
    return 