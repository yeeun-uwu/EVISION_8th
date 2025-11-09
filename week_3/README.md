# 3주차 과제

> 챕터: Reversing  
> 사일로: 개발

과제 내용: 패킹된 실행파일 분석

1) 간단한 패커 구현 
2) 언패킹 프로그램 개발
3) 안티 리버싱 추가 (선택사항)


> 제출 내용: 패커 소스 코드, 언패커 소스 코드, READ.md (패킹 알고리즘 설명, 언패킹 과정 설명, 실행 결과)

## 1. 패커 구현

먼저 Hello, World! 메시지를 출력하는 간단한 실행파일을 만들었다.   
이후 패킹 기법은 

- xor 인코딩  
- Base64 인코딩  
- 간단한 압축(zlib 등)  
- 더미 코드 삽입  

중에서 2가지 이상을 적용해서 구현하는 게 요구사항이었다. 

이를 수행하기 위해 `packer.py`를 만들고, 구현을 시작했다. 

### 👀 선택한 방식

앞뒤로 40바이트의 더미 코드(NOP)를 삽입한 후 `zlib`을 이용해 코드를 압축하고, `base64` 인코딩하는 방식으로 패커를 구현했다. 
또한 일단은 `.text` 섹션만 패킹하도록 했다. 

실행했던 로그: 
```
[Running] python -u "EVISION_8th\week_3\packer.py"
[*] Packer started.
[+] Loaded PE file: EVISION_8th\week_3/hello.exe
[+] .text section found. Size: 6144 bytes
[+] Dummy code inserted. New size: 6224 bytes
[+] Code compressed. Compressed size: 3615 bytes
[+] Code encoded to Base64. Encoded size: 4820 bytes
[+] Packed data saved to: EVISION_8th\week_3/packed.dat

[Done] exited with code=0 in 0.107 seconds
```

(경로 앞부분만 삭제했다) 

## 2. 언패커 구현

일단은 패킹했던 `.text` 섹션을 언패킹하는 코드를 `unpacker.py`로 작성하고, 이를 사용해서 `restored_code.bin`을 생성했다.

실행 로그: 
```
[Running] python -u "EVISION_8th\week_3\unpacker.py"
[*] Unpacker started.
[+] Packed data loaded from: EVISION_8th\week_3/packed.dat
[+] Code decoded from Base64. Decoded size: 3615 bytes
[+] Code decompressed. Decompressed size: 6224 bytes
[+] Dummy code removed. Restored size: 6144 bytes
[+] Restored code saved to: EVISION_8th\week_3/restored_code.bin

[Done] exited with code=0 in 0.074 seconds
```

`Restored size`가 기존에 로드했던 `.text` 섹션과 일치함을 알 수 있다. 

