# 1주차 과제

> 챕터: Reversing  
> 사일로: 개발


과제 내용: 패스워드/라이선스 체크 프로그램 개발(c) 후 리버싱
- crackme 프로그램이라고 보면 됨
- 라이선스 검증 방법은 자유롭게 하나 이상 선택
- 리버싱을 통해 검증 알고리즘 파악 후 유효한 키 찾기 (리버싱을 통해 찾아보면서 스스로 다시 유추)
- 선택사항: 유효한 키를 맞추는 파이썬 프로그램 개발


## 1. 라이선스 체크 프로그램 개발 (C)

- Crackme로 보면 된다고 해서 드림핵 등에서 볼 수 있는 리버싱 문제 스타일로 생각하고 작성. 
- 라이선스를 체크한 뒤, 기준을 충족하는 키를 입력했다면 flag를 얻을 수 있다. 


### ✅ 라이선스 검증 방법
- checksum을 검증하는 방식으로 하되, 일반적인 라이선스 키처럼 16글자의 영문 대문자와 숫자만 사용하는 것으로 한정함. 
- 해당 길이만 정확하게 입력받도록 작성함. 
- 라이선스 키의 길이와 사용할 수 있는 문자를 고려하여, 다양한 키를 구할 수 있도록 1101이라는 값으로 checksum 값을 설정하였음. 
- scanf의 버퍼오버플로우 문제를 피하기 위해 `%16s`로 읽어오고, 이후 실제 길이를 확인함. 입력 조건을 만족하는지 확인한 후 실제 checksum 값을 확인하고, 맞다면 flag를 출력하도록 설정. 


### 🔒 목표 체크섬 값 은닉
- 단순히 checksum 상수를 정의하면 리버싱을 통해 직접적으로 알 수 있었기 때문에, `get_target_checksum` 함수를 통해 리버싱으로 바로 얻을 수 없도록 은닉함. 
- checksum의 앞부분과 뒷부분을 분리하여 shift 연산을 통해 값을 알아내도록 함. 
- 이때, 메모리에서 항상 변수를 읽어오도록 volatile로 강제하여 Constant Folding과 같은 최적화를 억제하고, `return (high << 8) | low;` 코드를 실행 파일에 남김. 


### 🔒 FLAG 은닉 
- `main.c`와 `flag.c`를 분리하여, 정보 은닉을 강화하고, 외부 파일로 분리되었기 때문에 함수 주소를 비교적 발견하기 까다롭도록 함. 인라인 최적화를 방지함. 
- `flag.c`에서는 순환 xor 연산을 통해 flag를 다시 연산하여 출력하므로, 디컴파일 결과에서 바로 플래그를 획득할 수 없음. 

## 2. 리버싱 후 key를 얻는 파이썬 프로그램 개발 

1) IDA로 디컴파일한 결과, `if ( checksum == get_target_checksum() )`에서 `get_target_checksum()`이 `return (GLOBAL_HIGH_PART << 8) | GLOBAL_LOW_PART;`로 작동하는 부분임을 확인. 


```
.rdata:0000000140004000 ; const volatile int GLOBAL_HIGH_PART
.rdata:0000000140004000 GLOBAL_HIGH_PART dd 4                   ; DATA XREF: get_target_checksum+8↑r
.rdata:0000000140004004                 public GLOBAL_LOW_PART
.rdata:0000000140004004 ; const volatile int GLOBAL_LOW_PART
.rdata:0000000140004004 GLOBAL_LOW_PART dd 4Dh                  ; DATA XREF: get_target_checksum+11↑r
```
  
위처럼 메모리 값이 저장된 것을 발견하여, high part가 10진수 4, low part가 16진수 0x4D임을 확인함.

이에 따라 genKey에서 checksum 값을 구하는 부분을 작성함.

2) crackme.exe를 실행해 아무 값이나 입력해 본 결과, 라이선스 키가 길이 16에 대문자와 숫자만 사용됨을 오류 메시지를 통해 확인함. 

3) `gen_valid_key` 함수를 생성하여, 0를 기준으로 전체 문자열을 채운 후 키를 생성하는 코드를 작성함. 
- 알파벳으로 변환하고 앞에서부터 남은 체크섬을 채우면서 넘어감 

구한 키: ZZLAAAAAAAAAAAAA
실제로 flag를 얻을 수 있었으며, 결과는 success.png 이미지로 확인 가능 