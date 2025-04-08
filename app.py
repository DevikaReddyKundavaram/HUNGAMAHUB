from flask import Flask, render_template, request, jsonify, session
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import io
import base64
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for, flash
from flask import session
from flask import Flask
from config import Config
from extensions import db
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import User

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'

    # 🔗 Database Config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # 👇 All routes inside here
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            if User.query.filter_by(email=email).first():
                flash("Email already exists.")
                return redirect(url_for('register'))

            hashed_pw = generate_password_hash(password)
            new_user = User(name=name, email=email, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()

            session['username'] = name
            session['email'] = email
            return redirect(url_for('chat'))

        return render_template('register.html')


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                session['username'] = user.name
                session['email'] = user.email
                return redirect(url_for('chat'))
            else:
                flash("Invalid credentials")
                return redirect(url_for('login'))

        return render_template('login.html')


    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    df = pd.read_csv('games_dataset.csv')
    df.fillna('', inplace=True)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/group_by_occasion')
    def group_by_occasion():
        grouped = df.groupby('occasion').apply(lambda x: x.to_dict(orient='records')).to_dict()
        return render_template('group_by_occasion.html', grouped=grouped)

    @app.route('/group_by_genre')
    def group_by_genre():
        grouped = df.groupby('genre').apply(lambda x: x.to_dict(orient='records')).to_dict()
        return render_template('group_by_genre.html', grouped=grouped)

    @app.route('/grouped_multi')
    def grouped_multi():
        grouped = df.groupby(['occasion', 'game_type']).apply(lambda x: x.to_dict(orient='records')).to_dict()
        return render_template('grouped_multi.html', grouped=grouped)

    @app.route('/clusters')
    def clusters():
        df_cluster = df.copy()

        # Encode categorical features
        le_occasion = LabelEncoder()
        le_genre = LabelEncoder()
        le_game_type = LabelEncoder()

        df_cluster['occasion_encoded'] = le_occasion.fit_transform(df_cluster['occasion'])
        df_cluster['genre_encoded'] = le_genre.fit_transform(df_cluster['genre'])
        df_cluster['game_type_encoded'] = le_game_type.fit_transform(df_cluster['game_type'])

        kmeans = KMeans(n_clusters=5, random_state=42)
        df_cluster['cluster'] = kmeans.fit_predict(
            df_cluster[['occasion_encoded', 'genre_encoded', 'game_type_encoded']]
        )

        # Create the scatter plot
        plt.figure(figsize=(8, 5))
        plt.scatter(df_cluster['genre_encoded'], df_cluster['game_type_encoded'], c=df_cluster['cluster'], cmap='tab10')
        plt.title('Game Clusters')
        plt.xlabel('Genre')
        plt.ylabel('Game Type')

        # Save plot to base64
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        grouped_clusters = df_cluster.groupby('cluster').apply(lambda x: x.to_dict(orient='records')).to_dict()

        return render_template('clusters.html', clusters=grouped_clusters, plot_url=plot_url)

    @app.route('/popular_games')
    def popular_games():
        df_copy = df.copy()
        df_copy['popularity_rating'] = pd.to_numeric(df_copy['popularity_rating'], errors='coerce')
        df_valid = df_copy[df_copy['popularity_rating'].apply(lambda x: isinstance(x, float))]
        top_games = df_valid.sort_values(by='popularity_rating', ascending=False).head(15)
        games_data = top_games.to_dict(orient='records')
        return render_template('popular_games.html', games=games_data)

    chat_state = {
        'state': 'initial',
        'filters': {},
        'num_games': 5
    }

    unique_occasions = df['occasion'].dropna().unique().tolist()
    unique_age_groups = df['age_group'].dropna().unique().tolist()
    unique_group_types = df['game_type'].dropna().unique().tolist()

    @app.route('/chat')
    def chat():
        if 'username' not in session:
            return redirect(url_for('login'))
        return render_template('chat.html', username=session['username'])


    @app.route('/chatbot', methods=['POST'])
    def chatbot():
        data = request.get_json()
        user_input = data.get('user_input', '').strip()
        state = data.get('state', 'initial')
        filters = data.get('filters', {})

        handler = chatbot_logic(user_input, state, filters)
        return jsonify(handler)

    def chatbot_logic(user_input, state, filters):
        response = ""
        next_state = state
        options = []

        if state == 'initial':
            if user_input.lower() == 'yes':
                response = "Great! First, select an occasion:"
                options = unique_occasions
                next_state = 'awaiting_occasion'
            else:
                response = "No worries! I'm here if you change your mind."
                next_state = 'done'

        elif state == 'awaiting_occasion':
            if user_input in unique_occasions:
                filters['occasion'] = user_input
                response = "Awesome! Now, pick an age group:"
                options = unique_age_groups
                next_state = 'awaiting_age_group'
            else:
                response = "Please select a valid occasion."
                options = unique_occasions

        elif state == 'awaiting_age_group':
            if user_input in unique_age_groups:
                filters['age_group'] = user_input
                response = "Cool! Now, choose the group type (e.g., friends, family, corporate):"
                options = unique_group_types
                next_state = 'awaiting_group_type'
            else:
                response = "Please choose a valid age group."
                options = unique_age_groups

        elif state == 'awaiting_group_type':
            if user_input in unique_group_types:
                filters['game_type'] = user_input
                response = "How many game suggestions would you like to see?"
                next_state = 'awaiting_game_count'
            else:
                response = "Please select a valid group type."
                options = unique_group_types

        elif state == 'awaiting_game_count':
            try:
                count = int(user_input)
                filtered = df[
                    (df['occasion'] == filters['occasion']) &
                    (df['age_group'] == filters['age_group']) &
                    (df['game_type'] == filters['game_type'])
                ]
                if filtered.empty:
                    response = "Oops! No games match those filters. Try again with different options."
                    next_state = 'initial'
                    filters = {}
                else:
                    filtered['popularity_rating'] = pd.to_numeric(filtered['popularity_rating'], errors='coerce')
                    filtered = filtered.dropna(subset=['popularity_rating'])
                    top_games = filtered.sort_values(by='popularity_rating', ascending=False).head(count)
                    response = "Here are your game suggestions:<br><br>"
                    for i, game in enumerate(top_games.to_dict(orient='records'), 1):
                        response += f"<b>{i}. {game['game_name']}</b><br>"
                        response += f"🎯 {game['description']}<br>"
                        response += f"📦 Items Needed: {game['items_needed']}<br>"
                        response += f"⭐ Popularity: {game['popularity_rating']}<br><br>"
                    next_state = 'done'
            except ValueError:
                response = "Please enter a valid number."

        else:
            response = "Let's start over. Do you want me to suggest games?"
            options = ['Yes', 'No']
            next_state = 'initial'
            filters = {}

        return {
            'response': response,
            'state': next_state,
            'filters': filters,
            'options': options
        }

    return app

# Only run when NOT imported
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)



