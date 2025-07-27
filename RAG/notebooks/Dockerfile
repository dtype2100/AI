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

# ----- Jupyter, JupyterLab, ipykernel 등 필수 파이썬 패키지 설치 -----
RUN pip install --no-cache-dir \
    jupyter \
    notebook \
    jupyterlab \
    ipykernel

# ----- 프로젝트 requirements 파일 복사 및 설치 -----
COPY requirements-base.txt /tmp/
COPY requirements-ml.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements-base.txt
RUN pip install --no-cache-dir -r /tmp/requirements-ml.txt

# ----- ipykernel을 통해 커널 등록 (가상환경) -----
RUN python -m ipykernel install --user --name=python3 --display-name "Python (venv)"

# ----- 작업 디렉터리 설정 -----
WORKDIR /workspace

# ----- JupyterLab 실행 -----
CMD ["jupyter", "lab", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--allow-root", \
     "--NotebookApp.token=devtoken", \
     "--notebook-dir=/home/jovyan/work"] 