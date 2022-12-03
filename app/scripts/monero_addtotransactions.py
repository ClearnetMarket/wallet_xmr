from datetime import datetime

from app import db
from app.classes.wallet_xmr import Xmr_Transactions


def xmr_add_transaction(category,amount,user_id, txid, block,balance,confirmed,fee, address):
    """
    # this function adds the transaction recording
    :param category:
    :param amount:
    :param user_id:
    :param txid:
    :param block:
    :param balance:
    :param confirmed:
    :param fee:
    :param address:
    :return:
    """

    now = datetime.utcnow()

    trans = Xmr_Transactions(
        category=category,
        user_id=user_id,
        confirmations=0,
        confirmed=confirmed,
        txid=str(txid),
        amount=amount,
        balance=balance,
        block=int(block),
        created=now,
        address=address,
        note=None,
        fee=fee,
        item_uuid=None,
        digital_currency=3,
        order_uuid=None
    )
    db.session.add(trans)
    db.session.commit()

