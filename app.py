from flask import Flask, render_template, request
import os
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'

def parse_key_string(key_str):
    key_map = {}
    pairs = key_str.lower().split(',')
    for pair in pairs:
        if ':' in pair:
            k, v = pair.split(':')
            key_map[k.strip()] = v.strip()
    return key_map

def mono_encrypt(text, key_map):
    result = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                result += key_map.get(char, char)
            else:
                result += key_map.get(char.lower(), char).upper()
        else:
            result += char
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    encrypted_text = ""
    keymap = ""
    plaintext = ""

    if request.method == 'POST':
        plaintext = request.form.get('plaintext', '')
        keymap = request.form.get('keymap', '')
        try:
            key_dict = parse_key_string(keymap)
            encrypted_text = mono_encrypt(plaintext, key_dict)
        except Exception as e:
            encrypted_text = f"⚠️ خطأ في مفتاح التشفير: {e}"

    return render_template('index.html', encrypted=encrypted_text, keymap=keymap, plaintext=plaintext)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
