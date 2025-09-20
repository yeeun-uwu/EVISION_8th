### flag.c에 넣을 난독화된 xor 값을 생성하는 스크립트

target = list("CR4CK_3V1S10N_PRJ_DONE")
print(target)

xor_key = [0xDE, 0xAD, 0xBE, 0xEF]
flag_data = []

for i in target:
    print(hex(xor_key[len(flag_data) % 4]))
    flag_data.append(ord(i) ^ xor_key[len(flag_data) % 4])

print([hex(x) for x in flag_data])
