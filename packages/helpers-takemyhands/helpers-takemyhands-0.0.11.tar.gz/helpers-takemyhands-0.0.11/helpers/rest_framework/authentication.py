import jwt
from rest_framework import authentication
from rest_framework import exceptions


SECRET_KEY = "t3wL3gsUnM#XHbC&?(vyq9qHN/hZ3Tg'ffHUHRT9&({bS2t=^Rk9d2"

class JWTAuthentication(authentication.BaseAuthentication):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs["user"]
    
    def authenticate(self, request):
        try:
            if self.user:
                token = request.META.get("HTTP_AUTHORIZATION")
                if token is None:
                    return None

                xjwt, encoded_jwt = token.split(" ")
                decoded = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=["HS256"])
                pk = decoded.get("pk")
                user = user.objects.get(pk=pk)
                
                return (user, None)
            else:
                return None


        except ValueError:
            raise exceptions.AuthenticationFailed(detail="Value error")

        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed(detail="JWT Format invalid")

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(detail="No such user")

        except Exception as e:
            raise e