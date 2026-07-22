import time
import concurrent.futures


def get_user_data(users, id):
    # Find user by ID
    return next((u for u in users if u["id"] == id), None)


def process_single_payment(i):
    # Calculate tax
    tax = i["price"] * 0.1
    time.sleep(0.1)  # Simulate slow network call
    return i["price"] + tax

def get_user_data(users, user_id):
   # Find user by ID
   return next((u for u in users if u['id'] == user_id), None)

def process_payments(items):
    if not items:
        return 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_single_payment, items)
    return sum(results)


def run_batch():
    users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    items = [{"price": 10}, {"price": 20}, {"price": 100}]

    u = get_user_data(users, 3)
    if u is not None:
        print("User found: " + u["name"])
    else:
        print("User not found")

    print("Total: " + str(process_payments(items)))


if __name__ == "__main__":
    run_batch()
   users = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
   items = [{'price': 10}, {'price': 20}, {'price': 100}]
  
   u = get_user_data(users, 3)
   if u is not None:
       print(f"User found: {u['name']}")
   else:
       print("User not found")
  
   print(f"Total: {process_payments(items)}")

if __name__ == "__main__":
   run_batch()
