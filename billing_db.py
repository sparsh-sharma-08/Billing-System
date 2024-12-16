import sqlite3
import textwrap
from datetime import datetime

con = sqlite3.connect('billing.db')
cursor = con.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bill(
        product TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price INTEGER NOT NULL
    )
''')

# Helper function to validate positive integers
def input_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

# Helper function to display tables (used in view_items and generate_bill)

def print_table(rows, show_total=False):
    serial_width = 10
    product_width = 20
    quantity_width = 10
    price_width = 10

    total_amount = 0  

    # Print table header
    print("-" * (serial_width + product_width + quantity_width + price_width + 10))
    print(f"{'Serial No.':<{serial_width}} {'Product Name':<{product_width}} {'Quantity':<{quantity_width}} {'Price':<{price_width}}")
    print("-" * (serial_width + product_width + quantity_width + price_width + 10))

    # Print table rows
    for i, row in enumerate(rows, start=1):
        serial_no = str(i)
        product = textwrap.fill(row[1], width=product_width).split("\n")
        quantity = str(row[2])
        price = str(row[3])

        if show_total:
            total_amount += row[2] * row[3] 

        print(f"{serial_no:<{serial_width}} {product[0]:<{product_width}} {quantity:<{quantity_width}} {price:<{price_width}}")
        for line in product[1:]:
            print(f"{' ':<{serial_width}} {line:<{product_width}}")

    print("-" * (serial_width + product_width + quantity_width + price_width + 10))

    if show_total:
        print(f"Total Amount:: ₹{total_amount}") 

    return total_amount 

# Add items to the cart
def add_items():
    try:
        product = input("Enter the product name: ")
        quantity = input_positive_integer("Enter the product quantity: ")
        price = input_positive_integer("Enter the product price: ")
        cursor.execute("INSERT INTO bill (product, quantity, price) VALUES (?, ?, ?)", (product, quantity, price))
        con.commit()
        print(f"{product} with quantity {quantity} has been added to your cart worth ₹{price}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Update items in the cart using serial number
def update_items():
    rows = display_items()
    if not rows:
        return

    try:
        serial_no = input_positive_integer("Enter the serial number of the product to update: ")
        if 1 <= serial_no <= len(rows):
            rowid = rows[serial_no - 1][0]  
            product = input("Enter the new product name: ")
            quantity = input_positive_integer("Enter the new product quantity: ")
            price = input_positive_integer("Enter the new product price: ")
            cursor.execute("UPDATE bill SET product=?, quantity=?, price=? WHERE rowid=?", (product, quantity, price, rowid))
            con.commit()
            print(f"Product at serial number {serial_no} has been updated.")
        else:
            print("Invalid serial number! Please select a valid number from the list.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Delete items from the cart using serial number
def delete_items():
    rows = display_items()
    if not rows:
        return

    try:
        serial_no = input_positive_integer("Enter the serial number of the product to delete: ")
        if 1 <= serial_no <= len(rows):
            rowid = rows[serial_no - 1][0] 
            cursor.execute("DELETE FROM bill WHERE rowid=?", (rowid,))
            con.commit()
            print(f"Product at serial number {serial_no} has been removed from the cart.")
        else:
            print("Invalid serial number! Please select a valid number from the list.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Clear the cart
def clear_cart():
    confirm=input("Are you sure? (Y/N)")
    if confirm=="y":
        cursor.execute("DELETE FROM bill")
        con.commit()
        print("The cart has been cleared.")
    else:
        print("Cart not cleared!")

# View items in the cart
def display_items():
    cursor.execute("SELECT rowid, product, quantity, price FROM bill")  
    rows = cursor.fetchall()

    if not rows:
        print("\nThe cart is empty!")
        return []

    print_table(rows)
    return rows

def view_items():
    rows = display_items()
    if not rows:
        return

# Generate the bill
def generate_bill():
    rows = display_items() 
    if not rows:
        print("\nNo items in the cart to generate a bill!")
        return
    
    print(f"Bill Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")  
    print("\nThank you for shopping with us!")

# Greetings function
def greetings():
    print("\nThank you for shopping with us!")

# Main function
def main():
    try:
        while True:
            print("\nWelcome To Our Store! Select any of the following options:")
            print("1. Add Items to the Cart")
            print("2. Update Items in the Cart")
            print("3. Delete Items from the Cart")
            print("4. View Items in the Cart")
            print("5. Generate Bill")
            print("6. Clear Cart")
            print("7. Exit")
            user_input = input("Enter the operation to perform: ")

            match user_input:
                case "1":
                    add_items()
                case "2":
                    update_items()
                case "3":
                    delete_items()
                case "4":
                    view_items()
                case "5":
                    generate_bill()
                case "6":
                    clear_cart()
                case "7":
                    break
                case _:
                    print("Invalid choice! Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        greetings()
        con.close()

if __name__ == "__main__":
    main()
