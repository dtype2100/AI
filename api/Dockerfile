FROM ubuntu:22.04

# ----- 환경변수 설정 -----
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/venv/bin:${PATH}"

# ----- 필수 패키지 설치 -----
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        wget \
        git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ----- 가상환경 생성 및 활성화 -----
RUN python3 -m venv /opt/venv

# ----- 작업 디렉터리 설정 -----
WORKDIR /app

# ----- 프로젝트 requirements.txt 설치 -----
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# ----- 애플리케이션 파일 복사 -----
COPY . .

# ----- FastAPI 실행 -----
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 