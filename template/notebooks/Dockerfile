<<<<<<< HEAD:notebooks/Dockerfile
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
=======
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

# ----- 가상환경 활성화 및 패키지 설치 -----
RUN /opt/venv/bin/pip install --no-cache-dir \
    jupyter \
    notebook \
    jupyterlab \
    ipykernel

# ----- 프로젝트 requirements 파일 복사 및 설치 -----
COPY requirements-base.txt /tmp/
COPY requirements-ml.txt /tmp/
RUN /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements-base.txt
RUN /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements-ml.txt

# ----- ipykernel을 통해 커널 등록 (가상환경) -----
RUN /opt/venv/bin/python -m ipykernel install --user --name=venv --display-name "Python (venv)"

# ----- 시스템 Python 커널 제거 (선택사항) -----
RUN jupyter kernelspec remove python3 -f || true

# ----- 작업 디렉터리 설정 -----
WORKDIR /workspace

# ----- JupyterLab 실행 (가상환경 사용) -----
CMD ["/opt/venv/bin/jupyter", "lab", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--allow-root", \
     "--NotebookApp.token=devtoken", \
>>>>>>> 1de3b1b80d282141b95bf741b9c6ca102e8ea80e:template/notebooks/Dockerfile
     "--notebook-dir=/home/jovyan/work"] 