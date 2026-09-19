from flask import Flask
import requests

app = Flask(__name__)

@app.route('/api/Go', methods=['POST'])
def one_command():
    data = request.json
    command = data.get('command')
    if command == 'Go':
        return('Yes')

if __name__ == '__main__':
    app.run(host='192.168.0.75', port=5000, debug=True)