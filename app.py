from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json
import random
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 타임스탬프를 날짜로 변환하는 필터 함수
def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assistant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Jinja2 필터 등록
app.jinja_env.filters['timestamp_to_datetime'] = timestamp_to_datetime

# 데이터베이스 모델
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Note('{self.title}', '{self.date_created}')"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task('{self.content}', '{self.completed}')"

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Conversation('{self.date_created}')"

# 애플리케이션 컨텍스트에서 데이터베이스 생성
with app.app_context():
    db.create_all()

# 간단한 AI 응답 생성 함수
def generate_ai_response(user_message):
    # 간단한 키워드 기반 응답
    greetings = ["안녕", "hi", "hello", "ㅎㅇ", "하이"]
    weather = ["날씨", "비", "맑음", "흐림", "눈", "기온"]
    time = ["시간", "몇시", "date", "날짜"]
    
    user_message_lower = user_message.lower()
    
    if any(greeting in user_message_lower for greeting in greetings):
        responses = [
            "안녕하세요! 무엇을 도와드릴까요?",
            "반갑습니다! 오늘 기분은 어떠신가요?",
            "안녕하세요! 저는 AI 비서입니다. 무엇을 도와드릴까요?"
        ]
        return random.choice(responses)
    
    elif any(w in user_message_lower for w in weather):
        responses = [
            "오늘 날씨는 맑을 예정입니다. 상단 메뉴의 '날씨'를 클릭하여 자세한 정보를 확인하세요.",
            "날씨 정보를 확인하시려면 상단 메뉴의 '날씨'를 클릭하세요.",
            "오늘은 화창한 날씨가 예상됩니다. 더 자세한 정보를 원하시면 날씨 메뉴를 이용해주세요."
        ]
        return random.choice(responses)
    
    elif any(t in user_message_lower for t in time):
        now = datetime.now()
        return f"현재 시간은 {now.strftime('%Y년 %m월 %d일 %H시 %M분')}입니다."
    
    else:
        responses = [
            "죄송합니다. 질문을 이해하지 못했습니다. 다른 방식으로 질문해 주시겠어요?",
            "흥미로운 질문이네요! 조금 더 자세히 설명해 주시겠어요?",
            "도움이 필요하신가요? 메모 작성이나 할 일 관리, 날씨 확인 등을 도와드릴 수 있습니다.",
            f"'{user_message}'에 대해 더 알려주세요. 어떤 도움이 필요하신가요?"
        ]
        return random.choice(responses)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "메시지가 비어있습니다."}), 400
    
    try:
        # AI 응답 생성
        ai_response = generate_ai_response(user_message)
        
        # 대화 저장
        new_conversation = Conversation(user_message=user_message, ai_response=ai_response)
        db.session.add(new_conversation)
        db.session.commit()
        
        return jsonify({"response": ai_response})
    
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/notes')
def notes():
    all_notes = Note.query.order_by(Note.date_created.desc()).all()
    return render_template('notes.html', notes=all_notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    
    new_note = Note(title=title, content=content)
    db.session.add(new_note)
    db.session.commit()
    
    return redirect(url_for('notes'))

@app.route('/delete_note/<int:id>')
def delete_note(id):
    note_to_delete = Note.query.get_or_404(id)
    db.session.delete(note_to_delete)
    db.session.commit()
    
    return redirect(url_for('notes'))

@app.route('/tasks')
def tasks():
    all_tasks = Task.query.order_by(Task.date_created.desc()).all()
    return render_template('tasks.html', tasks=all_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    content = request.form['content']
    
    new_task = Task(content=content)
    db.session.add(new_task)
    db.session.commit()
    
    return redirect(url_for('tasks'))

@app.route('/toggle_task/<int:id>')
def toggle_task(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    
    return redirect(url_for('tasks'))

@app.route('/delete_task/<int:id>')
def delete_task(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    
    return redirect(url_for('tasks'))

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_data = None
    
    if request.method == 'POST':
        city = request.form['city']
        api_key = os.getenv("WEATHER_API_KEY", "338bd5e23afd49b2c68187b80ed218e9")
        
        try:
            import requests
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            weather_data = response.json()
        except Exception as e:
            weather_data = {"error": str(e)}
    
    return render_template('weather.html', weather_data=weather_data)

@app.route('/history')
def history():
    all_conversations = Conversation.query.order_by(Conversation.date_created.desc()).all()
    return render_template('history.html', conversations=all_conversations)

if __name__ == '__main__':
    app.run(debug=True) 