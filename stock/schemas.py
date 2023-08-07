import strawberry
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import *

Session = sessionmaker(bind=engine)
session =Session()

from dao import (
    SupplierDAO,
    ProductDAO,
    CategoryDAO,
    SupplierOrderDAO,
    SupplierOrderItemDAO,
    ConsumerOrderDAO,
    ConsumerOrderItemDAO,
    ConsumerDAO,
)
from models import (
    Supplier,
    Product,
    Category,
    SupplierOrder,
    SupplierOrderItem,
    ConsumerOrder,
    ConsumerOrderItem,
    Consumer
)

@strawberry.type
class SupplierSchema:
    id: int
    name: str
    contact_number: str

@strawberry.type
class ProductSchema:
    id: int
    category_id: int
    name: str
    unit_price: float
    description: str

@strawberry.type
class CategorySchema:
    id: int
    category_name: str

@strawberry.type
class SupplierOrderSchema:
    id: int
    supplier_id: int
    order_date: str
    total_amount: float

@strawberry.type
class SupplierOrderItemSchema:
    id: int
    supplier_order_id: int
    product_id: int
    item_name: str
    quantity: int
    unit_price: float
    total_price:Optional[float]


@strawberry.type
class ConsumerOrderSchema:
    id: int
    consumer_id: int
    order_date: str
    total_amount: float

@strawberry.type
class ConsumerOrderItemSchema:
    id: int
    consumer_order_id: int
    product_id: int
    item_name: str
    quantity: int
    unit_price: float
    total_price: float

@strawberry.type
class ConsumerSchema:
    id: int
    name: str
    contact_number: str

@strawberry.type
class Product:
    id: int
    category_id: int
    name: str
    unit_price: float
    description: str


# Define your queries and mutations

