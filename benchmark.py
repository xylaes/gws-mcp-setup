import time
from demo_bad_code import process_payments

items = [{'price': i} for i in range(20)]

start = time.time()
total = process_payments(items)
end = time.time()
print(f"Total time: {end - start:.4f}s")
