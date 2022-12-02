from flask import jsonify
from app.scripts import\
monero_checkincomming,\
monero_createaccount,\
monero_deletewalletwork,\
monero_full_accounts,\
monero_getbalanceaccounts,\
monero_getblockcount,\
monero_sendcoin
from app import app

# End Models


@app.route('/', methods=['GET'])
def get_wallet_status():
    """
    Check is wallet is online
    :return:
    """

    return jsonify({
        "wallet_status": 'Monero Wallet is Online',
    })

@app.route('/deletework', methods=['GET'])
def delete_work():
    """
    Deletes old database entries
    :return:
    """
    monero_deletewalletwork.deleteoldorder()

    return jsonify({
        "wallet_status": 'Deleted Work',
    })


@app.route('/getbalanceaccounts', methods=['GET'])
def get_balance_accounts():
    """
    Gets the balance of account 2
    Lists the accounts
    :return:
    """
    #monero_getbalanceaccounts.getaddresses()
    monero_getbalanceaccounts.getbalance(2)
    monero_getbalanceaccounts.gettheaccounts()

    return jsonify({
        "wallet_status": 'Getting Block Couint',
    })

@app.route('/getblockcount', methods=['GET'])
def get_block_count():
    """
    Gets the count of how many blocks
    :return:
    """
    monero_getblockcount.main()

    return jsonify({
        "wallet_status": 'Getting Block Couint',
    })

@app.route('/createaccount', methods=['GET'])
def create_accounts():
    """
    Creates accounts for users
    :return:
    """
    monero_createaccount.main()
    
    return jsonify({
        "wallet_status": 'Getting Block Couint',
    })


@app.route('/send', methods=['GET'])
def send_coin():
    """
    send coin offsite
    :return:
    """
    
    monero_sendcoin.main()
    
    return jsonify({
        "status": 'sent coin',
    })

@app.route('/recieve', methods=['GET'])
def recieve_coin():
    """
     check for incomming coin
    :return:
    """
    monero_checkincomming.find_new_deposits(blockbacklog=100)
    
    return jsonify({
        "status": 'sent coin',
    })



@app.route('/checkaccounts', methods=['GET'])
def check_accounts():
    """
    This will check accounts to make sure no empty addresses
    :return:
    """
    
    monero_full_accounts.main()
    
    return jsonify({
        "status": 'Checked Accounts',
    })

