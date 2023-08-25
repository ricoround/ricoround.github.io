from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, send, emit
import qrcode
import os
from io import BytesIO
import base64
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

def generate_qr(code):
    memory = BytesIO()
    # img = qrcode.make(request.base_url + '/' + str(code))
    img = qrcode.make(code)
    img.save(memory)
    memory.seek(0)

    base64_img = "data:image/png;base64," + \
        base64.b64encode(memory.read()).decode('ascii')
    
    return base64_img

# Generate a random secret code for this session (you should use a more secure method)
secret_code = str(random.randint(0000, 9999))

# The TV website route for generating QR code and handling URL submissions
@app.route('/')
def index():
    device_url = request.base_url + 'device?code=' + secret_code
    qr_code = generate_qr(device_url)
    return render_template('index.html', secret_code=secret_code, qr_code=qr_code)

@app.route('/device')
def device():
    return render_template('device.html')

@socketio.on('message_device2tv')
def handle_message(data):
    print(data)
    user_secret_code = data['secret_code']
    print("--------", user_secret_code, secret_code, "--------")
    
    # Verify that the secret code matches the one generated earlier
    if user_secret_code == secret_code:
        url = data['url']
        print(url)
        emit('message_from_server', url, broadcast=True)
    else:
        emit('unauthorized', {}, broadcast=False)



# @socketio.on('message_device2tv')
# def handle_message(data):
#     url = data['url']
#     print(url)
#     emit('message_from_server', url, broadcast=True)

# @app.route('/page2')
# def page2():
#     return render_template('page2.html')

if __name__ == '__main__':
    socketio.run(app)






# @app.route('/')
# def index():
#     return render_template('index.html')



# @app.route('/tvqr')
# def tvqr():
#     # Generate random 5 digit number
#     code = random.randint(00000, 99999)
#     base64_img = generate_qr(code)

#     return render_template('tvqr.html', code=code, qr_code=base64_img)

# @app.route('/tvqr/<code>')
# def tvqr_code(code):
#     base64_img = generate_qr(code)
#     return render_template('tvqr.html', code=code, qr_code=base64_img)


# @app.route('/tvqr/process_url', methods=['GET'])
# def process_url():
#     user_input_url = request.args.get('url')
    
#     # Validate the user input URL here
    
#     # Perform the redirect
#     print(user_input_url)
#     return redirect(user_input_url)












if __name__ == '__main__':

    
    app.run(debug=True)