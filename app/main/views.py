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
    Gets the count of vendor order issues.  Notification bar at top
    :return:
    """

    return jsonify({
        "wallet_status": 'Monero Wallet is Online',
    })

@app.route('/deletework', methods=['GET'])
def delete_work():
    """
    Gets the count of how many blocks
    :return:
    """
    monero_deletewalletwork()

    return jsonify({
        "wallet_status": 'Deleted Work',
    })


@app.route('/getbalanceaccounts', methods=['GET'])
def get_balance_accounts():
    """
    Gets the count of how many blocks
    :return:
    """
    monero_getbalanceaccounts()

    return jsonify({
        "wallet_status": 'Getting Block Couint',
    })

@app.route('/getblockcount', methods=['GET'])
def get_block_count():
    """
    Gets the count of how many blocks
    :return:
    """
    monero_getblockcount()

    return jsonify({
        "wallet_status": 'Getting Block Couint',
    })

@app.route('/createaccount', methods=['GET'])
def create_accounts():
    """
    Gets the count of how many blocks
    :return:
    """
    monero_createaccount()
    return jsonify({
        "wallet_status": 'Getting Block Couint',
    })


@app.route('/send', methods=['GET'])
def send_coin():
    """
    This will activiate the script to send coin
    :return:
    """
    
    monero_sendcoin()
    
    return jsonify({
        "status": 'sent coin',
    })

@app.route('/recieve', methods=['GET'])
def recieve_coin():
    """
     This will activiate the script to check for incomming bitcoin
    :return:
    """
    monero_checkincomming()
    
    return jsonify({
        "status": 'sent coin',
    })



@app.route('/checkaccounts', methods=['GET'])
def check_accounts():
    """
    This will check accounts to make sure no empty addresses
    :return:
    """
    
    monero_full_accounts()
    
    return jsonify({
        "status": 'Checked Accounts',
    })

