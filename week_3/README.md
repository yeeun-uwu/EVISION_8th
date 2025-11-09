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

## 3. 추출해야 하는 정보 추가

요구사항에서는 언패킹 프로그램을 통해 Entry Point, Import Table, 문자열 정보를 추출하도록 되어 있었다.
해당 정보를 먼저 packer.py가 포함하여 패킹하도록 추가했다. 
`EP`, `imports` 등을 json 모듈을 통해 바이트로 변환하고 파일에 쓰도록 했다. 

실행한 패커 로그: 
```
[Running] python -u "EVISION_8th\week_3\packer.py"
[*] Packer started.
[+] Loaded PE file: EVISION_8th\week_3/hello.exe
[+] .text section found. Size: 6144 bytes

[*] Extracting PE information...
[+] Original Entry Point RVA: 0x13e0
[+] Entry Point VA: 0x1400013e0
[+] Found IAT entry: KERNEL32.dll with 10 functions
[+] Found IAT entry: api-ms-win-crt-environment-l1-1-0.dll with 1 functions
[+] Found IAT entry: api-ms-win-crt-heap-l1-1-0.dll with 4 functions
[+] Found IAT entry: api-ms-win-crt-math-l1-1-0.dll with 1 functions
[+] Found IAT entry: api-ms-win-crt-private-l1-1-0.dll with 2 functions
[+] Found IAT entry: api-ms-win-crt-runtime-l1-1-0.dll with 13 functions
[+] Found IAT entry: api-ms-win-crt-stdio-l1-1-0.dll with 6 functions
[+] Found IAT entry: api-ms-win-crt-string-l1-1-0.dll with 2 functions
[+] Found 92 strings in .rdata
[+] Dummy code inserted. New size: 6224 bytes
[+] Code compressed. Compressed size: 3615 bytes
[+] Code encoded to Base64. Encoded size: 4820 bytes

[+] Packed data saved to: EVISION_8th\week_3/packed.dat

[Done] exited with code=0 in 0.108 seconds
```

실행한 언패커 로그:
```
[Running] python -u "EVISION_8th\week_3\unpacker.py"
[*] Unpacker started.
[+] Packed data loaded from: EVISION_8th\week_3/packed.dat
[+] Code decoded from Base64. Decoded size: 3615 bytes
[+] Code decompressed. Decompressed size: 6224 bytes
[+] Dummy code removed. Restored size: 6144 bytes
[+] Restored code saved to: EVISION_8th\week_3/restored_code.bin

--- Extracted PE Information ---

[*] Entry Point (VA):
    0x1400013E0

[*] Import Table:
    DLL: KERNEL32.dll
        - DeleteCriticalSection
        - EnterCriticalSection
        - GetLastError
        - InitializeCriticalSection
        - LeaveCriticalSection
        - SetUnhandledExceptionFilter
        - Sleep
        - TlsGetValue
        - VirtualProtect
        - VirtualQuery
    DLL: api-ms-win-crt-environment-l1-1-0.dll
        - __p__environ
    DLL: api-ms-win-crt-heap-l1-1-0.dll
        - _set_new_mode
        - calloc
        - free
        - malloc
    DLL: api-ms-win-crt-math-l1-1-0.dll
        - __setusermatherr
    DLL: api-ms-win-crt-private-l1-1-0.dll
        - __C_specific_handler
        - memcpy
    DLL: api-ms-win-crt-runtime-l1-1-0.dll
        - __p___argc
        - __p___argv
        - _cexit
        - _configure_narrow_argv
        - _crt_atexit
        - _exit
        - _initialize_narrow_environment
        - _initterm
        - _set_app_type
        - _set_invalid_parameter_handler
        - abort
        - exit
        - signal
    DLL: api-ms-win-crt-stdio-l1-1-0.dll
        - __acrt_iob_func
        - __p__commode
        - __p__fmode
        - __stdio_common_vfprintf
        - fwrite
        - puts
    DLL: api-ms-win-crt-string-l1-1-0.dll
        - strlen
        - strncmp

[*] Extracted Strings:
    - Hello, World!
    - Argument domain error 
    - DOMAIN
    - Argument singularity 
    - Overflow range error 
    - OVERFLOW
    - Partial loss of significance 
    - PLOSS
    - Total loss of significance 
    - TLOSS
    - The result is too small to be represented 
    - UNDERFLOW
    - Unknown error
    - matherr
    - s in 
    - retval
    - Mingw
    - w64 runtime failure
    - Address 
    - p has no image
    - section
    -   VirtualQuery failed for 
    - d bytes at address 
    -   VirtualProtect failed with code 0x
    -   Unknown pseudo relocation protocol version 
    -   Unknown pseudo relocation bit size 
    - d bit pseudo relocation at 
    - p out of range, targeting 
    - p, yielding the value 
    - runtime error 
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0
    - Rev2, Built by MSYS2 project
    -  14.2.0

--- End of PE Information ---

[*] Unpacking completed.

[Done] exited with code=0 in 0.082 seconds
```

