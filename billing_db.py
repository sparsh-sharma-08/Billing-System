import sqlite3
import time

# Connect to the database
con = sqlite3.connect('billing.db')
cursor = con.cursor()

# Create the table without `id` column
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bill(
        product TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price INTEGER NOT NULL
    )
''')


# Helper function to display items with serial numbers
def display_items():
    cursor.execute("SELECT rowid, product, quantity, price FROM bill")  # Use `rowid` as serial number
    rows = cursor.fetchall()

    if not rows:
        print("\nThe cart is empty!")
        return []

    print("\nItems in the cart:")
    print("------------------------------------------------------")
    print("Serial No. | Product Name | Quantity | Price")
    print("------------------------------------------------------")
    for i, row in enumerate(rows, start=1):
        print(f"{i}.           {row[1]}        {row[2]}       {row[3]}")
    print("------------------------------------------------------")
    return rows


# Add items to the cart
def add_items():
    try:
        product = input("Enter the product name: ")
        quantity = int(input("Enter the product quantity: "))
        price = int(input("Enter the product price: "))
        cursor.execute("INSERT INTO bill (product, quantity, price) VALUES (?, ?, ?)", (product, quantity, price))
        con.commit()
        print(f"{product} with quantity {quantity} has been added to your cart worth {price}.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Update items in the cart using serial number
def update_items():
    rows = display_items()
    if not rows:
        return

    try:
        serial_no = int(input("Enter the serial number of the product to update: "))
        if 1 <= serial_no <= len(rows):
            rowid = rows[serial_no - 1][0]  # Get the rowid from the serial number
            product = input("Enter the new product name: ")
            quantity = int(input("Enter the new product quantity: "))
            price = int(input("Enter the new product price: "))
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
        serial_no = int(input("Enter the serial number of the product to delete: "))
        if 1 <= serial_no <= len(rows):
            rowid = rows[serial_no - 1][0]  # Get the rowid from the serial number
            cursor.execute("DELETE FROM bill WHERE rowid=?", (rowid,))
            con.commit()
            print(f"Product at serial number {serial_no} has been removed from the cart.")
        else:
            print("Invalid serial number! Please select a valid number from the list.")
    except Exception as e:
        print(f"An error occurred: {e}")


# View items in the cart
def view_items():
    rows = display_items()
    if not rows:
        return


# Generate the bill
def generate_bill():
    rows = display_items()
    if not rows:
        return

    total_price = sum(row[3] for row in rows)  # Sum the price column
    bill_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print("\nFinal Bill:")
    print("------------------------------------------------------")
    print("Serial No. | Product Name | Quantity | Price")
    print("------------------------------------------------------")
    for i, row in enumerate(rows, start=1):
        print(f"{i}.           {row[1]}        {row[2]}       {row[3]}")
    print("------------------------------------------------------")
    print(f"Total Price: {total_price}")
    print(f"Bill Generated At: {bill_time}")
    print("------------------------------------------------------")


# Greetings function
def greetings(name="Customer"):
    print(f"\nThank you, {name}, for shopping with us!")


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
            print("6. Exit")
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
