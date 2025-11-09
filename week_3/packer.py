import pefile
import zlib
import base64
import os
import json

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
    print("")

    # 4. PE 정보 추출 
    print("[*] Extracting PE information...")

    # 4-1. EP 추출
    entry_point = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    image_base = pe.OPTIONAL_HEADER.ImageBase
    ep_va = image_base + entry_point
    print(f"[+] Original Entry Point RVA: {hex(entry_point)}")
    print(f"[+] Entry Point VA: {hex(ep_va)}")

    # 4-2. IAT 추출
    import_list = []
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            dll_name = entry.dll.decode('utf-8')
            functions = []
            for imp in entry.imports:
                func_name = imp.name.decode('utf-8') if imp.name else f"Ordinal_{imp.ordinal}"
                functions.append(func_name)
            import_list.append({'dll': dll_name, 'functions': functions})
            print(f"[+] Found IAT entry: {dll_name} with {len(functions)} functions")

    # 4-3. 문자열 정보 추출
    # .rdata 섹션에서 printable 추출
    string_list = []
    for section in pe.sections:
        if section.Name.startswith(b'.rdata'):
            try:
                import re
                printable_strings = re.findall(br"[a-zA-Z0-9\s.,!?]{5,}", section.get_data())
                string_list = list(set([s.decode('utf-8') for s in printable_strings]))
                print(f"[+] Found {len(string_list)} strings in .rdata")
            except Exception as e:
                print(f"[-] Error extracting strings: {e}")
                pass

    # 5. 더미 코드 삽입 (NOP 추가)
    dummy_code = b'\x90' * 40  # 40 바이트의 NOP 코드
    modified_code = dummy_code + original_code + dummy_code # 앞뒤로 추가
    print(f"[+] Dummy code inserted. New size: {len(modified_code)} bytes")

    # 6. 코드 압축
    compressed_code = zlib.compress(modified_code)
    print(f"[+] Code compressed. Compressed size: {len(compressed_code)} bytes")

    # 7. 압축된 코드 Base64 인코딩
    encoded_code = base64.b64encode(compressed_code)
    print(f"[+] Code encoded to Base64. Encoded size: {len(encoded_code)} bytes")

    # 8. 모든 정보 json 패키징
    packed_data = {
        'entry_point_rva': entry_point,
        'entry_point_va': ep_va,
        'imports': import_list,
        'strings': string_list,
        'encoded_code': encoded_code.decode('utf-8')
    }

    final_data_bytes = json.dumps(packed_data, indent = 4).encode('utf-8')
    with open(NOW_DIR+PACKED_FILE, 'wb') as f:
        f.write(final_data_bytes)

    print(f"\n[+] Packed data saved to: {NOW_DIR+PACKED_FILE}")

except pefile.PEFormatError as e:
    print(f"[-] PEFormatError: '{EXE_FILE_PATH}' is not valid PE file. {e}")
except FileNotFoundError:
    print(f"[-] FileNotFoundError: '{EXE_FILE_PATH}' not found.")
except Exception as e:
    print(f"[-] Exception: {e}")