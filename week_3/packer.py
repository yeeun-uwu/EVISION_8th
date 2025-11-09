import pefile
import zlib
import base64
import os

# -- 설정 --
NOW_DIR = os.path.dirname(os.path.abspath(__file__))
EXE_FILE_PATH = '/hello.exe'  # 분석할 실행 파일 경로
PACKED_FILE = '/packed.dat'  # 압축된 데이터를 저장할 파일
# ----------

print("[*] Packer started.")

try:
    # 1. PE 파일 로드
    pe = pefile.PE(NOW_DIR + EXE_FILE_PATH)
    print(f"[+] Loaded PE file: {NOW_DIR + EXE_FILE_PATH}")

    # 2. .text 섹션 찾기
    text_section = None
    for section in pe.sections:
        if section.Name.startswith(b'.text'):
            text_section = section
            break

    if not text_section:
        raise Exception("[-] .text section not found.")
    
    # 3. .text 섹션 데이터 추출
    original_code = text_section.get_data()
    print(f"[+] .text section found. Size: {len(original_code)} bytes")

    # 4. 더미 코드 삽입 (NOP 추가)
    dummy_code = b'\x90' * 40  # 40 바이트의 NOP 코드
    modified_code = dummy_code + original_code + dummy_code # 앞뒤로 추가
    print(f"[+] Dummy code inserted. New size: {len(modified_code)} bytes")

    # 5. 코드 압축
    compressed_code = zlib.compress(modified_code)
    print(f"[+] Code compressed. Compressed size: {len(compressed_code)} bytes")

    # 6. 압축된 코드 Base64 인코딩
    encoded_code = base64.b64encode(compressed_code)
    print(f"[+] Code encoded to Base64. Encoded size: {len(encoded_code)} bytes")

    # 7. 압축된 데이터 파일로 저장
    with open(NOW_DIR+PACKED_FILE, 'wb') as f:
        f.write(encoded_code)

    print(f"[+] Packed data saved to: {NOW_DIR+PACKED_FILE}")

except pefile.PEFormatError as e:
    print(f"[-] PEFormatError: '{EXE_FILE_PATH}' is not valid PE file. {e}")
except FileNotFoundError:
    print(f"[-] FileNotFoundError: '{EXE_FILE_PATH}' not found.")
except Exception as e:
    print(f"[-] Exception: {e}")