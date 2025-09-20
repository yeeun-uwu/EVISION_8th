#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "flag.h"

const volatile int GLOBAL_HIGH_PART = 4;
const volatile int GLOBAL_LOW_PART = 77;

//체크섬 검증 
int calc_checksum(const char *key) {
    int sum = 0;
    for (size_t i = 0; i < strlen(key); i++) {
        sum += (int)key[i];
    }
    return sum;
}

#define KEY_LENGTH 16
#define BUFFER_SIZE (KEY_LENGTH + 1)

int get_target_checksum(){
    volatile int high = GLOBAL_HIGH_PART;
    volatile int low = GLOBAL_LOW_PART;

    return (high << 8) | low;
}

int main() {
    
    char user_key[BUFFER_SIZE]; // 사용자 키 입력 버퍼

    printf("Enter 16-character license key: ");
    if (scanf("%16s", user_key) != 1) {
        printf("License failed: Input processing error.\n");
        // 길이 넘어가면 입력 실패 처리
        return 0;
    }

    if (strlen(user_key) != KEY_LENGTH) {
        printf("License failed: Key must be 16 characters long.\n");
        return 0;
    }
    
    //문자셋이 영문 대문자, 숫자만 사용되었는지 확인 
    for (int i = 0; i < KEY_LENGTH; i++) {
        if (!isupper(user_key[i]) && !isdigit(user_key[i])) {
            printf("License failed: Key must contain only uppercase letters and digits.\n");
            return 0;
        }
    }

    int checksum = calc_checksum(user_key);

     if (checksum == get_target_checksum()) {
        print_flag(); 
    } else {
        printf("License failed: Invalid key.\n");
    }

}