# AI 비서 웹 애플리케이션

이 프로젝트는 Flask를 사용하여 구현된 AI 비서 웹 애플리케이션입니다. 사용자가 AI와 대화하고, 메모를 작성하고, 할 일 목록을 관리하고, 날씨 정보를 확인할 수 있는 기능을 제공합니다.

## 주요 기능

- **AI 비서와 대화**: OpenAI API를 사용하여 사용자의 질문에 답변하고 대화할 수 있습니다.
- **메모 관리**: 메모를 작성, 저장, 삭제할 수 있습니다.
- **할 일 목록**: 할 일을 추가하고, 완료 여부를 표시하고, 삭제할 수 있습니다.
- **날씨 정보**: 도시 이름을 입력하여 현재 날씨 정보를 확인할 수 있습니다.
- **대화 기록**: AI 비서와의 대화 내용을 저장하고 나중에 확인할 수 있습니다.

## 설치 방법

1. 저장소를 클론합니다:
   ```
   git clone https://github.com/yourusername/ai-assistant.git
   cd ai-assistant
   ```

2. 가상 환경을 생성하고 활성화합니다:
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. 필요한 패키지를 설치합니다:
   ```
   pip install -r requirements.txt
   ```

4. 환경 변수 설정을 위한 `.env` 파일을 생성합니다:
   ```
   OPENAI_API_KEY=your_openai_api_key
   WEATHER_API_KEY=your_openweathermap_api_key
   ```

## 실행 방법

1. 다음 명령어로 애플리케이션을 실행합니다:
   ```
   python app.py
   ```

2. 웹 브라우저에서 `http://127.0.0.1:5000/`으로 접속합니다.

## 기술 스택

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite
- **API**: OpenAI API, OpenWeatherMap API

## 프로젝트 구조

```
ai-assistant/
├── app.py                  # 메인 애플리케이션 파일
├── requirements.txt        # 필요한 패키지 목록
├── .env                    # 환경 변수 파일 (생성 필요)
├── static/                 # 정적 파일
│   ├── css/                # CSS 파일
│   │   └── style.css       # 메인 스타일시트
│   └── js/                 # JavaScript 파일
│       └── main.js         # 메인 JavaScript 파일
└── templates/              # HTML 템플릿
    ├── base.html           # 기본 레이아웃
    ├── index.html          # 메인 페이지
    ├── notes.html          # 메모 페이지
    ├── tasks.html          # 할 일 목록 페이지
    ├── weather.html        # 날씨 정보 페이지
    └── history.html        # 대화 기록 페이지
```

## API 키 설정

이 애플리케이션을 사용하려면 다음 API 키가 필요합니다:

1. **OpenAI API 키**: [OpenAI](https://platform.openai.com/)에서 API 키를 발급받을 수 있습니다.
2. **OpenWeatherMap API 키**: [OpenWeatherMap](https://openweathermap.org/api)에서 API 키를 발급받을 수 있습니다.

발급받은 API 키는 `.env` 파일에 설정해야 합니다.

## 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다. 