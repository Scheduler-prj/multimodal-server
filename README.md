# PlanQ Multimodal RAG Server Guide

이 프로젝트는 Flask를 사용하여 개발되었습니다.  
아래 가이드를 따라 환경을 설정하고 애플리케이션을 실행해 주세요.

## 1. 가상환경 설정

1. **가상환경 생성**  
   프로젝트 루트 디렉토리에서 아래 명령어를 실행하여 가상환경을 생성합니다:
   ```bash
   python -m venv .venv
   ```

2. **가상환경 활성화**
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```


## 2. 의존성 설치

1. 가상환경을 활성화한 상태에서 아래 명령어를 실행하여 의존성을 설치합니다:
   ```bash
   pip install -r requirements.txt
   ```

2. 개발 중 새로운 라이브러리를 설치한 경우, 아래 명령어로 `requirements.txt`를 업데이트하세요:
   ```bash
   pip freeze > requirements.txt
   ```



## 3. Flask 서버 실행

1. 가상환경을 활성화한 상태에서 Flask 서버를 실행합니다:
   ```bash
   python app.py
   ```

2. 브라우저에서 `http://127.0.0.1:5000/`로 접속하여 애플리케이션을 확인합니다.



## 4. 환경 변수 설정(필수)

이 프로젝트는 API 키와 같은 민감한 정보를 `.env` 파일에서 관리합니다.

1. 프로젝트 루트 디렉토리에 `.env` 파일을 생성합니다.
2. `.env` 파일에 아래와 같은 내용을 추가합니다:
   ```
   GEMINI_API_KEY=<Gemini API 키>
   UPSTAGE_API_KEY=<Upstage API 키>
   ```
3. `.env` 파일은 Git에 포함되지 않으므로 **민감한 정보를 외부에 노출하지 않도록 주의하세요**.