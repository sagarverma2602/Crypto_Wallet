from accounts.models import UserModel

def AddUser(username , password) :

    user = UserModel(username=username, password= password)
    user.save()

