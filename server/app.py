from flask import Flask, request, send_file, jsonify
from tools import base64_to_image
from database import set_stats, set_image, get_image, get_commands

app = Flask(__name__)

@app.route('/update-stats', methods=['POST'])
def update_stats():
    data: dict = request.get_json()
    
    if not any([data.get('temp'), data.get('lux')]):
        return 'Invalid request', 400
    
    else:
        set_stats(data.get('temp'), data.get('lux'))
        return 'OK', 200

@app.route('/update-image', methods=['POST'])
def update_image():
    data: dict = request.get_json()
    
    if not data.get('image'):
        return 'Invalid request', 400
    
    else:
        set_image(data.get('image'))
        return 'OK', 200

@app.route('/get-image', methods=['GET'])
def get_image():
    try:
        img_io = base64_to_image(get_image())
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='imagem.png')

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/get-commands', methods=['GET'])
def get_command():
    commands: tuple = get_commands()
    return jsonify({'heat': commands[0], 'lamp': commands[1]})

if __name__ == '__main__':
    app.run(debug=True)