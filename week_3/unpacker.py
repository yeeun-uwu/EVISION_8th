import zlib
import base64
import os

# -- 설정 --
NOW_DIR = os.path.dirname(os.path.abspath(__file__))
PACKED_FILE = '/packed.dat'  # 언패킹할 파일
RESTORED_FILE = '/restored_code.bin'  # 복원된 코드를 저장할 파일
DUMMY_SIZE = 40  # 삽입된 더미 코드 크기
# ----------

print("[*] Unpacker started.")

try:
    # 1. 패킹된 데이터 파일 읽기
    with open(NOW_DIR + PACKED_FILE, 'rb') as f:
        encoded_code = f.read()
    
    print(f"[+] Packed data loaded from: {NOW_DIR + PACKED_FILE}")

    # 2. Base64 디코딩
    compressed_code = base64.b64decode(encoded_code)
    print(f"[+] Code decoded from Base64. Decoded size: {len(compressed_code)} bytes")

    # 3. 코드 압축 해제
    modified_code = zlib.decompress(compressed_code)
    print(f"[+] Code decompressed. Decompressed size: {len(modified_code)} bytes")

    # 4. 더미 코드 제거
    restored_code = modified_code[DUMMY_SIZE:-DUMMY_SIZE] # 앞뒤 제거
    print(f"[+] Dummy code removed. Restored size: {len(restored_code)} bytes")

    # 5. 복원된 코드 파일로 저장
    with open(NOW_DIR + RESTORED_FILE, 'wb') as f:
        f.write(restored_code)

    print(f"[+] Restored code saved to: {NOW_DIR + RESTORED_FILE}")

except FileNotFoundError:
    print(f"[-] FileNotFoundError: '{PACKED_FILE}' not found.")
except Exception as e:
    print(f"[-] Exception: {e}")