@strawberry.type
class Query:
    # Supplier queries
    @strawberry.field
    def get_supplier_by_id(self, supplier_id: int) -> Optional[SupplierSchema]:
        supplier_dao = SupplierDAO(session)
        supplier = supplier_dao.get_supplier_by_id(supplier_id)
        return SupplierSchema(id=supplier.id, name=supplier.name, contact_number=supplier.contact_number) if supplier else None

    
    @strawberry.field
    def get_all_suppliers(self) -> List[SupplierSchema]:
        supplier_dao = SupplierDAO(session)
        suppliers = supplier_dao.get_all_suppliers()
        return [
            SupplierSchema(id=supplier.id, name=supplier.name, contact_number=supplier.contact_number)
            for supplier in suppliers
        ]
                


    # Product queries
    @strawberry.field
    def get_product_by_id(self, product_id: int) -> Optional[ProductSchema]:
        product_dao = ProductDAO(session)
        product = product_dao.get_product_by_id(product_id)
        return ProductSchema(
            id=product.id,
            category_id=product.category_id,
            name=product.name,
            unit_price=product.unit_price,
            description=product.description,
        ) if product else None

    
    @strawberry.field
    def get_all_products(self) -> List[ProductSchema]:
        product_dao = ProductDAO(session)
        products = product_dao.get_all_products()
        return [
            ProductSchema(
                id=product.id,
                category_id=product.category_id,
                name=product.name,
                unit_price=product.unit_price,
                description=product.description,
            )
            for product in products
        ]

    # Category queries
    @strawberry.field
    def get_category_by_id(self, category_id: int) -> Optional[CategorySchema]:
        category_dao = CategoryDAO(session)
        category = category_dao.get_category_by_id(category_id)
        return CategorySchema(id=category.id, category_name=category.category_name) if category else None
    
    @strawberry.field
    def get_all_categories(self) -> List[CategorySchema]:
        category_dao = CategoryDAO(session)
        categories = category_dao.get_all_categories()
        return [
            CategorySchema(id=category.id, category_name=category.category_name)
            for category in categories
        ]

    # SupplierOrder queries
    @strawberry.field
    def get_supplier_order_by_id(self, supplier_order_id: int) -> Optional[SupplierOrderSchema]:
        supplier_order_dao = SupplierOrderDAO(session)
        supplier_order = supplier_order_dao.get_supplier_order_by_id(supplier_order_id)
        return SupplierOrderSchema(
            id=supplier_order.id,
            supplier_id=supplier_order.supplier_id,
            order_date=supplier_order.order_date,
            total_amount=supplier_order.total_amount,
        ) if supplier_order else None

    # SupplierOrderItem queries
    @strawberry.field
    def get_supplier_order_item_by_id(self, supplier_order_item_id: int) -> Optional[SupplierOrderItemSchema]:
        supplier_order_item_dao = SupplierOrderItemDAO(session)
        supplier_order_item = supplier_order_item_dao.get_supplier_order_item_by_id(supplier_order_item_id)
        return SupplierOrderItemSchema(
            id=supplier_order_item.id,
            supplier_order_id=supplier_order_item.supplier_order_id,
            product_id=supplier_order_item.product_id,
            item_name=supplier_order_item.item_name,
            quantity=supplier_order_item.quantity,
            unit_price=supplier_order_item.unit_price,
            total_price=supplier_order_item.total_price,
        ) if supplier_order_item else None
    

    @strawberry.field
    def get_all_supplier_orders(self) -> List[SupplierOrderSchema]:
        supplier_order_dao = SupplierOrderDAO(session)
        supplier_orders = supplier_order_dao.get_all_supplier_orders()
        return [
            SupplierOrderSchema(
                id=supplier_order.id,
                supplier_id=supplier_order.supplier_id,
                order_date=supplier_order.order_date,
                total_amount=supplier_order.total_amount,
            )
            for supplier_order in supplier_orders
        ]
    
    @strawberry.field
    def get_all_supplier_order_items(self) -> List[SupplierOrderItemSchema]:
        supplier_order_item_dao = SupplierOrderItemDAO(session)
        supplier_order_items = supplier_order_item_dao.get_all_supplier_order_items()
        return [
            SupplierOrderItemSchema(
                id=supplier_order_item.id,
                supplier_order_id=supplier_order_item.supplier_order_id,
                product_id=supplier_order_item.product_id,
                item_name=supplier_order_item.item_name,
                quantity=supplier_order_item.quantity,
                unit_price=supplier_order_item.unit_price,
                total_price=supplier_order_item.total_price,
            )
            for supplier_order_item in supplier_order_items
        ]

    # ConsumerOrder queries
    @strawberry.field
    def get_consumer_order_by_id(self, consumer_order_id: int) -> Optional[ConsumerOrderSchema]:
        consumer_order_dao = ConsumerOrderDAO(session)
        consumer_order = consumer_order_dao.get_consumer_order_by_id(consumer_order_id)
        return ConsumerOrderSchema(
            id=consumer_order.id,
            consumer_id=consumer_order.consumer_id,
            order_date=consumer_order.order_date,
            total_amount=consumer_order.total_amount,
        ) if consumer_order else None
    
    @strawberry.field
    def get_all_consumer_orders(self) -> List[ConsumerOrderSchema]:
        consumer_order_dao = ConsumerOrderDAO(session)
        consumer_orders = consumer_order_dao.get_all_consumer_orders()
        return [
            ConsumerOrderSchema(
                id=consumer_order.id,
                consumer_id=consumer_order.consumer_id,
                order_date=consumer_order.order_date,
                total_amount=consumer_order.total_amount,
            )
            for consumer_order in consumer_orders
        ]

    # ConsumerOrderItem queries
    @strawberry.field
    def get_consumer_order_item_by_id(self, consumer_order_item_id: int) -> Optional[ConsumerOrderItemSchema]:
        consumer_order_item_dao = ConsumerOrderItemDAO(session)
        consumer_order_item = consumer_order_item_dao.get_consumer_order_item_by_id(consumer_order_item_id)
        return ConsumerOrderItemSchema(
            id=consumer_order_item.id,
            consumer_order_id=consumer_order_item.consumer_order_id,
            product_id=consumer_order_item.product_id,
            item_name=consumer_order_item.item_name,
            quantity=consumer_order_item.quantity,
            unit_price=consumer_order_item.unit_price,
            total_price=consumer_order_item.total_price,
        ) if consumer_order_item else None
    
    @strawberry.field
    def get_all_consumer_order_items(self) -> List[ConsumerOrderItemSchema]:
        consumer_order_item_dao = ConsumerOrderItemDAO(session)
        consumer_order_items = consumer_order_item_dao.get_all_consumer_order_items()
        return [
            ConsumerOrderItemSchema(
                id=consumer_order_item.id,
                consumer_order_id=consumer_order_item.consumer_order_id,
                product_id=consumer_order_item.product_id,
                item_name=consumer_order_item.item_name,
                quantity=consumer_order_item.quantity,
                unit_price=consumer_order_item.unit_price,
                total_price=consumer_order_item.total_price,
            )
            for consumer_order_item in consumer_order_items
        ]

    # Consumer queries
    @strawberry.field
    def get_consumer_by_id(self, consumer_id: int) -> Optional[ConsumerSchema]:
        consumer_dao = ConsumerDAO(session)
        consumer = consumer_dao.get_consumer_by_id(consumer_id)
        return ConsumerSchema(id=consumer.id, name=consumer.name, contact_number=consumer.contact_number) if consumer else None

    @strawberry.field
    def get_consumers_by_name(self, name: str) -> List[ConsumerSchema]:
        consumer_dao = ConsumerDAO(session)
        consumers = consumer_dao.get_consumers_by_name(name)
        return [
            ConsumerSchema(id=consumer.id, name=consumer.name, contact_number=consumer.contact_number)
            for consumer in consumers
        ]
    
    @strawberry.field
    def get_all_consumers(self) -> List[ConsumerSchema]:
        consumer_dao = ConsumerDAO(session)
        consumers = consumer_dao.get_all_consumers()
        return [
            ConsumerSchema(id=consumer.id, name=consumer.name, contact_number=consumer.contact_number)
            for consumer in consumers
        ]
    
    @strawberry.field
    def get_products_by_category_id(category_id: int) -> List[ProductSchema]:
        product_dao = ProductDAO(session)
        products = product_dao.get_products_by_category_id(category_id)

        return [
            ProductSchema(
                id=product.id,
                category_id=product.category_id,
                name=product.name,
                unit_price=product.unit_price,
                description=product.description
            )
            for product in products
        ]
    
    @strawberry.field
    def get_products_supplierid(self,supplier_id: int) -> List[Product]:
        supplier_dao=SupplierDAO(session)
        return supplier_dao.get_supplier_products(supplier_id)
    
    @strawberry.field
    def get_suppliers_by_product_name(self, product_name: str) -> List[SupplierSchema]:
        product_dao = ProductDAO(session)
        return product_dao.get_suppliers_by_product_name(product_name)
    
    @strawberry.field
    def get_product_by_name(self, product_name: str) -> Optional[ProductSchema]:
        product_dao = ProductDAO(session)
        product = product_dao.get_product_by_name(product_name)
        
        if product:
            return ProductSchema(
                id=product.id,
                category_id=product.category_id,
                name=product.name,
                unit_price=product.unit_price,
                description=product.description,
            )
        return None
    
    @strawberry.field
    def get_category_by_name(self, category_name: str) -> Optional[CategorySchema]:
        category_dao = CategoryDAO(session)
        category = category_dao.get_category_by_name(category_name)
        
        if category:
            return CategorySchema(
                id=category.id,
                category_name=category.category_name,
            )
        
        return None
    
    
    @strawberry.field
    def get_products_by_consumer_order_item(consumer_order_item_id: int) -> List[Product]:
        product_dao = ProductDAO(session)
        return product_dao.get_products_by_consumer_order_item(consumer_order_item_id)
    
    @strawberry.field
    def get_products_by_supplier_order_item(supplier_order_item_id: int) -> List[Product]:
        product_dao = ProductDAO(session)
        return product_dao.get_products_by_supplier_order_item(supplier_order_item_id)
    
    @strawberry.field
    def get_consumer_orders_by_order_date(self, order_date: date) -> List[ConsumerOrderSchema]:
        consumer_order_dao = ConsumerOrderDAO(session)
        return consumer_order_dao.get_consumer_orders_by_order_date(order_date)
    
    @strawberry.field
    def get_supplier_orders_by_order_date(self, order_date: date) -> List[SupplierOrderSchema]:
        supplier_order_dao = SupplierOrderDAO(session)
        return supplier_order_dao.get_supplier_orders_by_order_date(order_date)
    
    @strawberry.field
    def get_supplier_by_name(supplier_name: str) -> Optional[SupplierSchema]:
        supplier = (
            session.query(Supplier)
            .filter(func.lower(Supplier.name) == func.lower(supplier_name))
            .first()
        )
        
        if supplier:
            return SupplierSchema(
                id=supplier.id,
                name=supplier.name,
                contact_number=supplier.contact_number,
            )
        
        return None
    

    @strawberry.field
    def get_category_by_supplierid(self, supplier_id: int) -> List[CategorySchema]:
        category_dao = CategoryDAO(session)
        categories = category_dao.get_category_by_supplierid(supplier_id)
        return [
            CategorySchema(id=category.id, category_name=category.category_name)
            for category in categories
        ]

    
    @strawberry.field
    def get_supplier_by_productid(self, product_id: int) -> Optional[SupplierSchema]:
        product_dao = ProductDAO(session)
        supplier = product_dao.get_supplier_by_productid(product_id)
        
        if supplier:
            return SupplierSchema(
                id=supplier.id,
                name=supplier.name,
                contact_number=supplier.contact_number,
            )
        
        return None
    
    @strawberry.field
    def getProductsBySupplierOrderId(supplier_order_id: int) -> List[ProductSchema]:
        product_dao = ProductDAO(session)
        products = product_dao.get_products_by_supplierorder_id(supplier_order_id)

        return [
            ProductSchema(
                id=product.id,
                category_id=product.category_id,
                name=product.name,
                unit_price=product.unit_price,
                description=product.description
            )
            for product in products
        ] 
    



    @strawberry.field
    def getProductsBySupplierOrderDate(supplier_order_date: date) -> List[ProductSchema]:
        product_dao = ProductDAO(session)
        products = product_dao.get_products_by_supplierorder_date(supplier_order_date)

        return [
            ProductSchema(
                id=product.id,
                category_id=product.category_id,
                name=product.name,
                unit_price=product.unit_price,
                description=product.description
            )
            for product in products
        ]
    
    @strawberry.field
    def get_products_by_category_name(category_name: str) -> List[ProductSchema]:
        product_dao = ProductDAO(session)
        return product_dao.get_products_by_category_name(category_name)
    
    @strawberry.field
    def get_all_consumer_orders_by_product(self, product_name: str) -> List[ConsumerOrderSchema]:
        consumer_order_dao = ConsumerOrderDAO(session)
        return consumer_order_dao.get_all_consumer_orders_by_product(product_name)
    

    @strawberry.field
    def get_supplier_orders_by_supplier_id(self, supplier_id: int) -> List[SupplierOrderSchema]:
        supplier_order_dao = SupplierOrderDAO(session)
        supplier_orders = supplier_order_dao.get_supplier_orders_by_supplier_id(supplier_id)
        return [
            SupplierOrderSchema(
                id=supplier_order.id,
                supplier_id=supplier_order.supplier_id,
                order_date=supplier_order.order_date,
                total_amount=supplier_order.total_amount,
            )
            for supplier_order in supplier_orders
        ]
    
    @strawberry.field
    def get_supplier_orders_by_product(self, product_name: str) -> List[SupplierOrderSchema]:
        supplier_order_dao = SupplierOrderDAO(session)
        supplier_orders = supplier_order_dao.get_supplier_orders_by_product(product_name)

        # Convert SupplierOrder objects to SupplierOrderSchema objects
        return [
            SupplierOrderSchema(
                id=supplier_order.id,
                supplier_id=supplier_order.supplier_id,
                order_date=supplier_order.order_date,
                total_amount=supplier_order.total_amount,
            )
            for supplier_order in supplier_orders
        ]
    
    @strawberry.field
    def getSuppliersByCategoriesId(category_ids: List[int]) -> List[SupplierSchema]:
        supplier_dao = SupplierDAO(session)
        suppliers = supplier_dao.get_supplier_by_categories_id(category_ids)

        return [
            SupplierSchema(
                id=supplier.id,
                name=supplier.name,
                contact_number=supplier.contact_number
            )
            for supplier in suppliers
        ]

    @strawberry.field
    def get_supplier_by_category_name(self, category_name: str) -> List[SupplierSchema]:
        supplier_dao = SupplierDAO(session)
        suppliers = supplier_dao.get_supplier_by_category_name(category_name)

        return [
            SupplierSchema(
                id=supplier.id,
                name=supplier.name,
                contact_number=supplier.contact_number
            )
            for supplier in suppliers
        ]
    
    @strawberry.field
    def get_Products_by_Supplier_Name(supplier_name: str) -> List[ProductSchema]:
        product_dao = ProductDAO(session)
        products = product_dao.get_products_by_supplier_name(supplier_name)

        return [
            ProductSchema(
                id=product.id,
                category_id=product.category_id,
                name=product.name,
                unit_price=product.unit_price,
                description=product.description
            )
            for product in products
        ]
    
    @strawberry.field
    def get_category_by_suppliername(self, supplier_name: str) -> List[CategorySchema]:
        category_dao = CategoryDAO(session)
        categories = category_dao.get_category_by_suppliername(supplier_name)
        return[
            CategorySchema(id=category.id, category_name=category.category_name)
            for category in categories
        ]
    
    @strawberry.field
    def get_Products_by_Customer_Order_date(order_date: str) -> List[ProductSchema]:
        product_dao = ProductDAO(session)
        products = product_dao.get_products_by_customer_order_date(order_date)

        return [
            ProductSchema(
                id=product.id,
                category_id=product.category_id,
                name=product.name,
                unit_price=product.unit_price,
                description=product.description
            )
            for product in products
        ]
    

