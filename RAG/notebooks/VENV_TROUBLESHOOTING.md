# 가상환경 문제 해결 가이드

Jupyter 노트북에서 "Python (venv)" 가상환경이 보이지 않는 문제를 해결하는 방법을 설명합니다.

## 🔍 문제 진단

### 현재 상황 확인
```bash
# Jupyter 컨테이너에 접속
docker exec -it jupyter bash

# 가상환경 상태 확인
python check_venv.py

# Jupyter 커널 목록 확인
jupyter kernelspec list
```

## 🚨 일반적인 문제들

### 1. "Python 3 (ipykernel)"만 보이는 경우

**원인**: 시스템 Python에 ipykernel이 설치되어 있음

**해결 방법**:
```bash
# 시스템 Python 커널 제거
jupyter kernelspec remove python3 -f

# 가상환경 커널만 남기기
jupyter kernelspec list
```

### 2. 가상환경이 활성화되지 않은 경우

**원인**: Dockerfile에서 가상환경 경로를 제대로 지정하지 않음

**해결 방법**:
```bash
# 컨테이너 재빌드
docker-compose build jupyter

# 컨테이너 재시작
docker-compose restart jupyter
```

### 3. 가상환경 커널이 등록되지 않은 경우

**원인**: ipykernel이 가상환경에 설치되지 않음

**해결 방법**:
```bash
# 가상환경의 Python으로 ipykernel 설치
/opt/venv/bin/pip install ipykernel

# 가상환경 커널 등록
/opt/venv/bin/python -m ipykernel install --user --name=venv --display-name "Python (venv)"
```

## 🛠️ 수정된 Dockerfile

### 주요 변경사항:

1. **가상환경 pip 사용**:
```dockerfile
# 이전 (시스템 pip 사용)
RUN pip install jupyter

# 수정 후 (가상환경 pip 사용)
RUN /opt/venv/bin/pip install jupyter
```

2. **가상환경 Python으로 커널 등록**:
```dockerfile
# 이전 (시스템 Python 사용)
RUN python -m ipykernel install --user --name=python3 --display-name "Python (venv)"

# 수정 후 (가상환경 Python 사용)
RUN /opt/venv/bin/python -m ipykernel install --user --name=venv --display-name "Python (venv)"
```

3. **Jupyter 실행도 가상환경 사용**:
```dockerfile
# 이전 (시스템 jupyter 사용)
CMD ["jupyter", "lab", ...]

# 수정 후 (가상환경 jupyter 사용)
CMD ["/opt/venv/bin/jupyter", "lab", ...]
```

## 🔄 적용 방법

### 1. 컨테이너 재빌드
```bash
cd AI/RAG
docker-compose build jupyter
```

### 2. 컨테이너 재시작
```bash
docker-compose restart jupyter
```

### 3. 상태 확인
```bash
# 컨테이너에 접속
docker exec -it jupyter bash

# 가상환경 확인
python check_venv.py

# 커널 목록 확인
jupyter kernelspec list
```

## ✅ 정상 상태 확인

### 올바른 상태:
```
📍 Python 실행 경로: /opt/venv/bin/python
✅ 가상환경이 활성화되어 있습니다!
   가상환경 경로: /opt/venv

📋 사용 가능한 커널:
Available kernels:
  venv    /home/jovyan/.local/share/jupyter/kernels/venv
```

### Jupyter에서 확인:
- 커널 선택 시 "Python (venv)" 옵션 표시
- 노트북 실행 시 가상환경 경로 사용

## 🐛 추가 문제 해결

### 1. 권한 문제
```bash
# 가상환경 디렉토리 권한 확인
ls -la /opt/venv/

# 권한 수정 (필요한 경우)
chmod -R 755 /opt/venv/
```

### 2. 패키지 설치 문제
```bash
# 가상환경 pip 업그레이드
/opt/venv/bin/pip install --upgrade pip

# 패키지 재설치
/opt/venv/bin/pip install -r requirements-base.txt
/opt/venv/bin/pip install -r requirements-ml.txt
```

### 3. 커널 등록 문제
```bash
# 기존 커널 제거
jupyter kernelspec remove venv -f

# 새로 등록
/opt/venv/bin/python -m ipykernel install --user --name=venv --display-name "Python (venv)"
```

## 📋 체크리스트

- [ ] Dockerfile에서 가상환경 pip 사용
- [ ] 가상환경 Python으로 커널 등록
- [ ] Jupyter 실행도 가상환경 사용
- [ ] 컨테이너 재빌드 완료
- [ ] 컨테이너 재시작 완료
- [ ] 가상환경 상태 확인
- [ ] Jupyter에서 "Python (venv)" 커널 선택 가능

## 💡 모범 사례

### 1. 명시적 경로 사용
```dockerfile
# 절대 경로로 가상환경 사용
RUN /opt/venv/bin/pip install package
RUN /opt/venv/bin/python -m ipykernel install ...
```

### 2. 환경변수 설정
```dockerfile
# 가상환경 PATH 설정
ENV PATH="/opt/venv/bin:${PATH}"
```

### 3. 커널 이름 구분
```dockerfile
# 시스템과 구분되는 커널 이름 사용
--name=venv --display-name "Python (venv)"
```

이렇게 설정하면 Jupyter에서 올바른 가상환경을 사용할 수 있습니다! 