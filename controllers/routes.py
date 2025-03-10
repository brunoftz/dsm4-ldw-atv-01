import urllib.request
import json
from flask import render_template, request, redirect, url_for

# Store your characters (assuming you want to keep track of added ones)
personagens = []
plist = []

def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/jogo', methods=['GET', 'POST'])
    def jogo():
        if request.method == 'POST':
            if request.form.get('personagem'):
                personagens.append(request.form.get('personagem'))
                return redirect(url_for('jogo'))
            
        return render_template('jogo.html', personagens=personagens)
    
    @app.route('/cadpersonagens', methods=['GET', 'POST'])
    def cadpersonagens():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            plist.append(form_data)
            return redirect(url_for('cadpersonagens'))
        return render_template('cadpersonagens.html', plist=plist)
    
    @app.route('/apidbz', methods=['GET', 'POST'])
    @app.route('/apidbz/<int:id>', methods=['GET', 'POST'])
    def apidbz(id=None):
        url = 'https://dragonball-api.com/api/characters'
        res = urllib.request.urlopen(url)
        data = res.read()
        dbzjson = json.loads(data)

        if id:
            # Find character by ID from the 'items' list
            p_info = next((persona for persona in dbzjson['items'] if persona['id'] == id), None)

            if p_info:
                return render_template('p_info.html', p_info=p_info)
            else:
                return f'Personagem com a ID {id} não foi encontrado.'

        return render_template('apidbz.html', dbzjson=dbzjson)

