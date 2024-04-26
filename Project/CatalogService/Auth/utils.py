import jwt
from CatalogService.Auth.config import SECRET_KEY
from CatalogService.Utils.Utils import colorPrinter

def encode_token(password):
    return jwt.encode({"password": password}, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded["password"]
    except Exception as e:
        colorPrinter(str(e), "red")
        return None
    
def check_token(token):
    return decode_token(token) is not None

def check_user_password(userId, password):
    return True
    # return user["password"] == decode_token(password)["password"]

# if __name__ == '__main__':
#     password = "123456789"
#     encoded = encode_token(password)
#     decoded = decode_token(encoded)
#     colorPrinter(str(encoded), "green")
#     colorPrinter(str(decoded), "blue")
#     colorPrinter(str(password == decoded), "green")
#     colorPrinter(str(check_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXNzd29yZCI6IjEyMzQ1Njc4OSJ9.ogzCuLktEiTFgg2Y7-kypB0N5TnABXJ8Mu40XVvPVqg')), "red")
 