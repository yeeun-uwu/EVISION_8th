import zlib
import base64
import os
import json

# -- 설정 --
NOW_DIR = os.path.dirname(os.path.abspath(__file__))
PACKED_FILE = '/packed.dat'  # 언패킹할 파일
RESTORED_FILE = '/restored_code.bin'  # 복원된 코드를 저장할 파일
DUMMY_SIZE = 40  # 삽입된 더미 코드 크기
# ----------

# -- 디버거 탐지 함수 --
import ctypes

def check_debugger():
    try:
        kernel32 = ctypes.windll.kernel32

        if kernel32.IsDebuggerPresent():
            return True
        return False
    except Exception as e:
        print(f"[!] Debugger detection error: {e}")
        return False

# -- vm 탐지 함수 --

import uuid

VM_MAC_PREFIXES = [
    "00:05:69",  # VMware
    "00:0C:29",  # VMware
    "00:1C:14",  # VMware
    "00:50:56",  # VMware
    "08:00:27",  # VirtualBox
    "0A:00:27",  # VirtualBox
    "00:15:5D",  # Hyper-V
    "00:03:FF",  # Microsoft Virtual PC
]

def check_vm():
    try:
        mac_int = uuid.getnode()
        mac_str = ':'.join(['{:02x}'.format((mac_int >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])

        for prefix in VM_MAC_PREFIXES:
            if mac_str.upper().startswith(prefix):
                return True
        return False
    except Exception as e:
        print(f"[!] VM detection error: {e}")
        return False


print("[*] Unpacker started.")

try:
    # 디버거 / 가상머신 탐지
    if check_debugger():
        raise Exception("[-] Debugger detected! Exiting unpacker.")
    if check_vm():
        raise Exception("[-] Virtual Machine detected! Exiting unpacker.")

    # 1. 패킹된 데이터 파일 읽기
    with open(NOW_DIR + PACKED_FILE, 'rb') as f:
        json_bytes = f.read()
    
    print(f"[+] Packed data loaded from: {NOW_DIR + PACKED_FILE}")

    # 2. JSON 데이터 파싱
    packed_data_dict = json.loads(json_bytes.decode('utf-8'))
    
    # 2-1. 패킹된 코드 데이터 추출
    encoded_code = packed_data_dict.get('encoded_code')
    if not encoded_code:
        raise Exception("[-] 'packed_code' not found in JSON data.")
        
    # 2-2. PE 정보 추출
    ep_va = packed_data_dict.get('entry_point_va', 0)
    import_table = packed_data_dict.get('imports', [])
    strings = packed_data_dict.get('strings', [])

    # 3. Base64 디코딩
    compressed_code = base64.b64decode(encoded_code.encode('utf-8'))
    print(f"[+] Code decoded from Base64. Decoded size: {len(compressed_code)} bytes")

    # 4. 코드 압축 해제
    modified_code = zlib.decompress(compressed_code)
    print(f"[+] Code decompressed. Decompressed size: {len(modified_code)} bytes")

    # 5. 더미 코드 제거
    restored_code = modified_code[DUMMY_SIZE:-DUMMY_SIZE] # 앞뒤 제거
    print(f"[+] Dummy code removed. Restored size: {len(restored_code)} bytes")

    # 6. 복원된 코드 파일로 저장
    with open(NOW_DIR + RESTORED_FILE, 'wb') as f:
        f.write(restored_code)

    print(f"[+] Restored code saved to: {NOW_DIR + RESTORED_FILE}")

    # 7. PE 정보 출력
    print("\n--- Extracted PE Information ---")
    
    print(f"\n[*] Entry Point (VA):")
    print(f"    0x{ep_va:X}")
    
    print(f"\n[*] Import Table:")
    for dll_info in import_table:
        print(f"    DLL: {dll_info['dll']}")
        for func in dll_info['functions']:
            print(f"        - {func}")
            
    print(f"\n[*] Extracted Strings:")
    for s in strings:
        print(f"    - {s}")

    print("\n--- End of PE Information ---")
    print("\n[*] Unpacking completed.")

except json.JSONDecodeError as e:
    print(f"[-] JSONDecodeError: Failed to parse JSON data. {e}")

except FileNotFoundError:
    print(f"[-] FileNotFoundError: '{PACKED_FILE}' not found.")

except Exception as e:
    print(f"{e}")
