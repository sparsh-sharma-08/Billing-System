import time 
import json

file_path="bill_info.txt"

def list_load():
    try:
        with open(file_path, "r") as file:
            store= json.load(file)
            return store
    except FileNotFoundError:
        print("file not found!")
        return []

def save_data(lists):
    with open(file_path, 'w')as file:
        json.dump(lists, file)

def add_item(lists):
    item_name=input("Enter the item name: ")
    item_price=float(input("Enter price of item: "))
    trans_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    lists.append({"Item name":item_name, "Item price": item_price, "Current Time":trans_time})
    save_data(lists)


def list_cart(lists):
    if not lists:
        print("Cart is empty")
        return
    print("_"*40)
    print("\n")
    for index, cont in enumerate(lists, start=1):
        print(f"{index}. {cont['Item name']}, (₹{cont['Item price']}), Time: ({cont['Current Time']})")
    print("_"*40)
    print("\n")

def update_cart(lists):
    pass

def delete_item(lists):
    pass

def bill_calc(lists):
    pass

def main():
    lists = list_load()
    while True:
        print("Welcome to Billing Software!")
        print("1. Add Item\n2. List Cart Details\3. Update Card\n4. Delete Item\n5. Calculate Bill\n6. Exit")
        user_input=input("Enter the operation no.: ")
        match user_input:
            case "1":
                add_item(lists)
            case "2":
                list_cart(lists)
            case "3":
                update_cart(lists)
            case "4":
                delete_item(lists)
            case "5":
                bill_calc(lists)
            case "6":
                break


if __name__ == "__main__":
    main()