from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from models import Sale, SaleItem, Product
from schemas import SaleCreate, SaleRead
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SaleRead)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    product_ids = [item.product_id for item in sale.items]
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    products_dict = {p.id: p for p in products}
    if len(products_dict) != len(product_ids):
        raise HTTPException(status_code=400, detail="Некорректный product_id")
    total = 0
    sale_items = []
    for item in sale.items:
        price = products_dict[item.product_id].price
        total += price * item.quantity
        sale_items.append(SaleItem(product_id=item.product_id, quantity=item.quantity, price=price))
    db_sale = Sale(total_amount=total, payment_method=sale.payment_method, items=sale_items)
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@router.get("/", response_model=List[SaleRead])
def get_sales(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    sales = db.query(Sale).options(joinedload(Sale.items).joinedload(SaleItem.product)).order_by(Sale.created_at.desc()).limit(limit).offset(offset).all()
    return sales

@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).options(joinedload(Sale.items).joinedload(SaleItem.product)).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Продажа не найдена")
    return sale 