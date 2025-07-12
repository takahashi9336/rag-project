#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 関数1：ファイルから1行読み込む
void read_line_from_file(FILE *fp, char *buffer, int size) {
    fgets(buffer, size, fp);
}

// 関数2：メモリ確保して初期化
char* allocate_and_zero(int size) {
    char *ptr = (char*)malloc(size);
    if (ptr != NULL) {
        memset(ptr, 0, size); // ゼロ初期化
    }
    return ptr;
}

// 関数3：2つの文字列を連結
void concat_strings(char *dest, const char *src1, const char *src2) {
    strcpy(dest, src1);
    strcat(dest, src2);
}

// 関数4：main関数（テスト用）
int main() {
    char buffer[100];
    FILE *fp = fopen("test.txt", "r");
    if (fp) {
        read_line_from_file(fp, buffer, sizeof(buffer));
        printf("Read: %s\n", buffer);
        fclose(fp);
    }

    char *mem = allocate_and_zero(50);
    if (mem) {
        strcpy(mem, "Hello, ");
        strcat(mem, "World!");
        printf("%s\n", mem);
        free(mem);
    }

    char result[100];
    concat_strings(result, "Tree", "Sitter");
    printf("Result: %s\n", result);

    return 0;
}

