 to talk to your Pi
import os

app = Flask(__name__)
CORS(app) # This allows external websites to send commands to this Pi

@app.route('/drive')
def drive():
    action = request.args.get('action')
    
    if action == "forward":
        # INSERT MOTOR CODE HERE
        return "Car Moving Forward"
    elif action == "stop":
        # INSERT MOTOR STOP CODE HERE
        return "Car Stopped"
    
    return "Unknown Command"

if __name__ == '__main__':
    # '0.0.0.0' makes the Pi listen to everyone on your Wi-Fi network
    app.run(host='0.0.0.0', port=5000)
