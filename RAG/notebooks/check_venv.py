#!/usr/bin/env python3
"""
가상환경 상태 확인 스크립트
"""

import sys
import os
import subprocess
from pathlib import Path

def check_venv_status():
    """가상환경 상태 확인"""
    print("🔍 가상환경 상태 확인")
    print("=" * 50)
    
    # 1. Python 실행 경로 확인
    print(f"📍 Python 실행 경로: {sys.executable}")
    
    # 2. 가상환경 여부 확인
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ 가상환경이 활성화되어 있습니다!")
        if hasattr(sys, 'real_prefix'):
            print(f"   시스템 Python: {sys.real_prefix}")
        print(f"   가상환경 경로: {sys.prefix}")
    else:
        print("❌ 가상환경이 활성화되어 있지 않습니다.")
        print(f"   현재 Python 경로: {sys.prefix}")
    
    # 3. PATH 환경변수 확인
    print(f"\n🔗 PATH 환경변수:")
    for i, path in enumerate(os.environ.get('PATH', '').split(':')):
        if '/opt/venv' in path:
            print(f"   {i+1}. {path} ✅ (가상환경)")
        else:
            print(f"   {i+1}. {path}")
    
    # 4. pip 위치 확인
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True)
        print(f"\n📦 pip 정보:")
        print(f"   {result.stdout.strip()}")
    except Exception as e:
        print(f"   ❌ pip 확인 실패: {e}")
    
    # 5. 설치된 패키지 확인
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True)
        packages = result.stdout.strip().split('\n')
        print(f"\n📋 설치된 패키지 수: {len(packages) - 2}")  # 헤더 제외
    except Exception as e:
        print(f"   ❌ 패키지 목록 확인 실패: {e}")

def check_jupyter_kernels():
    """Jupyter 커널 확인"""
    print("\n🎯 Jupyter 커널 확인")
    print("=" * 50)
    
    try:
        result = subprocess.run(['jupyter', 'kernelspec', 'list'], 
                              capture_output=True, text=True)
        print("📋 사용 가능한 커널:")
        print(result.stdout)
    except Exception as e:
        print(f"❌ 커널 목록 확인 실패: {e}")

def check_venv_directory():
    """가상환경 디렉토리 확인"""
    print("\n📁 가상환경 디렉토리 확인")
    print("=" * 50)
    
    venv_path = Path("/opt/venv")
    if venv_path.exists():
        print(f"✅ 가상환경 디렉토리 존재: {venv_path}")
        
        # 주요 파일들 확인
        files_to_check = [
            "bin/python",
            "bin/pip", 
            "bin/jupyter",
            "lib/python3.*/site-packages"
        ]
        
        for pattern in files_to_check:
            matches = list(venv_path.glob(pattern))
            if matches:
                print(f"   ✅ {pattern}: {matches[0]}")
            else:
                print(f"   ❌ {pattern}: 없음")
    else:
        print(f"❌ 가상환경 디렉토리 없음: {venv_path}")

if __name__ == "__main__":
    check_venv_status()
    check_jupyter_kernels()
    check_venv_directory()
    
    print("\n" + "=" * 50)
    print("💡 가상환경이 제대로 설정되지 않은 경우:")
    print("   1. Docker 컨테이너 재빌드: docker-compose build jupyter")
    print("   2. 컨테이너 재시작: docker-compose restart jupyter")
    print("   3. Jupyter에서 'Python (venv)' 커널 선택") 