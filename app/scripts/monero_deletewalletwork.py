from app import db
from app.classes.wallet_xmr import Xmr_WalletWork

# run once every ten minutes
def deleteoldorder():

    getwork = db.session\
        .query(Xmr_WalletWork)\
        .filter_by(type=0)\
        .all()
    for f in getwork:
        db.session.delete(f)
    db.session.commit()


