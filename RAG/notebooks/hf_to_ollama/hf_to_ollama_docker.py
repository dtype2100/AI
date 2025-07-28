import os
import subprocess
import requests
import json

def register_hf_model_to_ollama(model_path, model_name, ollama_host="http://ollama:11434"):
    """
    Hugging Face 모델을 ollama에 등록하는 함수입니다.
    Docker 환경에서 HTTP API를 통해 ollama와 통신합니다.
    
    :param model_path: 변환된 모델 파일 경로 (예: 'model.gguf')
    :param model_name: ollama에 등록할 모델 이름 (예: 'my-model')
    :param ollama_host: ollama 서버 주소 (Docker 내부에서는 'http://ollama:11434')
    """
    
    # Modelfile 생성
    modelfile_content = f"""FROM {model_path}
TEMPLATE "{{{{ .System }}}}{{{{ .Prompt }}}}{{{{ .Response }}}}"
"""
    
    modelfile_path = f"{model_name}.Modelfile"
    with open(modelfile_path, 'w') as f:
        f.write(modelfile_content)
    
    # ollama create 명령어 실행 (Docker 컨테이너 내부에서)
    command = [
        "ollama", "create", model_name, 
        "--file", modelfile_path
    ]
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"모델이 성공적으로 등록되었습니다: {model_name}")
        print(result.stdout)
        
        # 등록된 모델 확인
        check_model_status(model_name, ollama_host)
        
    except subprocess.CalledProcessError as e:
        print("모델 등록 중 오류가 발생했습니다.")
        print(f"Error: {e.stderr}")
        print(f"Command: {' '.join(command)}")
    except FileNotFoundError:
        print("Ollama가 설치되지 않았거나 PATH에 없습니다.")
        print("Docker 컨테이너 내부에서 실행 중인지 확인하세요.")

def check_model_status(model_name, ollama_host="http://ollama:11434"):
    """
    등록된 모델의 상태를 확인합니다.
    """
    try:
        response = requests.get(f"{ollama_host}/api/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            for model in models:
                if model['name'] == model_name:
                    print(f"모델 '{model_name}'이 성공적으로 등록되었습니다.")
                    print(f"모델 크기: {model.get('size', 'N/A')}")
                    return True
            print(f"모델 '{model_name}'을 찾을 수 없습니다.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Ollama API 연결 오류: {e}")
        return False

def list_available_models(ollama_host="http://ollama:11434"):
    """
    사용 가능한 모델 목록을 확인합니다.
    """
    try:
        response = requests.get(f"{ollama_host}/api/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("사용 가능한 모델:")
            for model in models:
                print(f"- {model['name']} (크기: {model.get('size', 'N/A')})")
            return models
        else:
            print(f"API 오류: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Ollama API 연결 오류: {e}")
        return []

def test_ollama_connection(ollama_host="http://ollama:11434"):
    """
    Ollama 서버 연결을 테스트합니다.
    """
    try:
        response = requests.get(f"{ollama_host}/api/tags")
        if response.status_code == 200:
            print("✅ Ollama 서버에 성공적으로 연결되었습니다.")
            return True
        else:
            print(f"❌ Ollama 서버 연결 실패: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama 서버 연결 오류: {e}")
        return False

if __name__ == "__main__":
    # 연결 테스트
    print("Ollama 서버 연결 테스트:")
    test_ollama_connection()
    
    print("\n현재 등록된 모델:")
    list_available_models()
    
    # 사용 예시 (주석 처리)
    # register_hf_model_to_ollama("./models/llama-3.2-Korean-Bllossom-3B-gguf-Q4_K_M.gguf", "llama-3.2-Korean-Bllossom-3B-gguf-Q4_K_M.gguf") 