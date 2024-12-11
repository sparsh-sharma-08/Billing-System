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
    if not lists:
        print("Cart is empty. Nothing to update!")
        return
    
    list_cart(lists)

    try:
        index=int(input("Enter the list number to update: "))
        if 1<=index<=len(lists):
            item_name=input("Enter the item name: ")
            item_price=float(input("Enter price of item: "))
            trans_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            lists[index-1]={"Item name":item_name, "Item price": item_price, "Current Time":trans_time}
            save_data(lists)
        else:
            print("Invalid Command!")
    except ValueError:
        print("Invalid input! Please enter a valid number!")

def delete_item(lists):
    if not lists:
        print("Cart is empty. Nothing to delete!")
        return
    
    list_cart(lists)

    try:
        index=int(input("Enter the list number to delete"))
        if 1<=index<=len(lists):
            deleted_item=lists.pop(index-1)
            save_data(lists)
            print(f"Deleted item: {deleted_item['Item name']} (₹{deleted_item['Item price']})")
            print("Updated cart:")
            list_cart(lists)
        else:
            print("invalid index selected for deletion!")
    except ValueError:
        print("Invalid input! Please enter a valid number!")

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