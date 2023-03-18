import requests
from requests.auth import HTTPDigestAuth
import json
from app import db, rpcpassword, rpcusername, url

from app.classes.wallet_xmr import Xmr_BlockHeight


###
# This script updates blocks in order to define confirmations as human readable
##

def getblockheight():

    # standard json header
    headers = {'content-type': 'application/json'}

    rpc_input = {
        "method": "get_height",
    }

    # add standard rpc values
    rpc_input.update({"jsonrpc": "2.0", "id": "0"})

    # execute the rpc request
    response = requests.post(
        url,
        data=json.dumps(rpc_input),
        headers=headers,
        auth=HTTPDigestAuth(rpcusername, rpcpassword))
    response_json = response.json()
    print(response_json)
    return response_json


def main():
    response_json = getblockheight()

    if response_json["result"]['height'] > 1:

        lastheight = response_json["result"]['height']

        lastblockheight = db.session\
            .query(Xmr_BlockHeight)\
            .get(1)
        lastblockheight.blockheight = int(lastheight)

        db.session.add(lastblockheight)

        db.session.commit()


