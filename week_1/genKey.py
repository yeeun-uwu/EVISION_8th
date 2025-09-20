import string

target_checksum = (4<<8) + 0x4D
print(target_checksum)
KEY_LENGTH = 16

base_char_code = ord("0") # 48

def gen_valid_key():
    codes = [base_char_code] * KEY_LENGTH
    current_sum = sum(codes)
    remaining = target_checksum - current_sum

    alphabet_num = remaining // 17
    # 0에서 알파벳 대문자(A)로 넘어가려면 17 이상의 수가 더해져야 하므로 
    # 최대 알파벳 수를 구함 
    num_to_convert = min(alphabet_num, KEY_LENGTH)
    # 뒤에서부터 (KEY_LENGTH - 1)부터 역순으로 인덱스 접근해 알파벳(A)로 변환
    for i in range(0, num_to_convert):
        codes[i] = ord('A')

    remaining = target_checksum - sum(codes) # 재계산
    index = 0

    while remaining > 0 and index < KEY_LENGTH:
        current_code = codes[index]
        max_increase = ord('Z') - current_code 

        if current_code < ord('A'):
            max_increase = ord('9') - current_code

        increase = min(remaining, max_increase)
        codes[index] += increase
        remaining -= increase
        index += 1
    
    valid_key = "".join([chr(c) for c in codes])
    return valid_key

print("Valid Key:", gen_valid_key())