from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import json
import random
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# ОЧЕНЬ ВАЖНО: Замените на реальный, сложный секретный ключ!
app.secret_key = os.environ.get("SECRET_KEY")

# Получаем абсолютный путь к директории, где находится app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SENTENCES_FILE = os.path.join(BASE_DIR, 'sentences.json')

@app.before_request
def set_default_language():
    """
    Устанавливает язык по умолчанию (en) если он не установлен в сессии.
    Это гарантирует, что session['lang'] всегда определен.
    """
    if 'lang' not in session:
        session['lang'] = 'en'

@app.route('/')
def home():
    """
    Обрабатывает корневой URL и отображает главную страницу.
    Передает текущий язык из сессии в шаблон.
    """
    current_lang = session.get('lang', 'en')
    return render_template('index3.html', lang=current_lang)

@app.route('/type')
def typing_trainer():
    """
    Обрабатывает URL /type и отображает страницу тренажёра печати.
    Передает текущий язык из сессии в шаблон.
    """
    current_lang = session.get('lang', 'en')
    return render_template('type.html', lang=current_lang)

@app.route('/set-language/<lang_code>')
def set_language(lang_code):
    """
    Устанавливает язык в сессии и перенаправляет пользователя на предыдущую страницу
    или на главную, если предыдущая страница неизвестна.
    """
    if lang_code in ['en', 'ru']: # Проверяем, что язык поддерживается
        session['lang'] = lang_code
    # Перенаправляем пользователя на ту же страницу, откуда пришел запрос
    return redirect(request.referrer or url_for('home'))

@app.route('/api/random-sentence')
def get_random_sentence():
    """
    Отдает одно случайное предложение из sentences.json на основе текущего языка из сессии.
    """
    current_lang = session.get('lang', 'en') # Получаем язык из сессии

    try:
        with open(SENTENCES_FILE, 'r', encoding='utf-8') as f:
            all_sentences = json.load(f)

        sentences_for_lang = all_sentences.get(current_lang)

        if sentences_for_lang:
            random_sentence = random.choice(sentences_for_lang)
            return jsonify({'sentence': random_sentence})
        else:
            # Если для запрошенного языка нет предложений (хотя не должно быть с текущим JSON),
            # попробуем вернуться к английскому.
            sentences_for_lang = all_sentences.get('en')
            if sentences_for_lang:
                random_sentence = random.choice(sentences_for_lang)
                return jsonify({'sentence': random_sentence, 'warning': f'No sentences for {current_lang}, returned English.'})
            else:
                return jsonify({'error': f'No sentences found for language {current_lang} or "en" in JSON file'}), 404
    except FileNotFoundError:
        return jsonify({'error': 'sentences.json not found'}), 500
    except json.JSONDecodeError:
        return jsonify({'error': 'Error decoding JSON from sentences.json'}), 500

@app.route('/privacy-policy')
def privacy_policy():
    """
    Обрабатывает URL /privacy-policy и отображает страницу политики конфиденциальности.
    Передает текущий язык из сессии в шаблон.
    """
    current_lang = session.get('lang', 'en')
    return render_template('privacy_policy.html', lang=current_lang)

@app.route('/terms-of-service')
def terms_of_service():
    """
    Обрабатывает URL /terms-of-service и отображает страницу условий обслуживания.
    Передает текущий язык из сессии в шаблон.
    """
    current_lang = session.get('lang', 'en')
    return render_template('terms_of_service.html', lang=current_lang)

# НОВЫЙ МАРШРУТ ДЛЯ СТРАНИЦЫ "О САЙТЕ"
@app.route('/about-us')
def about_us():
    """
    Обрабатывает URL /about-us и отображает страницу "О сайте".
    Передает текущий язык из сессии в шаблон.
    """
    current_lang = session.get('lang', 'en')
    return render_template('about_us.html', lang=current_lang)

if __name__ == '__main__':
    app.run(debug=True)