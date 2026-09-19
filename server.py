from flask import Flask, request, jsonify, render_template
import requests
import psycopg2



robot_ip = '192.168.0.75'
robot_port = 5000

art = r"""
  ____  _ _       _               ____            _                 
 |  _ \(_) | ___ | |_ _   _ ___  / ___| _   _ ___| |_ ___ _ __ ___  
 | |_) | | |/ _ \| __| | | / __| \___ \| | | / __| __/ _ \ '_ ` _ \ 
 |  __/| | | (_) | |_| |_| \__ \  ___) | |_| \__ \ ||  __/ | | | | |
 |_|   |_|_|\___/ \__|\__,_|___/ |____/ \__, |___/\__\___|_| |_| |_|
                                        |___/                                

                        []Code by ARrZoNe[]
                        Version: Beta 1.0                                                           
"""
print(art)

app = Flask(__name__)

@app.route("/")

def index():
    return render_template('main.html')

@app.route("/map")

def map():
    return render_template('map.html')

@app.route("/start", methods = ['POST'])

def start():
    try:
        responce = requests.post(
            f'http://{robot_ip}:{robot_port}/api/Go',
            json={'command':'Go'}
        )
        return f"good"
    except:
        return f"bad connection error"

def init_database():
    conn = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWD
    )
    c=conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS robot (id TEXT)')
    conn.commit()
    conn.close()


def add_robot():
    conn = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWD
    )
    c=conn.cursor()
    c.execute('INSERT INTO robots (id) VALUES (%?)', (robot_id,))
    conn.commit()
    conn.close()
def test(): 
    add_robot('robot_1')
    return("flag")



if __name__ == "__main__":
    app.run(host="192.168.0.83", port=5000)

