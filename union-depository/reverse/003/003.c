#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void decrypt_flag(char *encrypted_flag, int key) {
    int len = strlen(encrypted_flag);
    for (int i = 0; i < len; i++) {
        encrypted_flag[i] = encrypted_flag[i] ^ key;
    }
}

int main() {
    char *encrypted_flag = malloc(29);
    strcpy(encrypted_flag, "i~lQNCNu_u_YOuF^XKIOW");

    int key = 42;
    decrypt_flag(encrypted_flag, key);

    printf("Welcome to the simple crackme challenge!\n");
    printf("Can you find the hidden flag?\n");

    char input[29];
    printf("Enter the flag: ");
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = 0;

    if (strcmp(input, encrypted_flag) == 0) {
        printf("Congratulations! You found the correct flag!\n");
    } else {
        printf("Sorry, that's not the correct flag. Try again!\n");
    }

    free(encrypted_flag);
    return 0;
}
