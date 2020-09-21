from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Details
from bitcoin import *
import bs4
import requests

# Create your views here.
def index(request):

    if request.method == 'POST':
        addr = request.POST['addr']
        res2 = requests.get('https://cryptowat.ch/')
        soup2 = bs4.BeautifulSoup(res2.text, 'lxml')
        live_price = soup2.find_all('span', {'class': 'price'})
        live_bitcoin_price = live_price[1].getText()
        live_bitcoin_price1 = live_price[1].getText()
        res = requests.get('https://www.blockchain.com/btc/address/'+addr)
        if res:
            soup = bs4.BeautifulSoup(res.text, 'lxml')
            # bal = soup.find_all('span', {'class': 'sc-1ryi78w-0 bFGdFC sc-16b9dsl-1 iIOvXh u3ufsr-0 gXDEBk'})
            bal = soup.find_all('span', {'class': 'sc-1ryi78w-0 gCzMgE sc-16b9dsl-1 kUAhZx u3ufsr-0 fGQJzg'})
            bal[4].getText()
            final_bal = bal[4].getText()
            final_bal1 = final_bal.replace(" ", "").rstrip()[:-3].upper()
            transactions = bal[1].getText()
            total_received = bal[2].getText()
            total_received1 = total_received.replace(" ", "").rstrip()[:-3].upper()
            total_sent = bal[3].getText()
            total_sent1 = total_sent.replace(" ", "").rstrip()[:-3].upper()
            final_bal1_int = float(final_bal1)
            total_received1_int = float(total_received1)
            total_sent1_int = float(total_sent1)
            live_bitcoin_price1_int = float(live_bitcoin_price1)
            
            balance_usd = final_bal1_int*live_bitcoin_price1_int
            total_received_usd = total_received1_int*live_bitcoin_price1_int
            total_sent_usd = total_sent1_int*live_bitcoin_price1_int
        else:
            return redirect('/')

        detail = Details()
        detail.balance = final_bal
        detail.balance1 = final_bal1
        detail.transactions = transactions
        detail.total_received = total_received
        detail.total_received1 = total_received1
        detail.total_sent = total_sent
        detail.total_sent1 = total_sent1
        detail.live_bitcoin_price = live_bitcoin_price
        detail.live_bitcoin_price1 = live_bitcoin_price1
        detail.balance_usd = int(balance_usd)
        detail.total_received_usd = int(total_received_usd)
        detail.total_sent_usd = int(total_sent_usd)


    else:
        detail = '   '

    return render(request, 'index.htm', {'detail' : detail})

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')

    else:
        return render(request, 'login.htm')

def register(request):

    detail = Details()
    private_key = random_key()
    public_key = privtopub(private_key)
    address = pubtoaddr(public_key)
    detail.private_key = private_key
    detail.public_key = public_key
    detail.address = address


    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        private_key = request.POST['private_key']
        public_key = request.POST['public_key']
        address = request.POST['address']

        if password==password2:       
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, last_name=private_key, first_name=address)
                user.save();
                print('User Created')
                return redirect('login')

        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')
        return redirect('/')

    else:
        return render(request, 'register.htm', {'detail': detail})
def logout(request):
    auth.logout(request)
    return redirect('/')