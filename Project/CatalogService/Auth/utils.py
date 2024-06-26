import jwt
from Auth.config import SECRET_KEY
from Utils.Utils import colorPrinter

def encode_token(password):
    try:
        encoded_token = jwt.encode({"password": str(password)}, SECRET_KEY, algorithm='HS256')
        return encoded_token
    except Exception as e:
        print('Error encoding token:', e)
        colorPrinter(str(e), "red")
        return None

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
#     # encoded = encode_token(password)
#     encoded = jwt.encode({"password": str(password)}, SECRET_KEY, algorithm='HS256')
#     decoded = decode_token(encoded)
#     colorPrinter(str(encoded), "green")
#     colorPrinter(str(decoded), "blue")
#     colorPrinter(str(password == decoded), "green")
#     colorPrinter(str(check_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXNzd29yZCI6IjEyMzQ1Njc4OSJ9.ogzCuLktEiTFgg2Y7-kypB0N5TnABXJ8Mu40XVvPVqg')), "red")
 