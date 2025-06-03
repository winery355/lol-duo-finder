from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

def load_profiles():
    if os.path.exists('duo_profiles.json'):
        with open('duo_profiles.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_profiles(profiles):
    with open('duo_profiles.json', 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    mode_filter = request.args.get('mode')
    profiles = load_profiles()

    if mode_filter in ['SoloQ', 'Flex']:
        profiles = [p for p in profiles if p['mode'] == mode_filter]

    return render_template('index.html', profiles=profiles, mode_filter=mode_filter)

@app.route('/add_profile', methods=['POST'])
def add_profile():
    profile = {
        'nickname': request.form['nickname'],
        'role': request.form['role'],
        'mode': request.form['mode']
    }

    profiles = load_profiles()
    profiles.append(profile)
    save_profiles(profiles)

    return redirect(url_for('index'))

@app.route('/delete_profile/<int:index>', methods=['POST'])
def delete_profile(index):
    profiles = load_profiles()
    if 0 <= index < len(profiles):
        profiles.pop(index)
        save_profiles(profiles)
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Iniciando LoL Duo Finder...")
    app.run(debug=True)
