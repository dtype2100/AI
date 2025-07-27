#!/usr/bin/env python3
"""
Hugging Face 모델을 Ollama로 변환하고 LangChain으로 추론 테스트
"""

import os
import json
import requests
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import time

# LangChain 관련 import
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOllama

class HFToOllamaConverter:
    def __init__(self, ollama_host: str = "http://localhost:11434"):
        self.ollama_host = ollama_host
        self.models_dir = Path("./ollama/models")
        self.models_dir.mkdir(exist_ok=True)
        
    def check_ollama_status(self) -> bool:
        """Ollama 서버 상태 확인"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_installed_models(self) -> list:
        """설치된 모델 목록 조회"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except Exception as e:
            print(f"모델 목록 조회 실패: {e}")
            return []
    
    def pull_model_from_hf(self, model_name: str, hf_model_id: str) -> bool:
        """
        Hugging Face 모델을 Ollama로 가져오기
        
        Args:
            model_name: Ollama에서 사용할 모델 이름
            hf_model_id: Hugging Face 모델 ID (예: "microsoft/DialoGPT-medium")
        """
        try:
            print(f"🤖 {hf_model_id} 모델을 Ollama로 가져오는 중...")
            
            # Ollama pull 명령어 실행
            cmd = [
                "ollama", "pull", 
                f"{model_name}:latest",
                "--insecure-registry"
            ]
            
            # 환경변수 설정 (Hugging Face 토큰이 있는 경우)
            env = os.environ.copy()
            if "HUGGING_FACE_HUB_TOKEN" in env:
                env["HF_TOKEN"] = env["HUGGING_FACE_HUB_TOKEN"]
            
            # 명령어 실행
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                env=env,
                timeout=3600  # 1시간 타임아웃
            )
            
            if result.returncode == 0:
                print(f"✅ {model_name} 모델 다운로드 완료!")
                return True
            else:
                print(f"❌ 모델 다운로드 실패: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ 모델 다운로드 시간 초과")
            return False
        except Exception as e:
            print(f"❌ 모델 다운로드 중 오류: {e}")
            return False
    
    def create_custom_modelfile(self, model_name: str, hf_model_id: str, template: str = None) -> str:
        """
        커스텀 Modelfile 생성
        
        Args:
            model_name: 모델 이름
            hf_model_id: Hugging Face 모델 ID
            template: 프롬프트 템플릿
        """
        modelfile_content = f"""FROM {hf_model_id}

# 기본 시스템 프롬프트 설정
SYSTEM \"\"\"당신은 도움이 되는 AI 어시스턴트입니다. 
한국어로 친절하고 정확한 답변을 제공해주세요.\"\"\"

# 프롬프트 템플릿 설정
TEMPLATE \"\"\"{template or "{{ .System }}\n\n사용자: {{ .Prompt }}\n\n어시스턴트: "}\"\"\"

# 파라미터 설정
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
"""
        
        modelfile_path = f"./modelfile_{model_name}"
        with open(modelfile_path, 'w', encoding='utf-8') as f:
            f.write(modelfile_content)
        
        return modelfile_path
    
    def create_model_from_modelfile(self, model_name: str, modelfile_path: str) -> bool:
        """Modelfile로부터 모델 생성"""
        try:
            print(f"🔨 {model_name} 모델 생성 중...")
            
            cmd = ["ollama", "create", model_name, "-f", modelfile_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {model_name} 모델 생성 완료!")
                return True
            else:
                print(f"❌ 모델 생성 실패: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 모델 생성 중 오류: {e}")
            return False
    
    def test_model_inference(self, model_name: str, test_prompts: list) -> Dict[str, Any]:
        """모델 추론 테스트"""
        results = {}
        
        try:
            # Ollama LLM 초기화
            llm = Ollama(
                model=model_name,
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
                temperature=0.7
            )
            
            print(f"\n🧪 {model_name} 모델 추론 테스트 시작...\n")
            
            for i, prompt in enumerate(test_prompts, 1):
                print(f"\n--- 테스트 {i} ---")
                print(f"프롬프트: {prompt}")
                print("응답:")
                
                start_time = time.time()
                try:
                    response = llm(prompt)
                    end_time = time.time()
                    
                    results[f"test_{i}"] = {
                        "prompt": prompt,
                        "response": response,
                        "time_taken": end_time - start_time,
                        "status": "success"
                    }
                    
                except Exception as e:
                    results[f"test_{i}"] = {
                        "prompt": prompt,
                        "error": str(e),
                        "status": "error"
                    }
                    print(f"❌ 추론 실패: {e}")
                
                print("-" * 50)
            
            return results
            
        except Exception as e:
            print(f"❌ 모델 초기화 실패: {e}")
            return {"error": str(e)}
    
    def test_chat_model(self, model_name: str, test_conversations: list) -> Dict[str, Any]:
        """채팅 모델 테스트"""
        results = {}
        
        try:
            # ChatOllama 초기화
            chat_model = ChatOllama(
                model=model_name,
                temperature=0.7
            )
            
            print(f"\n💬 {model_name} 채팅 모델 테스트 시작...\n")
            
            for i, conversation in enumerate(test_conversations, 1):
                print(f"\n--- 채팅 테스트 {i} ---")
                
                messages = []
                for msg in conversation:
                    if msg["role"] == "system":
                        messages.append(SystemMessage(content=msg["content"]))
                    elif msg["role"] == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                
                print(f"대화: {[msg.content for msg in messages]}")
                print("응답:")
                
                start_time = time.time()
                try:
                    response = chat_model(messages)
                    end_time = time.time()
                    
                    results[f"chat_test_{i}"] = {
                        "conversation": conversation,
                        "response": response.content,
                        "time_taken": end_time - start_time,
                        "status": "success"
                    }
                    
                    print(f"AI: {response.content}")
                    
                except Exception as e:
                    results[f"chat_test_{i}"] = {
                        "conversation": conversation,
                        "error": str(e),
                        "status": "error"
                    }
                    print(f"❌ 채팅 실패: {e}")
                
                print("-" * 50)
            
            return results
            
        except Exception as e:
            print(f"❌ 채팅 모델 초기화 실패: {e}")
            return {"error": str(e)}

def main():
    """메인 실행 함수"""
    print("🚀 Hugging Face → Ollama → LangChain 테스트 시작\n")
    
    # 컨버터 초기화
    converter = HFToOllamaConverter()
    
    # Ollama 서버 상태 확인
    if not converter.check_ollama_status():
        print("❌ Ollama 서버가 실행되지 않았습니다.")
        print("docker-compose up -d ollama 명령어로 서버를 시작해주세요.")
        return
    
    print("✅ Ollama 서버 연결 확인됨")
    
    # 설치된 모델 목록 확인
    installed_models = converter.list_installed_models()
    print(f"📋 설치된 모델: {installed_models}")
    
    # 테스트할 모델 설정
    test_models = [
        {
            "name": "llama2",
            "hf_id": "meta-llama/Llama-2-7b-chat-hf",
            "description": "Llama2 7B 채팅 모델"
        },
        {
            "name": "codellama", 
            "hf_id": "codellama/CodeLlama-7b-Instruct-hf",
            "description": "CodeLlama 7B 인스트럭트 모델"
        }
    ]
    
    # 테스트 프롬프트
    test_prompts = [
        "안녕하세요! 오늘 날씨는 어떤가요?",
        "파이썬으로 Hello World를 출력하는 코드를 작성해주세요.",
        "인공지능의 미래에 대해 어떻게 생각하시나요?",
        "한국의 전통 문화에 대해 설명해주세요."
    ]
    
    # 테스트 대화
    test_conversations = [
        [
            {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다."},
            {"role": "user", "content": "파이썬을 배우고 싶어요. 어떻게 시작하면 좋을까요?"}
        ],
        [
            {"role": "system", "content": "당신은 친절한 코딩 튜터입니다."},
            {"role": "user", "content": "리스트와 튜플의 차이점을 설명해주세요."}
        ]
    ]
    
    all_results = {}
    
    for model_config in test_models:
        model_name = model_config["name"]
        hf_id = model_config["hf_id"]
        
        print(f"\n{'='*60}")
        print(f"🔧 {model_config['description']} 처리 중...")
        print(f"{'='*60}")
        
        # 모델이 이미 설치되어 있는지 확인
        if model_name in installed_models:
            print(f"✅ {model_name} 모델이 이미 설치되어 있습니다.")
        else:
            # 모델 다운로드
            success = converter.pull_model_from_hf(model_name, hf_id)
            if not success:
                print(f"❌ {model_name} 모델 다운로드 실패, 다음 모델로 진행...")
                continue
        
        # 추론 테스트
        print(f"\n🧪 {model_name} 추론 테스트...")
        inference_results = converter.test_model_inference(model_name, test_prompts)
        all_results[f"{model_name}_inference"] = inference_results
        
        # 채팅 테스트
        print(f"\n💬 {model_name} 채팅 테스트...")
        chat_results = converter.test_chat_model(model_name, test_conversations)
        all_results[f"{model_name}_chat"] = chat_results
        
        print(f"\n✅ {model_name} 테스트 완료!")
    
    # 결과 저장
    with open("ollama_test_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 모든 테스트 완료! 결과가 ollama_test_results.json에 저장되었습니다.")
    
    # 요약 출력
    print("\n📊 테스트 결과 요약:")
    for model_name in [m["name"] for m in test_models]:
        if f"{model_name}_inference" in all_results:
            inference_success = sum(1 for r in all_results[f"{model_name}_inference"].values() 
                                  if r.get("status") == "success")
            print(f"  {model_name} 추론: {inference_success}/{len(test_prompts)} 성공")
        
        if f"{model_name}_chat" in all_results:
            chat_success = sum(1 for r in all_results[f"{model_name}_chat"].values() 
                             if r.get("status") == "success")
            print(f"  {model_name} 채팅: {chat_success}/{len(test_conversations)} 성공")

if __name__ == "__main__":
    main() 