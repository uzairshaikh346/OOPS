from abc import ABC, abstractmethod
from datetime import datetime
import json

class InventoryError(Exception):
    pass

class DuplicateProductError(InventoryError):
    pass

class OutOfStockError(InventoryError):
    pass

class InvalidProductDataError(InventoryError):
    pass

class Product(ABC):
    def __init__(self, productID, name, price, quantity_in_stock):
        self._productID = productID
        self.name = name
        self.price = float(price)
        self.quantity_in_stock = int(quantity_in_stock)

    @property
    def productID(self):
        return self._productID

    @abstractmethod
    def __str__(self):
        pass

    def restock(self, quantity):
        self.quantity_in_stock += int(quantity)

    def sell(self, quantity):
        quantity = int(quantity)
        if quantity > self.quantity_in_stock:
            raise OutOfStockError("Requested quantity not available in stock.")
        self.quantity_in_stock -= quantity

    def get_total_value(self):
        return self.price * self.quantity_in_stock

class Electronic(Product):
    def __init__(self, productID, name, price, quantity_in_stock, brand, warranty_years):
        super().__init__(productID, name, price, quantity_in_stock)
        self.brand = brand
        self.warranty_years = int(warranty_years)

    def __str__(self):
        return f"(Electronic) ID: {self.productID}, Name: {self.name}, Price: {self.price}, Quantity: {self.quantity_in_stock}, Brand: {self.brand}, Warranty: {self.warranty_years} years"

    def to_dict(self):
        return {
            "type": "Electronic",
            "productID": self.productID,
            "name": self.name,
            "price": self.price,
            "quantity_in_stock": self.quantity_in_stock,
            "brand": self.brand,
            "warranty_years": self.warranty_years
        }

class Grocery(Product):
    def __init__(self, productID, name, price, quantity_in_stock, expiry_date):
        super().__init__(productID, name, price, quantity_in_stock)
        self.expiry_date = datetime.strptime(expiry_date, "%d/%m/%Y")

    def is_expired(self):
        return datetime.now() >= self.expiry_date

    def __str__(self):
        return f"(Grocery) ID: {self.productID}, Name: {self.name}, Price: {self.price}, Quantity: {self.quantity_in_stock}, Expiry: {self.expiry_date.strftime('%d/%m/%Y')}"

    def to_dict(self):
        return {
            "type": "Grocery",
            "productID": self.productID,
            "name": self.name,
            "price": self.price,
            "quantity_in_stock": self.quantity_in_stock,
            "expiry_date": self.expiry_date.strftime("%d/%m/%Y")
        }

class Clothing(Product):
    def __init__(self, productID, name, price, quantity_in_stock, size, material):
        super().__init__(productID, name, price, quantity_in_stock)
        self.size = size
        self.material = material

    def __str__(self):
        return f"(Clothing) ID: {self.productID}, Name: {self.name}, Price: {self.price}, Quantity: {self.quantity_in_stock}, Size: {self.size}, Material: {self.material}"

    def to_dict(self):
        return {
            "type": "Clothing",
            "productID": self.productID,
            "name": self.name,
            "price": self.price,
            "quantity_in_stock": self.quantity_in_stock,
            "size": self.size,
            "material": self.material
        }

class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product):
        if product.productID in self._products:
            raise DuplicateProductError("Product ID already exists.")
        self._products[product.productID] = product

    def remove_product(self, productID):
        if productID in self._products:
            self._products.pop(productID)
        else:
            raise InvalidProductDataError("Product ID not found.")

    def search_by_name(self, name):
        return [p for p in self._products.values() if name.lower() in p.name.lower()]

    def search_by_type(self, product_type):
        return [p for p in self._products.values() if p.__class__.__name__.lower() == product_type.lower()]

    def list_all_product(self):
        return list(self._products.values())

    def sell_product(self, productID, quantity):
        if productID in self._products:
            self._products[productID].sell(quantity)
        else:
            raise InvalidProductDataError("Product ID not found.")

    def restock(self, productID, quantity):
        if productID in self._products:
            self._products[productID].restock(quantity)
        else:
            raise InvalidProductDataError("Product ID not found.")

    def total_inventory_value(self):
        return sum(p.get_total_value() for p in self._products.values())

    def remove_expired_products(self):
        expired = [pid for pid, p in self._products.items() if isinstance(p, Grocery) and p.is_expired()]
        for pid in expired:
            self.remove_product(pid)

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump([p.to_dict() for p in self._products.values()], f, indent=4)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            for item in data:
                type_ = item.pop("type")
                if type_ == "Electronic":
                    product = Electronic(**item)
                elif type_ == "Grocery":
                    product = Grocery(**item)
                elif type_ == "Clothing":
                    product = Clothing(**item)
                else:
                    continue
                self.add_product(product)


if __name__ == "__main__":
    inv = Inventory()

    try:
        inv.load_from_file("inventory.json")
        inv.remove_expired_products()
    except:
        pass

    while True:
        print("\n--- Inventory Menu ---")
        print("1. Add Product")
        print("2. Sell Product")
        print("3. Restock Product")
        print("4. List All Products")
        print("5. Search by Name")
        print("6. Search by Type")
        print("7. Remove Product")
        print("8. Save Inventory")
        print("9. Show Total Inventory Value")
        print("0. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                type_ = input("Enter type (Electronic/Grocery/Clothing): ").capitalize().strip()
                pid = input("ID: ")
                name = input("Name: ")
                price = float(input("Price: "))
                qty = int(input("Quantity: "))

                if type_ == "Electronic":
                    brand = input("Brand: ")
                    warranty = int(input("Warranty (in years): "))
                    product = Electronic(pid, name, price, qty, brand, warranty)
                elif type_ == "Grocery":
                    expiry_date = input("Expiry Date (dd/mm/yyyy): ")
                    product = Grocery(pid, name, price, qty, expiry_date)
                elif type_ == "Clothing":
                    size = input("Size: ")
                    material = input("Material: ")
                    product = Clothing(pid, name, price, qty, size, material)
                else:
                    print("Invalid type. Try again.")
                    continue

                inv.add_product(product)
                print("Product added successfully!")

            elif choice == "2":
                pid = input("Enter Product ID: ")
                qty = int(input("Enter Quantity: "))
                inv.sell_product(pid, qty)
                print("Product sold successfully!")

            elif choice == "3":
                pid = input("Enter Product ID: ")
                qty = int(input("Enter Quantity to restock: "))
                inv.restock(pid, qty)
                print("Product restocked successfully!")

            elif choice == "4":
                for p in inv.list_all_product():
                    print(p)

            elif choice == "5":
                name = input("Search by name: ")
                results = inv.search_by_name(name)
                for p in results:
                    print(p)

            elif choice == "6":
                type_ = input("Enter product type (Electronic/Grocery/Clothing): ")
                results = inv.search_by_type(type_)
                for p in results:
                    print(p)

            elif choice == "7":
                pid = input("Enter Product ID to remove: ")
                inv.remove_product(pid)
                print("Product removed.")

            elif choice == "8":
                inv.save_to_file("inventory.json")
                print("Inventory saved.")

            elif choice == "9":
                print("Total Inventory Value:", inv.total_inventory_value())

            elif choice == "0":
                inv.save_to_file("inventory.json")
                print("Exiting... Inventory saved.")
                break

            else:
                print("Invalid choice. Try again.")

        except InventoryError as ie:
            print("Inventory Error:", ie)
        except Exception as e:
            print("Error:", e)
