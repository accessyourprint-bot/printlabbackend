from app.core.security import verify_password
hash_value = "$2b$12$ZNVVaeXshO0hqMH/COkjIeWK7NffF4ME340NSPoRjLbWSxrRDfQHO"
print(verify_password("Test1234!", hash_value))
