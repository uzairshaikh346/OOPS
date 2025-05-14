from abc import ABC, abstractmethod
from datetime import datetime




class InventoryError(Exception):
    pass

class DuplicateProductError(InventoryError):
    pass

class OutOfStockError(InventoryError):
    pass

class InvalidProductDataError(InventoryError):
    pass


class Product(ABC):


    def __init__(self , productID , name , price , quantity_in_stock):
        self.productID = productID
        self.name = name
        self.price = price
        self.quantity_in_stock = quantity_in_stock

    @abstractmethod
    def __str__(self):
        pass

    def restock(self , quantity):
        self.quantity_in_stock = quantity

    def sell(self , quantity):
        if quantity > self.quantity_in_stock:
            raise ValueError("Stock nahi hai")
        self.quantity_in_stock -= quantity

    def get_total_value(self):
        return self.price * self.quantity_in_stock
    


class Electronic(Product):
    def __init__(self, productID, name, price, quantity_in_stock , brand , warranty_years):
        super().__init__(productID, name, price, quantity_in_stock)
        self.brand = brand
        self.warranty_year = warranty_years

    def __str__(self):
        return f"(Electronic) ID : {self.productID} , Name : {self.name} , Price : {self.price} , Quantity : {self.quantity_in_stock} , Brand : {self.brand} , Warranty : {self.warranty_year}"
    
class Grocery(Product):
    def __init__(self, productID, name, price, quantity_in_stock , expiry_date):
        super().__init__(productID, name, price, quantity_in_stock)
        self.expiry_date = datetime.strptime(expiry_date,"%d/%m/%Y")

    def is_expired(self):
        datetime.now() >= self.expiry_date

    def __str__(self):
        return f"(Grocery) ID : {self.productID} , Name : {self.name} , Price : {self.price} , Quantity : {self.quantity_in_stock} , Expiry_date : {self.expiry_date}"
    

class Clothing(Product):
    def __init__(self, productID, name, price, quantity_in_stock , size , material):
        super().__init__(productID, name, price, quantity_in_stock)
        self.size = size
        self.material = material

    def __str__(self):
        return f"(Clothing) ID : {self.productID} , Name : {self.name} , Price : {self.price} , Quantity : {self.quantity_in_stock} , Size : {self.size} , Material : {self.material}"
    





class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self,product):
        if product.__productID in self._products:
            raise DuplicateProductError("Product ID already exist. ")
        self._products[product._productID] = product

    def remove_product(self,productID):
        self._products.pop(productID)

    def search_by_name(self, name):
        return [p for p in self._products.values() if name.lower() in p._name.lower()]
    
    def search_by_type(self, product_type):
        return [p for p in self._products.values() if p.__class__.__name__.lower() == product_type.lower()]
    
    def list_all_product(self):
        return list(self._products.values())
    
    def sell_product(self,productID,quantity):
        if productID in self._products:
            self._products[productID].sell(quantity)

    def restock(self, productID , quantity):
        if productID in self._products:
            self._products[productID].restock(quantity)

    def total_inventory_value(self):
        return sum(p.get_total_value() for p in self._products.values())
    
    def remove_expired_products(self):
        expired = [pid for pid, p in self._products.items() if isinstance(p, Grocery) and p.is_expired()]
        for pid in expired:
            self.remove_product(pid)
