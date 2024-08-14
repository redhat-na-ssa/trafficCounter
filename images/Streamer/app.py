from flask import Flask, send_from_directory, request

app = Flask(__name__)

@app.route('/stream/<path:filename>')
def stream(filename):
    return send_from_directory('videos', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
