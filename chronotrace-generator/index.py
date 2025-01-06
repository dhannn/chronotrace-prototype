from flask import Flask, jsonify, url_for, render_template, make_response
from flask_cors import CORS, cross_origin
from totp_generator import *

app = Flask(__name__)

# IP_ADDRESS = 'http://192.168.0.23:80'
IP_ADDRESS = 'http://10.254.133.34:80'
CORS(app, resources={r"/*": {"origins": IP_ADDRESS}})

@app.route("/")
@cross_origin()
def hello_world():
    return render_template('index.html')

@app.route('/log/<student_id>/token/<token>', methods=['POST'])
@cross_origin()
def log(student_id, token):
    print(student_id, token)
    if validate_entry(student_id, token):
        user_info = db.add_entry(student_id, uuid.uuid4())
        return user_info, 200
    else:
        return '404', 404
        

@app.route('/token/<token>', methods=['GET'])
@cross_origin()
def test(token):  
    data = {'is_valid': validate_entry('12131369', token) }
    resp = make_response(data, 200)
    return resp
    
@app.route('/qr-code')
def get_qr_code():
    totp = get_totp()
    generate_qr_code(totp)
    url_for('static', filename=f'qr-{totp['token']}.png')
    return totp['token']

if __name__ == "__main__":
    app.run(ssl_context=('certs/server-cert.pem', 'certs/server-key.pem'), host='0.0.0.0')
