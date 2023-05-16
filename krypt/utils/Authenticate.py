from accounts.models import UserModel

def authenticate(username , password , confirm_password) :
    return password == confirm_password or UserModel.objects.filter(username=username).exists()
    

def loginAuthenticate(username , password) :
    if UserModel.objects.filter(username=username).exists() :
        user = UserModel.objects.get(username=username)
        if user.password == password :
            return (True , user)
    return (False , None)