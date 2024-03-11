import jwt
import cherrypy
from Utils.Utils import colorPrinter
from config import SECRET_KEY


@cherrypy.tools.register('before_handler')
def check_jwt():
    colorPrinter("CHECK JWT TOKEN", "green")
    print(cherrypy.request.headers)
    token = "yes"
    token = cherrypy.request.headers.get('authorization').split(' ')[1]
    colorPrinter(token, "red")
    if not token:
        raise cherrypy.HTTPError(400, 'You must provide JWT token')
    try:
        info = jwt.decode(token, SECRET_KEY, algorithm='HS256')
    except jwt.ExpiredSignatureError:
        raise cherrypy.HTTPError(400, 'Expired Token')
    except jwt.DecodeError:
        raise cherrypy.HTTPError(400, 'Invalid Token')
    except:
        raise cherrypy.HTTPError(500, 'System Internal Error')
    else:
        return "CHECK  IN DATABASE IF PAYLOAD IS OK AND RETURN TO ROUTE"