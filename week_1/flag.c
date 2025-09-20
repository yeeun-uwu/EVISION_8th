#include <stdio.h>
#include <string.h>

void print_flag() {
    // 4바이트 XOR 키 
    const unsigned char XOR_KEY[] = { 0xDE, 0xAD, 0xBE, 0xEF }; 
    const size_t KEY_LEN = sizeof(XOR_KEY); // 키 길이: 4

    unsigned char flag_data[] = {
        // C R A C K _ V 1 S 1 0 N _ P R J _ D O N E
        0x9d, 0xff, 0x8a, 0xac, 0x95, 0xf2, 0x8d, 0xb9, 
        0xef, 0xfe, 0x8f, 0xdf, 0x90, 0xf2, 0xee, 0xbd, 
        0x94, 0xf2, 0xfa, 0xa0, 0x90, 0xe8, 0xbe
        
    };
    size_t flag_len = sizeof(flag_data) / sizeof(flag_data[0]);

    for (size_t i = 0; i < flag_len; i++) {
        // i % KEY_LEN: 키를 순환하며 적용
        flag_data[i] = flag_data[i] ^ XOR_KEY[i % KEY_LEN]; 
    }
    
    printf("License activated! Your FLAG is: %s\n", (char*)flag_data);
}