중복된 문자열이 너무 많이 나와서 해당 부분을 수정해주기로 했다. 

### 👀 수정

` string_list = list(set([s.decode('utf-8') for s in printable_strings]))` 으로 수정해서 순서는 무너지겠지만 중복을 삭제하는 방향으로 수정했다. 

패커 실행 로그: 
```
[Running] python -u "EVISION_8th\week_3\packer.py"
[*] Packer started.
[+] Loaded PE file: EVISION_8th\week_3/hello.exe
[+] .text section found. Size: 6144 bytes

[*] Extracting PE information...
[+] Original Entry Point RVA: 0x13e0
[+] Entry Point VA: 0x1400013e0
[+] Found IAT entry: KERNEL32.dll with 10 functions
[+] Found IAT entry: api-ms-win-crt-environment-l1-1-0.dll with 1 functions
[+] Found IAT entry: api-ms-win-crt-heap-l1-1-0.dll with 4 functions
[+] Found IAT entry: api-ms-win-crt-math-l1-1-0.dll with 1 functions
[+] Found IAT entry: api-ms-win-crt-private-l1-1-0.dll with 2 functions
[+] Found IAT entry: api-ms-win-crt-runtime-l1-1-0.dll with 13 functions
[+] Found IAT entry: api-ms-win-crt-stdio-l1-1-0.dll with 6 functions
[+] Found IAT entry: api-ms-win-crt-string-l1-1-0.dll with 2 functions
[+] Found 32 strings in .rdata
[+] Dummy code inserted. New size: 6224 bytes
[+] Code compressed. Compressed size: 3615 bytes
[+] Code encoded to Base64. Encoded size: 4820 bytes

[+] Packed data saved to: EVISION_8th\week_3/packed.dat

[Done] exited with code=0 in 0.111 seconds
```

언패커 실행 로그: 
```
[Running] python -u "EVISION_8th\week_3\unpacker.py"
[*] Unpacker started.
[+] Packed data loaded from: EVISION_8th\week_3/packed.dat
[+] Code decoded from Base64. Decoded size: 3615 bytes
[+] Code decompressed. Decompressed size: 6224 bytes
[+] Dummy code removed. Restored size: 6144 bytes
[+] Restored code saved to: EVISION_8th\week_3/restored_code.bin

--- Extracted PE Information ---

[*] Entry Point (VA):
    0x1400013E0

[*] Import Table:
    DLL: KERNEL32.dll
        - DeleteCriticalSection
        - EnterCriticalSection
        - GetLastError
        - InitializeCriticalSection
        - LeaveCriticalSection
        - SetUnhandledExceptionFilter
        - Sleep
        - TlsGetValue
        - VirtualProtect
        - VirtualQuery
    DLL: api-ms-win-crt-environment-l1-1-0.dll
        - __p__environ
    DLL: api-ms-win-crt-heap-l1-1-0.dll
        - _set_new_mode
        - calloc
        - free
        - malloc
    DLL: api-ms-win-crt-math-l1-1-0.dll
        - __setusermatherr
    DLL: api-ms-win-crt-private-l1-1-0.dll
        - __C_specific_handler
        - memcpy
    DLL: api-ms-win-crt-runtime-l1-1-0.dll
        - __p___argc
        - __p___argv
        - _cexit
        - _configure_narrow_argv
        - _crt_atexit
        - _exit
        - _initialize_narrow_environment
        - _initterm
        - _set_app_type
        - _set_invalid_parameter_handler
        - abort
        - exit
        - signal
    DLL: api-ms-win-crt-stdio-l1-1-0.dll
        - __acrt_iob_func
        - __p__commode
        - __p__fmode
        - __stdio_common_vfprintf
        - fwrite
        - puts
    DLL: api-ms-win-crt-string-l1-1-0.dll
        - strlen
        - strncmp

[*] Extracted Strings:
    - Overflow range error 
    -   VirtualQuery failed for 
    -  14.2.0
    - section
    - p, yielding the value 
    - UNDERFLOW
    - PLOSS
    -   VirtualProtect failed with code 0x
    - Argument domain error 
    - Address 
    - DOMAIN
    - s in 
    - matherr
    - p out of range, targeting 
    - w64 runtime failure
    - Partial loss of significance 
    - Rev2, Built by MSYS2 project
    - Argument singularity 
    - runtime error 
    - OVERFLOW
    - Total loss of significance 
    - d bytes at address 
    - retval
    - The result is too small to be represented 
    - Hello, World!
    -   Unknown pseudo relocation protocol version 
    - p has no image
    - d bit pseudo relocation at 
    - TLOSS
    - Mingw
    - Unknown error
    -   Unknown pseudo relocation bit size 

--- End of PE Information ---

[*] Unpacking completed.

[Done] exited with code=0 in 0.077 seconds
```

