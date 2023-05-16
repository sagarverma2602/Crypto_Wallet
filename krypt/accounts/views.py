from django.shortcuts import render
from utils.Authenticate import authenticate
from utils.Authenticate import loginAuthenticate
from UserDAO.UserDAO import AddUser
from django.contrib.sessions import middleware
from django.http import JsonResponse
import requests
from datetime import datetime
from utils.filterPrices import filterPrices 
from EthiriumAccount import ethiriumAccount as ea

def login_view(request):
    if request.method == 'POST':
        # Handle the login form submission
        username = request.POST['username']
        password = request.POST['password']
        # Perform authentication and redirect as needed
        # Replace the placeholder logic with your actual authentication implementation
        valid , user = loginAuthenticate(username, password)
        if valid :
            request.session['username'] = user.username
            request.session['ethaddress'] = user.Ethaddress
            request.session['ethprivatekey'] = user.Ethprivatekey
           
            # Render the login template
            return render(request, 'welcome.html')

        return render(request, 'home.html')
# Create your views here.


def register_view(request) :
    return render(request, 'registerpage.html')

def registeruser_view(request) :
    if request.method == 'POST':
        # Handle the login form submission
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if (authenticate( username , password , confirm_password)) :
            AddUser(username , password)
            
           
    return render(request, 'home.html')
   
        

def createNewEthAccount_view(request) :

    username = request.session.get('username')
    private_key = request.POST.get('private_key')
    
    saddress = request.POST.get('s_address')
    
    key , add = ea.createNewEthAccount(username , private_key , saddress)
    request.session['username'] = username
    request.session['ethaddress'] = add
    request.session['ethprivatekey'] = key

    return render(request, 'welcome.html')


def EthiriumTransaction_view(request) :
    if request.method == 'POST':
        username = request.session.get('username')
        receiver_address = request.POST.get('r_address')
        amount = request.POST.get('amount')


        if ea.etheriumTransaction(username , receiver_address , amount) :
            return render(request, 'welcome.html')
        else :
            return render(request, 'welcome.html' , {'error' : "failed !!"})




def getBalance_view(request) :
    
    private_key = request.session.get('ethprivatekey')
    if private_key:
        # Code to retrieve balance using private key
        balance = ea.getBalance(private_key)  # Replace with your own implementation
        
       
        # Return balance as JSON response
        return JsonResponse({'balance': balance})
    else:
        return JsonResponse({'error': 'Private key not found'})


def getTransactions_view(request) :
    private_key = request.session.get('ethprivatekey')
    if private_key:
        transactions = ea.getTransactions(private_key)
        return JsonResponse({'transactions' : transactions})

    else :

        return JsonResponse({'error': 'Private key not found'})


def logout(request) :
    request.session.clear()
    return render(request, 'home.html')


def getPrices(request) :
    end_date = int(datetime.now().timestamp())
    start_date = end_date - 3600 
    
    url = f"https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range?vs_currency=usd&from={start_date}&to={end_date}"
    response = requests.get(url)
    

    if response.status_code == 200:
        price_data = response.json()
        ethereum_prices = []
        ethereum_prices = price_data["prices"]
        json_data = filterPrices(ethereum_prices)
        return JsonResponse({"json_data" : json_data})
    else:
        return JsonResponse({'error': 'Failed to fetch price data'}, status=500)


def unlink(request) :
    username = request.session.get("username")
    
    request.session['ethaddress'] = "NA"
    request.session['ethprivatekey'] = "NA"
    ea.unlink(username)
    
    return render(request, 'welcome.html')
    