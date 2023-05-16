from web3 import Web3
from eth_account import Account
from accounts.models import UserModel

ganache_url = "http://localhost:7545"  # Update with your Ganache URL
web3 = Web3(Web3.HTTPProvider(ganache_url))


def createNewEthAccount(username , private_key , s_address):

    
    # address = '0x35A1d37d8faD4c3b038149D9607115A9A2e94517'
    
    user = UserModel.objects.get(username=username)
    user.Ethaddress = s_address
    user.Ethprivatekey = private_key
    user.save()
    
    return (private_key, s_address)


def etheriumTransaction(username ,receiver_address , amount ) :

    user = UserModel.objects.get(username=username)
    
    transaction = {
    'to': receiver_address,
    'value': web3.to_wei(int(amount), 'ether'),  # Replace '1' with the amount of Ethereum to send
    'gas': 21000,  # Gas limit for a simple ETH transfer
    'gasPrice': web3.eth.gas_price,
    'nonce': web3.eth.get_transaction_count(user.Ethaddress),
    }

    signed_tx = web3.eth.account.sign_transaction(transaction, user.Ethprivatekey)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    transaction_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    status = transaction_receipt['status']

    if status == 1:
        return True
    else:
        return False


def getBalance(private_key) :
    account = web3.eth.account.from_key(private_key)
    balance = web3.eth.get_balance(account.address)
    balance_ether = web3.from_wei(balance, 'ether')
    
    return balance_ether


def getTransactions(private_key):
    account = web3.eth.account.from_key(private_key)
    address = account.address
    transaction_count = web3.eth.get_transaction_count(address)
    transactions = []
    block_number = web3.eth.block_number

    for i in range(block_number + 1):
        block = web3.eth.get_block(i)
        for transaction_hash in block.transactions:
            transaction = web3.eth.get_transaction(transaction_hash)
            if transaction and transaction["from"] == address:
                cleaned_transaction = clean_transaction(transaction)
                transactions.append(cleaned_transaction)

    # Return cleaned transactions
    
    return transactions


def clean_transaction(transaction):
    cleaned_transaction = {
       
        "From": transaction["from"],
        "To": transaction.to,
        "Value": web3.from_wei(transaction.value, "ether"),
     
    }
    return cleaned_transaction


def unlink(username) :

    user = UserModel.objects.get(username=username)
    user.Ethaddress = "NA"
    user.Ethaddress = "NA"
    