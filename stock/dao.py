import re
from typing import List, Optional
from sqlalchemy.orm import Session, join
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from datetime import date
from models import Supplier, Product, Category, SupplierOrder, SupplierOrderItem, ConsumerOrder, ConsumerOrderItem, Consumer

class NoResultFoundError(Exception):
    pass

class SupplierDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_supplier(self, name: str, contact_number: str) -> Supplier:
        supplier = Supplier(name=name, contact_number=contact_number)
        self.session.add(supplier)
        self.session.commit()
        return supplier

    def get_supplier_by_id(self, supplier_id: int) -> Optional[Supplier]:
        try:
            return self.session.query(Supplier).filter_by(id=supplier_id).one()
        except NoResultFound:
            raise NoResultFoundError("Supplier not found")

    def get_all_suppliers(self) -> List[Supplier]:
        return self.session.query(Supplier).all()
    
    def get_supplier_products(self, supplier_id: int) -> List[Product]:
        supplier = self.session.query(Supplier).get(supplier_id)
        if supplier:
            products = (
            self.session.query(Product)
            .join(SupplierOrderItem, Product.id==SupplierOrderItem.product_id)
            .join(SupplierOrder)
            .filter(SupplierOrder.supplier_id == supplier_id)
            .all()
            )
        
        return products
    
    def get_supplier_by_name(self, supplier_name: str) -> Optional[Supplier]:
        supplier = (
            self.session.query(Supplier)
            .filter(func.lower(Supplier.name) == func.lower(supplier_name))
            .first()
        )
        return supplier
            


    def update_supplier(self, supplier_id: int, name: Optional[str] = None, contact_number: Optional[str] = None) -> Optional[Supplier]:
        try:
            supplier = self.session.query(Supplier).filter_by(id=supplier_id).one()
            if name:
                supplier.name = name
            if contact_number:
                supplier.contact_number = contact_number
            self.session.commit()
            return supplier
        except NoResultFound:
            raise NoResultFoundError("Supplier not found")

    def delete_supplier(self, supplier_id: int) -> bool:
        try:
            supplier = self.session.query(Supplier).filter_by(id=supplier_id).one()
            self.session.delete(supplier)
            self.session.commit()
            return True
        except NoResultFound:
            raise NoResultFoundError("Supplier not found")
        
    def get_supplier_by_categories_id(self, category_ids: List[int]) -> List[Supplier]:
        return (
            self.session.query(Supplier)
            .join(SupplierOrder, Supplier.id == SupplierOrder.supplier_id)
            .join(SupplierOrderItem, SupplierOrder.id == SupplierOrderItem.supplier_order_id)
            .join(Product, SupplierOrderItem.product_id == Product.id)
            .filter(Product.category_id.in_(category_ids))
            .distinct()
            .all()
        )
    
    def get_supplier_by_category_name(self, category_name: str) -> List[Supplier]:
        suppliers = (
            self.session.query(Supplier)
            .join(SupplierOrder, Supplier.id == SupplierOrder.supplier_id)
            .join(SupplierOrderItem, SupplierOrder.id == SupplierOrderItem.supplier_order_id)
            .join(Product, SupplierOrderItem.product_id == Product.id)
            .join(Category, Product.category_id == Category.id)
            .filter(Category.category_name == category_name)
            .distinct()
            .all()
        )
        return suppliers



class ProductDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_product(self, name: str, unit_price: float, description: str, category_id: int) -> Product:
        product = Product(name=name, unit_price=unit_price, description=description, category_id=category_id)
        self.session.add(product)
        self.session.commit()
        return product

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        try:
            return self.session.query(Product).filter_by(id=product_id).one()
        except NoResultFound:
            raise NoResultFoundError("Product not found")



    def get_products_by_category_id(self, category_id: int) -> List[Product]:
        return (
            self.session.query(Product)
            .join(SupplierOrderItem, Product.id == SupplierOrderItem.product_id)
            .join(SupplierOrder, SupplierOrderItem.supplier_order_id == SupplierOrder.id)
            .join(Category, Product.category_id == Category.id)
            .filter(Category.id == category_id)
            .all()
        )


    def get_all_products(self) -> List[Product]:
        return self.session.query(Product).all()
    
    
    def get_products_by_consumer_order_item(self, consumer_order_item_id: int) -> List[Product]:
        products = (
            self.session.query(Product)
            .join(ConsumerOrderItem, Product.id == ConsumerOrderItem.product_id)
            .filter(ConsumerOrderItem.id == consumer_order_item_id)
            .all()
        )
        return products
    
    def get_products_by_supplier_order_item(self, supplier_order_item_id: int) -> List[Product]:
        products = (
             self.session.query(Product)
            .join(SupplierOrderItem, Product.id == SupplierOrderItem.product_id)
            .filter(SupplierOrderItem.id == supplier_order_item_id)
            .all()
        )
        return products
    
    
    

    def update_product(self, product_id: int, name: Optional[str] = None, unit_price: Optional[float] = None,
                       description: Optional[str] = None) -> Optional[Product]:
        try:
            product = self.session.query(Product).filter_by(id=product_id).one()
            if name:
                product.name = name
            if unit_price:
                product.unit_price = unit_price
            if description:
                product.description = description
            self.session.commit()
            return product
        except NoResultFound:
            raise NoResultFoundError("Product not found")

    def delete_product(self, product_id: int) -> bool:
        try:
            product = self.session.query(Product).filter_by(id=product_id).one()
            self.session.delete(product)
            self.session.commit()
            return True
        except NoResultFound:
            raise NoResultFoundError("Product not found")
    
    
    def get_suppliers_by_product_name(self, product_name: str) -> List[Supplier]:
        suppliers = (
            self.session.query(Supplier)
            .join(SupplierOrder, Supplier.id == SupplierOrder.supplier_id)
            .join(SupplierOrderItem, SupplierOrderItem.supplier_order_id == SupplierOrder.id)
            .join(Product, Product.id == SupplierOrderItem.product_id)
            .filter(Product.name == product_name)
            .all()
        )
        
        return suppliers
    
    def get_supplier_by_productid(self, product_id: int) -> Optional[Supplier]:
        supplier = (
            self.session.query(Supplier)
            .join(SupplierOrder, Supplier.id == SupplierOrder.supplier_id)
            .join(SupplierOrderItem, SupplierOrderItem.supplier_order_id == SupplierOrder.id)
            .join(Product, Product.id == SupplierOrderItem.product_id)
            .filter(Product.id == product_id)
            .first()
        )
        
        return supplier


    

    
    def get_product_by_name(self, product_name: str) -> Optional[Product]:
        product = (
            self.session.query(Product)
            .filter(func.lower(Product.name) == func.lower(product_name))
            .first()
        )
        return product
    

    def get_products_by_supplierorder_id(self, supplier_order_id: int) -> List[Product]:
        return (
            self.session.query(Product)
            .join(SupplierOrderItem, Product.id == SupplierOrderItem.product_id)
            .join(SupplierOrder, SupplierOrderItem.supplier_order_id == SupplierOrder.id)
            .filter(SupplierOrderItem.supplier_order_id == supplier_order_id)
            .all()
        )
    
    def get_products_by_supplierorder_date(self, supplier_order_date: date) -> List[Product]:
        return (
            self.session.query(Product)
            .join(SupplierOrderItem, Product.id == SupplierOrderItem.product_id)
            .join(SupplierOrder, SupplierOrderItem.supplier_order_id == SupplierOrder.id)
            .filter(SupplierOrder.order_date == supplier_order_date)
            .all()
        )
    
    def get_products_by_category_name(self, category_name: str) -> List[Product]:
        return (
            self.session.query(Product)
            .filter(Category.category_name == category_name)
            .all())
    
    def get_products_by_supplier_name(self, supplier_name: str) -> List[Product]:
        return (
            self.session.query(Product)
            .join(SupplierOrderItem, Product.id == SupplierOrderItem.product_id)
            .join(SupplierOrder, SupplierOrderItem.supplier_order_id == SupplierOrder.id)
            .join(Supplier, SupplierOrder.supplier_id == Supplier.id)
            .filter(Supplier.name == supplier_name)
            .all()
        )
    
    def get_products_by_customer_order_date(self, order_date: str) -> List[Product]:
        return (
            self.session.query(Product)
            .join(ConsumerOrderItem, Product.id == ConsumerOrderItem.product_id)
            .join(ConsumerOrder, ConsumerOrderItem.consumer_order_id == ConsumerOrder.id)
            .filter(ConsumerOrder.order_date == order_date)
            .all()
        )

    

    
    
    




class CategoryDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_category(self, category_name: str) -> Category:
        category = Category(category_name=category_name)
        self.session.add(category)
        self.session.commit()
        return category

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        try:
            return self.session.query(Category).filter_by(id=category_id).one()
        except NoResultFound:
            raise NoResultFoundError("Category not found")

    def get_all_categories(self) -> List[Category]:
        return self.session.query(Category).all()

    def update_category(self, category_id: int, category_name: str) -> Optional[Category]:
        try:
            category = self.session.query(Category).filter_by(id=category_id).one()
            category.category_name = category_name
            self.session.commit()
            return category
        except NoResultFound:
            raise NoResultFoundError("Category not found")

    def delete_category(self, category_id: int) -> bool:
        try:
            category = self.session.query(Category).filter_by(id=category_id).one()
            self.session.delete(category)
            self.session.commit()
            return True
        except NoResultFound:
            raise NoResultFoundError("Category not found")
        
    def get_category_by_name(self, category_name: str) -> Optional[Category]:
        category = (
            self.session.query(Category)
            .filter(func.lower(Category.category_name) == func.lower(category_name))
            .first()
        )
        
        return category
    
    def get_category_by_product_name(self, product_name: str) -> List[Category]:
        category = (
             self.session.query(Category)
            .join(Product, Category.product_id == Product.id)
            .filter(Product.name == product_name)
            .first()
        )
        return category
    

    def get_category_by_supplierid(self, supplier_id: int) -> List[Category]:
        categories = (
            self.session.query(Category)
            .join(Product, Category.product_id == Product.id)
            .join(SupplierOrderItem, SupplierOrderItem.product_id == Product.id)
            .join(SupplierOrder, SupplierOrder.id == SupplierOrderItem.supplier_order_id)
            .join(Supplier, Supplier.id == SupplierOrder.supplier_id)
            .filter(Supplier.id == supplier_id)
            .distinct()
            .all()
        )
        return categories
    

    def get_category_by_suppliername(self, supplier_name: str) -> List[Category]:
        category = (
            self.session.query(Category)
            .join(Product, Category.product_id == Product.id)
            .join(SupplierOrderItem, SupplierOrderItem.product_id == Product.id)
            .join(SupplierOrder, SupplierOrder.id == SupplierOrderItem.supplier_order_id)
            .join(Supplier, Supplier.id == SupplierOrder.supplier_id)
            .filter(func.lower(Supplier.name) == func.lower(supplier_name))
            .filter(Supplier.name == supplier_name)
            .distinct()
            .all()
        )
        return category






    


class SupplierOrderDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_supplier_order(self, supplier_id: int, order_date: str, total_amount: float) -> SupplierOrder:
        supplier_order = SupplierOrder(supplier_id=supplier_id, order_date=order_date, total_amount=total_amount)
        self.session.add(supplier_order)
        self.session.commit()
        return supplier_order

    def get_supplier_order_by_id(self, supplier_order_id: int) -> Optional[SupplierOrder]:
        try:
            return self.session.query(SupplierOrder).filter_by(id=supplier_order_id).one()
        except NoResultFound:
            raise NoResultFoundError("SupplierOrder not found")

    def get_all_supplier_orders(self) -> List[SupplierOrder]:
        return self.session.query(SupplierOrder).all()

    def get_supplier_orders_by_order_date(self, order_date: date) -> List[SupplierOrder]:
        return self.session.query(SupplierOrder).filter(SupplierOrder.order_date == order_date).all()



    def update_supplier_order(self, supplier_order_id: int, order_date: Optional[str] = None,
                              total_amount: Optional[float] = None) -> Optional[SupplierOrder]:
        try:
            supplier_order = self.session.query(SupplierOrder).filter_by(id=supplier_order_id).one()
            if order_date:
                supplier_order.order_date = order_date
            if total_amount:
                supplier_order.total_amount = total_amount
            self.session.commit()
            return supplier_order
        except NoResultFound:
            raise NoResultFoundError("SupplierOrder not found")

    def delete_supplier_order(self, supplier_order_id: int) -> bool:
        try:
            supplier_order = self.session.query(SupplierOrder).filter_by(id=supplier_order_id).one()
            self.session.delete(supplier_order)
            self.session.commit()
            return True
        except NoResultFound:
            raise NoResultFoundError("SupplierOrder not found")
    
    def get_supplier_orders_by_supplier_id(self, supplier_id: int) -> List[SupplierOrder]:
        try:
            return self.session.query(SupplierOrder).filter_by(supplier_id=supplier_id).all()
        except NoResultFound:
            return []
        
    def get_supplier_orders_by_product(self, product_name: str) -> List[SupplierOrder]:
        supplier_orders = self.session.query(SupplierOrder).join(SupplierOrderItem).join(Product).filter(Product.name == product_name).all()
        return supplier_orders



class SupplierOrderItemDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_supplier_order_item(
        self,
        supplier_order_id: int,
        product_id: int,
        item_name: str,
        quantity: int,
        unit_price: float,
        calculate_total: bool = True,
    ) -> SupplierOrderItem:
        supplier_order_item = SupplierOrderItem(
            supplier_order_id=supplier_order_id,
            product_id=product_id,
            item_name=item_name,
            quantity=quantity,
            unit_price=unit_price,
        )

        if calculate_total:
            supplier_order_item.calculate_total_price()

        # Update the total_amount of the associated SupplierOrder
        try:
            supplier_order = self.session.query(SupplierOrder).filter_by(id=supplier_order_id).one()
            if supplier_order_item.total_price is not None:
                if supplier_order.total_amount is None:
                    supplier_order.total_amount = 0  # Initialize to 0 if None
                supplier_order.total_amount += supplier_order_item.total_price

            self.session.add(supplier_order_item)
            self.session.commit()

            return supplier_order_item
        except NoResultFound:
            raise NoResultFoundError("SupplierOrderItem not found")

    def get_supplier_order_item_by_id(self, supplier_order_item_id: int) -> Optional[SupplierOrderItem]:
        try:
            return self.session.query(SupplierOrderItem).filter_by(id=supplier_order_item_id).one()
        except NoResultFound:
            raise NoResultFoundError("SupplierOrderItem not found")

    def get_all_supplier_order_items(self) -> List[SupplierOrderItem]:
        return self.session.query(SupplierOrderItem).all()

    def update_supplier_order_item(
        self,
        supplier_order_item_id: int,
        item_name: Optional[str] = None,
        quantity: Optional[int] = None,
        unit_price: Optional[float] = None,
        calculate_total: bool = True,
    ) -> Optional[SupplierOrderItem]:
        try:
            supplier_order_item = self.session.query(SupplierOrderItem).filter_by(id=supplier_order_item_id).one()
            if item_name is not None:
                supplier_order_item.item_name = item_name
            if quantity is not None:
                supplier_order_item.quantity = quantity
            if unit_price is not None:
                supplier_order_item.unit_price = unit_price

            if calculate_total:
                supplier_order_item.calculate_total_price()

            # Update the total_amount of the associated SupplierOrder
            supplier_order = supplier_order_item.order
            if supplier_order:
                if supplier_order_item.total_price is not None:
                    if supplier_order.total_amount is None:
                        supplier_order.total_amount = 0  # Initialize to 0 if None
                    supplier_order.total_amount += supplier_order_item.total_price

            self.session.commit()
            return supplier_order_item
        except NoResultFound:
            raise NoResultFoundError("SupplierOrderItem not found")

    def delete_supplier_order_item(self, supplier_order_item_id: int) -> bool:
        try:
            supplier_order_item = self.session.query(SupplierOrderItem).filter_by(id=supplier_order_item_id).one()
            self.session.delete(supplier_order_item)
            self.session.commit()
            return True
        except NoResultFound:
            raise NoResultFoundError("SupplierOrderItem not found")


class ConsumerOrderDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_consumer_order(
        self,
        consumer_id: int,
        order_date: str,
        total_amount: float,
    ) -> ConsumerOrder:
        consumer_order = ConsumerOrder(consumer_id=consumer_id, order_date=order_date, total_amount=total_amount)

        self.session.add(consumer_order)
        self.session.commit()
        return consumer_order

    def get_consumer_order_by_id(self, consumer_order_id: int) -> Optional[ConsumerOrder]:
        try:
            return self.session.query(ConsumerOrder).filter_by(id=consumer_order_id).one()
        except NoResultFound:
            raise NoResultFoundError("ConsumerOrder not found")

    def get_all_consumer_orders(self) -> List[ConsumerOrder]:
        return self.session.query(ConsumerOrder).all()
    
    def get_consumer_orders_by_order_date(self, order_date: date) -> List[ConsumerOrder]:
        return self.session.query(ConsumerOrder).filter(ConsumerOrder.order_date == order_date).all()

    def update_consumer_order(
        self,
        consumer_order_id: int,
        order_date: Optional[str] = None,
        total_amount: Optional[float] = None,
    ) -> Optional[ConsumerOrder]:
        try:
            consumer_order = self.session.query(ConsumerOrder).filter_by(id=consumer_order_id).one()
            if order_date is not None:
                consumer_order.order_date = order_date
            if total_amount is not None:
                consumer_order.total_amount = total_amount

            self.session.commit()
            return consumer_order
        except NoResultFound:
            raise NoResultFoundError("ConsumerOrder not found")

    def delete_consumer_order(self, consumer_order_id: int) -> bool:
        try:
            consumer_order = self.session.query(ConsumerOrder).filter_by(id=consumer_order_id).one()
            self.session.delete(consumer_order)
            self.session.commit()
            return True
        except NoResultFound:
            raise NoResultFoundError("ConsumerOrder not found")
        
    def get_all_consumer_orders_by_product(self, product_name: str) -> List[ConsumerOrder]:
        consumer_orders = self.session.query(ConsumerOrder).join(ConsumerOrderItem).join(Product).filter(Product.name == product_name).all()
        return consumer_orders


class ConsumerOrderItemDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_consumer_order_item(
        self,
        consumer_order_id: int,
        product_id: int,
        item_name: str,
        quantity: int,
        unit_price: float,
        total_price: float = 0.0,
    ) -> ConsumerOrderItem:
        consumer_order_item = ConsumerOrderItem(
            consumer_order_id=consumer_order_id,
            product_id=product_id,
            item_name=item_name,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
        )
        consumer_order_item.total_price = quantity * unit_price
        self.session.add(consumer_order_item)

        # Update the total_amount of the associated ConsumerOrder
        try:
            consumer_order = self.session.query(ConsumerOrder).filter_by(id=consumer_order_id).one()
            consumer_order.total_amount += total_price

            self.session.commit()

            return consumer_order_item
        except NoResultFound:
            raise NoResultFoundError("ConsumerOrderItem not found")

    def get_consumer_order_item_by_id(self, consumer_order_item_id: int) -> Optional[ConsumerOrderItem]:
        try:
            return self.session.query(ConsumerOrderItem).filter_by(id=consumer_order_item_id).one()
        except NoResultFound:
            raise NoResultFoundError("ConsumerOrderItem not found")

    def get_all_consumer_order_items(self) -> List[ConsumerOrderItem]:
        return self.session.query(ConsumerOrderItem).all()

    def update_consumer_order_item(
        self,
        consumer_order_item_id: int,
        item_name: Optional[str] = None,
        quantity: Optional[int] = None,
        unit_price: Optional[float] = None,
        total_price: Optional[float] = None,
    ) -> Optional[ConsumerOrderItem]:
        try:
            consumer_order_item = self.session.query(ConsumerOrderItem).filter_by(id=consumer_order_item_id).one()
            if item_name is not None:
                consumer_order_item.item_name = item_name
            if quantity is not None:
                consumer_order_item.quantity = quantity
            if unit_price is not None:
                consumer_order_item.unit_price = unit_price

            if quantity is not None and unit_price is not None:
                consumer_order_item.total_price = quantity * unit_price
            elif total_price is not None:
                consumer_order_item.total_price = total_price

            # Update the total_amount of the associated ConsumerOrder
            consumer_order = consumer_order_item.order
            if consumer_order:
                consumer_order.total_amount += consumer_order_item.total_price

            self.session.commit()
            return consumer_order_item
        except NoResultFound:
            raise NoResultFoundError("ConsumerOrderItem not found")

    def delete_consumer_order_item(self, consumer_order_item_id: int) -> bool:
        try:
            consumer_order_item = self.session.query(ConsumerOrderItem).filter_by(id=consumer_order_item_id).one()
            self.session.delete(consumer_order_item)
            self.session.commit()
            return True
        except NoResultFound:
            raise NoResultFoundError("ConsumerOrderItem not found")


class ConsumerDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_consumer(self, name: str, contact_number: str) -> Consumer:
        consumer = Consumer(name=name, contact_number=contact_number)
        self.session.add(consumer)
        self.session.commit()
        return consumer

    def get_consumer_by_id(self, consumer_id: int) -> Optional[Consumer]:
        try:
            return self.session.query(Consumer).filter_by(id=consumer_id).one()
        except NoResultFound:
            raise NoResultFoundError("Consumer not found")

    def get_consumers_by_name(self, name: str) -> List[Consumer]:
        pattern = re.compile(name, re.IGNORECASE)
        return self.session.query(Consumer).filter(pattern.match(Consumer.name)).all()

    def get_all_consumers(self) -> List[Consumer]:
        return self.session.query(Consumer).all()

    def update_consumer(self, consumer_id: int, name: Optional[str] = None,
                        contact_number: Optional[str] = None) -> Optional[Consumer]:
        try:
            consumer = self.session.query(Consumer).filter_by(id=consumer_id).one()
            if name:
                consumer.name = name
            if contact_number:
                consumer.contact_number = contact_number
            self.session.commit()
            return consumer
        except NoResultFound:
            raise NoResultFoundError("Consumer not found")

    def delete_consumer(self, consumer_id: int) -> bool:
        try:
            consumer = self.session.query(Consumer).filter_by(id=consumer_id).one()
            self.session.delete(consumer)
            self.session.commit()
            return True
        except NoResultFound:
            raise NoResultFoundError("Consumer not found")
