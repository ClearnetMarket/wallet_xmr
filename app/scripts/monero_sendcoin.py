import requests
from decimal import Decimal
from requests.auth import HTTPDigestAuth
import json
from walletconfig import rpcpassword, rpcusername, url
from app import db
from monero_addtotransactions import \
    xmr_add_transaction
from monero_helper_functions import \
    get_money, \
    get_amount
from app.classes.wallet_xmr import\
    Xmr_WalletWork,\
    Xmr_BlockHeight, \
    Xmr_Wallet


# standard json header
headers = {'content-type': 'application/json'}


def getwalletofperson(userid):
    """
    GEts a users wallet by id
    :param userid:
    :return: sql query of user row
    """
    getuserswallet = db.session\
        .query(Xmr_Wallet) \
        .filter(Xmr_Wallet.user_id == userid) \
        .first()
    return getuserswallet


def getblockheight():
    """
    Gets value from database of last block height
    Used to perform calculations of wallet transactions
    :return: returns an sql row
    """
    lastblockheight = db.session\
        .query(Xmr_BlockHeight)\
        .get(1)
    return lastblockheight


def add_error(f, response_json):

    if response_json["result"]['error']:
        if response_json["result"]['error']['message']:
            if response_json["result"]['error']['message'] == 'not enough unlocked money':
                f.type = 300
            else:
                f.type = 304
        else:
            f.type = 300

        db.session.add(f)


def sendcoin(sendto, amount):
    """
    This will send the coin.
    If it fails turn the work to 105 for error
    Update send transaction with txid

    """
    destination_address = str(sendto)

    int_amount = int(get_amount(amount))

    # just to make sure that amount->coversion->back
    # gives the same amount as in the initial number
    assert amount == Decimal(get_money(str(int_amount))), \
        "Amount conversion failed"

    # send specified xmr amount to the given destination_address
    recipents = [{"address": destination_address,
                  "amount": int_amount}]

    # using given mixin
    mixin = 5

    # get some random payment_id

    rpc_input = {
        "method": "transfer",
        "params": {"destinations": recipents,
                   "mixin": mixin,
                   "account_index": 2
                   }
    }

    # add standard rpc values
    rpc_input.update({"jsonrpc": "2.0", "id": "0"})

    # execute the rpc request
    response = requests.post(
        url,
        data=json.dumps(rpc_input),
        headers=headers,
        auth=HTTPDigestAuth(rpcusername, rpcpassword))

    # pretty print json output
    response_json = response.json()
    print(json.dumps(response_json, indent=4))

    return response_json


def add_transaction(f, sendto, amount, user_id):

    userswallet = getwalletofperson(userid=user_id)
    response_json_send = sendcoin(sendto=sendto,
                                  amount=amount,
                                  )
    # see if successful
    amountsend = response_json_send["result"]['amount']
    if amountsend:
        if amountsend > 0:
            theblockheight = getblockheight()

            thetxid = response_json_send["result"]['tx_hash']
            feefromtx = response_json_send["result"]['fee']
            thefee = Decimal(get_money(str(feefromtx)))

            xmr_add_transaction(category=2,
                                  amount=amount,
                                  user_id=f.user_id,
                                  txid=thetxid,
                                  block=theblockheight.blockheight,
                                  balance=userswallet.currentbalance,
                                  confirmed=1,
                                  fee=thefee,
                                  address=sendto
                                  )

            f.type = 0
            db.session.add(f)
            db.session.commit()
            print("sent coin work completed")

    elif response_json_send["result"]['error']:
        print("error!")
        print(response_json_send)
        add_error(f, response_json_send)

        newbalance = userswallet.currentbalance + amount
        userswallet.currentbalance = newbalance
        db.session.add(userswallet)

    else:
        pass


def main():
    """
    this will look for work to do.
      setup to provice furture expansion
    type 1: send coin offsite
    type 2: create a wallet

    """

    work = db.session\
        .query(Xmr_WalletWork) \
        .filter(Xmr_WalletWork.type == 1) \
        .order_by(Xmr_WalletWork.created.desc()) \
        .all()

    if not work:
        print("No outgoing transactions")
    else:
        for f in work:
            add_transaction(f,
                            sendto=f.sendto,
                            amount=f.amount,
                            user_id=f.user_id
                            )
        db.session.commit()



if __name__ == '__main__':
    main()
