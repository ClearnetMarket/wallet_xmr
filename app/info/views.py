from flask import jsonify, Response
from app.info import info


# End Models


@info.route('/status', methods=['GET'])
def vendor_topbar_get_issues_count():
    """
    Resturns stats of info
    :return:
    """
    return jsonify({
        "wallet_status": 'not yet set up',
    })