@strawberry.type
class Mutation:
    # Supplier mutations
    @strawberry.mutation
    def create_supplier(self, name: str, contact_number: str) -> SupplierSchema:
        supplier_dao = SupplierDAO(session)  
        supplier = supplier_dao.create_supplier(name, contact_number)
        return SupplierSchema(id=supplier.id, name=supplier.name, contact_number=supplier.contact_number)

    @strawberry.mutation
    def update_supplier(
        self,
        supplier_id: int,
        name: Optional[str] = None,
        contact_number: Optional[str] = None,
    ) -> Optional[SupplierSchema]:
        supplier_dao = SupplierDAO(session)  
        supplier = supplier_dao.update_supplier(supplier_id, name, contact_number)
        return SupplierSchema(id=supplier.id, name=supplier.name, contact_number=supplier.contact_number) if supplier else None

    @strawberry.mutation
    def delete_supplier(self, supplier_id: int) -> bool:
        supplier_dao = SupplierDAO(session) 
        return supplier_dao.delete_supplier(supplier_id)


    # Product mutations
    @strawberry.mutation
    def create_product(
        self,
        name: str,
        unit_price: float,
        description: str,
        category_id: int,
    ) -> ProductSchema:
        product_dao = ProductDAO(session)
        product = product_dao.create_product(name, unit_price, description, category_id)
        return ProductSchema(
            id=product.id,
            category_id=product.category_id,
            name=product.name,
            unit_price=product.unit_price,
            description=product.description,
        )

    @strawberry.mutation
    def update_product(
        self,
        product_id: int,
        name: Optional[str] = None,
        unit_price: Optional[float] = None,
        description: Optional[str] = None,
    ) -> Optional[ProductSchema]:
        product_dao = ProductDAO(session)
        product = product_dao.update_product(product_id, name, unit_price, description)
        return ProductSchema(
            id=product.id,
            category_id=product.category_id,
            name=product.name,
            unit_price=product.unit_price,
            description=product.description,
        ) if product else None

    @strawberry.mutation
    def delete_product(self, product_id: int) -> bool:
        product_dao = ProductDAO(session)
        return product_dao.delete_product(product_id)

    # Category mutations
    @strawberry.mutation
    def create_category(self, category_name: str) -> CategorySchema:
        category_dao = CategoryDAO(session)
        category = category_dao.create_category(category_name)
        return CategorySchema(id=category.id, category_name=category.category_name)

    @strawberry.mutation
    def update_category(self, category_id: int, category_name: str) -> Optional[CategorySchema]:
        category_dao = CategoryDAO(session)
        category = category_dao.update_category(category_id, category_name)
        return CategorySchema(id=category.id, category_name=category.category_name) if category else None

    @strawberry.mutation
    def delete_category(self, category_id: int) -> bool:
        category_dao = CategoryDAO(session)
        return category_dao.delete_category(category_id)

    # SupplierOrder mutations
    @strawberry.mutation
    def create_supplier_order(
        self,
        supplier_id: int,
        order_date: str,
        total_amount: float,
    ) -> SupplierOrderSchema:
        supplier_order_dao = SupplierOrderDAO(session)
        supplier_order = supplier_order_dao.create_supplier_order(supplier_id, order_date, total_amount)
        return SupplierOrderSchema(
            id=supplier_order.id,
            supplier_id=supplier_order.supplier_id,
            order_date=supplier_order.order_date,
            total_amount=supplier_order.total_amount,
        )

    @strawberry.mutation
    def update_supplier_order(
        self,
        supplier_order_id: int,
        order_date: Optional[str] = None,
        total_amount: Optional[float] = None,
    ) -> Optional[SupplierOrderSchema]:
        supplier_order_dao = SupplierOrderDAO(session)
        supplier_order = supplier_order_dao.update_supplier_order(supplier_order_id, order_date, total_amount)
        return SupplierOrderSchema(
            id=supplier_order.id,
            supplier_id=supplier_order.supplier_id,
            order_date=supplier_order.order_date,
            total_amount=supplier_order.total_amount,
        ) if supplier_order else None

    @strawberry.mutation
    def delete_supplier_order(self, supplier_order_id: int) -> bool:
        supplier_order_dao = SupplierOrderDAO(session)
        return supplier_order_dao.delete_supplier_order(supplier_order_id)

    # SupplierOrderItem mutations
    @strawberry.mutation
    def create_supplier_order_item(
        self,
        supplier_order_id: int,
        product_id: int,
        item_name: str,
        quantity: int,
        unit_price: float,
        total_price: Optional[float],
    ) -> SupplierOrderItemSchema:
        supplier_order_item_dao = SupplierOrderItemDAO(session)
        supplier_order_item = supplier_order_item_dao.create_supplier_order_item(
            supplier_order_id, product_id, item_name, quantity, unit_price, total_price
        )
        if supplier_order_item.quantity is not None and supplier_order_item.product and supplier_order_item.product.unit_price is not None:
                supplier_order_item.total_price = supplier_order_item.quantity * supplier_order_item.unit_price
                
        else:
            supplier_order_item.total_price = 0 # Set a default value if any of the required fields are None
            
        return SupplierOrderItemSchema(
            id=supplier_order_item.id,
            supplier_order_id=supplier_order_item.supplier_order_id,
            product_id=supplier_order_item.product_id,
            item_name=supplier_order_item.item_name,
            quantity=supplier_order_item.quantity,
            unit_price=supplier_order_item.unit_price,
            total_price=supplier_order_item.total_price,
        )

    
    @strawberry.mutation
    def update_supplier_order_item(
        self,
        supplier_order_item_id: int,
        item_name: Optional[str] = None,
        quantity: Optional[int] = None,
        unit_price: Optional[float] = None,
        total_price: Optional[float] = None,
    ) -> Optional[SupplierOrderItemSchema]:
        supplier_order_item_dao = SupplierOrderItemDAO(session)
        supplier_order_item = supplier_order_item_dao.get_supplier_order_item_by_id(supplier_order_item_id)

        if supplier_order_item:
            if item_name is not None:
                supplier_order_item.item_name = item_name
            if quantity is not None:
                supplier_order_item.quantity = quantity
            if unit_price is not None:
                supplier_order_item.unit_price = unit_price
            if total_price is not None:
                supplier_order_item.total_price = total_price
            elif (
                supplier_order_item.quantity is not None
                and supplier_order_item.unit_price is not None
            ):
                supplier_order_item.total_price = (
                    supplier_order_item.quantity * supplier_order_item.unit_price
                )
            else:
                supplier_order_item.total_price = 0  # Set a default value if any of the required fields are None

            session.commit()

            return SupplierOrderItemSchema(
                id=supplier_order_item.id,
                supplier_order_id=supplier_order_item.supplier_order_id,
                product_id=supplier_order_item.product_id,
                item_name=supplier_order_item.item_name,
                quantity=supplier_order_item.quantity,
                unit_price=supplier_order_item.unit_price,
                total_price=supplier_order_item.total_price,
            )

        return None



    @strawberry.mutation
    def delete_supplier_order_item(self, supplier_order_item_id: int) -> bool:
        supplier_order_item_dao = SupplierOrderItemDAO(session)
        return supplier_order_item_dao.delete_supplier_order_item(supplier_order_item_id)

    # ConsumerOrder mutations
    @strawberry.mutation
    def create_consumer_order(
        self,
        consumer_id: int,
        order_date: str,
        total_amount: float,
    ) -> ConsumerOrderSchema:
        consumer_order_dao = ConsumerOrderDAO(session)
        consumer_order = consumer_order_dao.create_consumer_order(consumer_id, order_date, total_amount)
        return ConsumerOrderSchema(
            id=consumer_order.id,
            consumer_id=consumer_order.consumer_id,
            order_date=consumer_order.order_date,
            total_amount=consumer_order.total_amount,
        )

    @strawberry.mutation
    def update_consumer_order(
        self,
        consumer_order_id: int,
        order_date: Optional[str] = None,
        total_amount: Optional[float] = None,
    ) -> Optional[ConsumerOrderSchema]:
        consumer_order_dao = ConsumerOrderDAO(session)
        consumer_order = consumer_order_dao.update_consumer_order(consumer_order_id, order_date, total_amount)
        return ConsumerOrderSchema(
            id=consumer_order.id,
            consumer_id=consumer_order.consumer_id,
            order_date=consumer_order.order_date,
            total_amount=consumer_order.total_amount,
        ) if consumer_order else None

    @strawberry.mutation
    def delete_consumer_order(self, consumer_order_id: int) -> bool:
        consumer_order_dao = ConsumerOrderDAO(session)
        return consumer_order_dao.delete_consumer_order(consumer_order_id)

    # ConsumerOrderItem mutations
    @strawberry.mutation
    def create_consumer_order_item(
        self,
        consumer_order_id: int,
        product_id: int,
        item_name: str,
        quantity: int,
        unit_price: float,
        total_price: Optional[float],  # Add total_price argument
    ) -> Optional[ConsumerOrderItemSchema]:
        # Check if the product exists
        product = self.session.query(Product).get(product_id)
        if not product:
            return None  # Product with the given ID does not exist

        consumer_order_item_dao = ConsumerOrderItemDAO(session)
        consumer_order_item = consumer_order_item_dao.create_consumer_order_item(
            consumer_order_id, product_id, item_name, quantity, unit_price
        )

        return ConsumerOrderItemSchema(
            id=consumer_order_item.id,
            consumer_order_id=consumer_order_item.consumer_order_id,
            product_id=consumer_order_item.product_id,
            item_name=consumer_order_item.item_name,
            quantity=consumer_order_item.quantity,
            unit_price=consumer_order_item.unit_price,
            total_price=consumer_order_item.total_price,

        )



    @strawberry.mutation
    def update_consumer_order_item(
        self,
        consumer_order_item_id: int,
        item_name: Optional[str] = None,
        quantity: Optional[int] = None,
        unit_price: Optional[float] = None,
    ) -> Optional[ConsumerOrderItemSchema]:
        consumer_order_item_dao = ConsumerOrderItemDAO(session)
        consumer_order_item = consumer_order_item_dao.update_consumer_order_item(
            consumer_order_item_id, item_name, quantity, unit_price
        )

        if consumer_order_item:
            consumer_order_item.calculate_total_price()

            session.commit()

            return ConsumerOrderItemSchema(
                id=consumer_order_item.id,
                consumer_order_id=consumer_order_item.consumer_order_id,
                product_id=consumer_order_item.product_id,
                item_name=consumer_order_item.item_name,
                quantity=consumer_order_item.quantity,
                unit_price=consumer_order_item.unit_price,
                total_price=consumer_order_item.total_price,
            )

        return None


    @strawberry.mutation
    def delete_consumer_order_item(self, consumer_order_item_id: int) -> bool:
        consumer_order_item_dao = ConsumerOrderItemDAO(session)
        return consumer_order_item_dao.delete_consumer_order_item(consumer_order_item_id)
    
    

    # ConsumerOrder mutations
    @strawberry.mutation
    def create_consumer_order(
        self,
        consumer_id: int,
        order_date: str,
        total_amount: float,
    ) -> ConsumerOrderSchema:
        consumer_order_dao = ConsumerOrderDAO(session)
        consumer_order = consumer_order_dao.create_consumer_order(consumer_id, order_date, total_amount)
        return ConsumerOrderSchema(
            id=consumer_order.id,
            consumer_id=consumer_order.consumer_id,
            order_date=consumer_order.order_date,
            total_amount=consumer_order.total_amount,
        )

    @strawberry.mutation
    def update_consumer_order(
        self,
        consumer_order_id: int,
        order_date: Optional[str] = None,
        total_amount: Optional[float] = None,
    ) -> Optional[ConsumerOrderSchema]:
        consumer_order_dao = ConsumerOrderDAO(session)
        consumer_order = consumer_order_dao.update_consumer_order(consumer_order_id, order_date, total_amount)
        return ConsumerOrderSchema(
            id=consumer_order.id,
            consumer_id=consumer_order.consumer_id,
            order_date=consumer_order.order_date,
            total_amount=consumer_order.total_amount,
        ) if consumer_order else None

    @strawberry.mutation
    def delete_consumer_order(self, consumer_order_id: int) -> bool:
        consumer_order_dao = ConsumerOrderDAO(session)
        return consumer_order_dao.delete_consumer_order(consumer_order_id)

    # ConsumerOrderItem mutations
    @strawberry.mutation
    def create_consumer_order_item(
        self,
        consumer_order_id: int,
        product_id: int,
        item_name: str,
        quantity: int,
        unit_price: float
    ) -> ConsumerOrderItemSchema:
        consumer_order_item_dao = ConsumerOrderItemDAO(session)
        consumer_order_item = consumer_order_item_dao.create_consumer_order_item(
            consumer_order_id, product_id, item_name, quantity, unit_price
        )
        return ConsumerOrderItemSchema(
            id=consumer_order_item.id,
            consumer_order_id=consumer_order_item.consumer_order_id,
            product_id=consumer_order_item.product_id,
            item_name=consumer_order_item.item_name,
            quantity=consumer_order_item.quantity,
            unit_price=consumer_order_item.unit_price,
            total_price=consumer_order_item.total_price
        )

    @strawberry.mutation
    def update_consumer_order_item(
        self,
        consumer_order_item_id: int,
        item_name: Optional[str] = None,
        quantity: Optional[int] = None,
        unit_price: Optional[float] = None,
    ) -> Optional[ConsumerOrderItemSchema]:
        consumer_order_item_dao = ConsumerOrderItemDAO(session)
        consumer_order_item = consumer_order_item_dao.update_consumer_order_item(
            consumer_order_item_id, item_name, quantity, unit_price
        )

        if consumer_order_item:
            if quantity is not None and unit_price is not None:
                consumer_order_item.total_price = quantity * unit_price

            return ConsumerOrderItemSchema(
                id=consumer_order_item.id,
                consumer_order_id=consumer_order_item.consumer_order_id,
                product_id=consumer_order_item.product_id,
                item_name=consumer_order_item.item_name,
                quantity=consumer_order_item.quantity,
                unit_price=consumer_order_item.unit_price,
                total_price=consumer_order_item.total_price,
            )

        return None 


    @strawberry.mutation
    def delete_consumer_order_item(self, consumer_order_item_id: int) -> bool:
        consumer_order_item_dao = ConsumerOrderItemDAO(session)
        return consumer_order_item_dao.delete_consumer_order_item(consumer_order_item_id)

    # Consumer mutations
    @strawberry.mutation
    def create_consumer(self, name: str, contact_number: str) -> ConsumerSchema:
        consumer_dao = ConsumerDAO(session)
        consumer = consumer_dao.create_consumer(name, contact_number)
        return ConsumerSchema(id=consumer.id, name=consumer.name, contact_number=consumer.contact_number)

    @strawberry.mutation
    def update_consumer(
        self,
        consumer_id: int,
        name: Optional[str] = None,
        contact_number: Optional[str] = None,
    ) -> Optional[ConsumerSchema]:
        consumer_dao = ConsumerDAO(session)
        consumer = consumer_dao.update_consumer(consumer_id, name, contact_number)
        return ConsumerSchema(id=consumer.id, name=consumer.name, contact_number=consumer.contact_number) if consumer else None

    @strawberry.mutation
    def delete_consumer(self, consumer_id: int) -> bool:
        consumer_dao = ConsumerDAO(session)
        return consumer_dao.delete_consumer(consumer_id)


schema = strawberry.Schema(query=Query, mutation=Mutation)