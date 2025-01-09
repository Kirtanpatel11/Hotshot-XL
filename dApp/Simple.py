from flask import flask, render_template
from web3 import Web3

app = Flask(__name__)

w3 = Web3(HTTPProvider('HTTP://127.0.0.1:7545'))

@app.route('/')

def index():
    return render_template("index.html")

    @app.route('/send', methods=['POST'])
    def send_transaction():
        from_address = request.form['from']
        to_address = request.form['to']
        value = request.form['value']
        private_key = request.form['private_key']

        transaction = {
            'to': to_address,
            'value': w3.toWei(value, ether),
            'gas':2000000,
            'gasPrice': w3.toWei('50', 'gwei')
            'nonce': we.eth.getTransactionCount(from_address),
        }
        signed_txn = w3.eth.account.signTransaction(Transaction, private_key) # Stamp

        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return f'transaction sent with hash': {txn_hash.hex()}

        if __name__ == '__main__':
            app.run(debug=True)