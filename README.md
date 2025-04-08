# 🎉 HungamaHub - AI-Powered Game Provider 🇮🇳

**From tradition to trend – we bring the hungama!**  
HungamaHub is an intelligent event management platform designed to plan, personalize, and power up events through culturally rich and dynamic game experiences. Built with Python & Flask, it's your one-stop destination for hosting unforgettable events with the help of AI.

---

## 🚀 Features

- 🎯 **Smart Game Recommendations** — Tailored by age group, group type, and occasion  
- 📊 **Game Clustering & Visualization** — Understand similarities between games  
- 🧠 **AI-Powered Chatbot** — Interactive assistant to help users find the perfect game  
- 📋 **Game Planning Toolkit** — Duration, difficulty, props, venue type, and more  
- 🧩 **User Profile System** — Save event history, preferences & past games  
- 🌐 **Multi-lingual Support** — Designed for diverse Indian audiences  
- 📦 **Flask Backend** — Modular, lightweight, and ready for scale

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript (Bootstrap for UI)  
- **Backend**: Python, Flask  
- **Database**: SQLite (can be upgraded to MongoDB/PostgreSQL)  
- **Visualization**: Matplotlib / Seaborn / Plotly  
- **Libraries**: Pandas, NumPy, Scikit-learn  
- **Hosting**: Local / Render / AWS (coming soon)

---

## 📁 Project Structure
hungamahub/ │ ├── app.py # Main Flask application ├── config.py # Configuration settings ├── requirements.txt # Python dependencies ├── .gitignore # Files/folders to be ignored by Git ├── README.md # Project documentation │ ├── static/ # Static assets (CSS, JS, images) │ ├── css/ │ ├── js/ │ └── images/ │ ├── templates/ # HTML templates using Jinja2 │ ├── base.html │ ├── index.html │ ├── dashboard.html │ ├── chatbot.html │ └── auth/ # Login/Signup pages │ ├── login.html │ └── signup.html │ ├── data/ # Game datasets and CSV files │ └── games_dataset.csv │ ├── models/ # Machine Learning models and scripts │ ├── clustering_model.pkl │ └── recommender.py │ ├── chatbot/ # Chatbot engine and filters │ ├── chatbot_engine.py │ ├── filters.py │ └── intent_handler.py │ ├── users/ # User authentication & profiles │ ├── auth.py │ ├── models.py │ └── routes.py │ ├── gameplanner/ # Core event planning and logic │ ├── planner.py │ ├── utils.py │ └── scheduler.py │ ├── visualizer/ # Game clustering and analytics visuals │ ├── visualizer.py │ └── charts.py │ └── api/ # REST API endpoints for mobile/web ├── endpoints.py └── utils.py

## 🔧 Setup & Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/your-username/hungamahub.git
cd hungamahub

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Flask app
python app.py

# 5. Open your browser and go to
http://127.0.0.1:5000/
```

## 🔮 Future Enhancements

- 🧠 **Advanced AI Game Recommender**  
  Personalized suggestions based on group type, age, occasion, and preferences.

- 💬 **Multilingual AI Chatbot**  
  Support for Hindi, Telugu, Tamil, and more — truly Indian and inclusive.

- 🛍️ **Smart Prop Wizard**  
  Auto-generate shopping lists with cost estimation and rental options.

- 📅 **Event Game Scheduler**  
  Drag-and-drop interface to organize games by time slots and breaks.

- 🎤 **Vendor & Host Booking System**  
  Hire game anchors, emcees, artists, and prop vendors from within the app.

- 🎨 **Game Customization with GenAI**  
  Modify existing games or create new ones with the help of generative AI.

- 📱 **Mobile App (Flutter/React Native)**  
  Bring HungamaHub to Android and iOS for event planning on the go.

- ☁️ **Cloud Deployment & Scalability**  
  Host on AWS/GCP with MongoDB or Firebase backend for performance.

- 🧪 **Game Testing Playground**  
  Simulate game flow to test engagement, timing, and difficulty before the event.

- 🏆 **Hungama Creators Program**  
  Community-based game contributors get leaderboard rankings and rewards.

- 📊 **Analytics Dashboard**  
  Event success metrics, engagement heatmaps, and feedback collection.

