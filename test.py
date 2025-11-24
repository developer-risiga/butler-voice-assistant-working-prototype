print("Testing Butler...")

import os

print("Checking if files exist:")
print("config.py exists:", os.path.exists("src/config/config.py"))
print("logger.py exists:", os.path.exists("src/utils/logger.py"))

if os.path.exists("src/config/config.py"):
    print("✅ config.py is found!")
else:
    print("❌ config.py is missing!")

if os.path.exists("src/utils/logger.py"):
    print("✅ logger.py is found!")
else:
    print("❌ logger.py is missing!")