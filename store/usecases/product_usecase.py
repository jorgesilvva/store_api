# usecases/product_usecase.py

from typing import List
from pydantic import UUID4
from datetime import datetime

from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException, InsertionException
from store.db.models import Product  # Assumindo que este é o modelo ORM
from store.db.session import Session  # Assumindo que esta é a sessão do banco de dados

class ProductUsecase:
    def __init__(self, db: Session):
        self.db = db

    async def create(self, body: ProductIn) -> ProductOut:
        try:
            product = Product(**body.dict())
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            return ProductOut.from_orm(product)
        except Exception as e:
            raise InsertionException(f"Failed to insert product: {str(e)}")

    async def get(self, id: UUID4) -> ProductOut:
        product = self.db.query(Product).filter(Product.id == id).first()
        if not product:
            raise NotFoundException("Product not found")
        return ProductOut.from_orm(product)

    async def query(self, price_min: float, price_max: float) -> List[ProductOut]:
        products = self.db.query(Product).filter(Product.price > price_min, Product.price < price_max).all()
        return [ProductOut.from_orm(product) for product in products]

    async def update(self, id: UUID4, body: ProductUpdate) -> ProductUpdateOut:
        product = self.db.query(Product).filter(Product.id == id).first()
        if not product:
            raise NotFoundException("Product not found")
        
        for key, value in body.dict(exclude_unset=True).items():
            setattr(product, key, value)
        product.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(product)
        return ProductUpdateOut.from_orm(product)

    async def delete(self, id: UUID4) -> None:
        product = self.db.query(Product).filter(Product.id == id).first()
        if not product:
            raise NotFoundException("Product not found")
        self.db.delete(product)
        self.db.commit()
