#include <stdint.h>

int f_beq(int a, int b) {
    if (a == b)
        return a + b;
    else
        return a - b;
}

int f_bne(int a, int b) {
    if (a != b)
        return a + 1;
    else
        return b + 1;
}

int f_blt(int a, int b) {
    if (a < b)
        return a * 2;
    else
        return b * 2;
}

int f_bge(int a, int b) {
    if (a >= b)
        return a / 2;
    else
        return b / 2;
}

unsigned int f_bltu(unsigned int a, unsigned int b) {
    if (a < b)
        return a + b;
    else
        return a - b;
}

unsigned int f_bgeu(unsigned int a, unsigned int b) {
    if (a >= b)
        return a ^ b;
    else
        return a | b;
}

int main() {
    int x1 = f_beq(5, 5);
    int x2 = f_bne(5, 3);
    int x3 = f_blt(-2, 7);
    int x4 = f_bge(9, 4);
    unsigned int x5 = f_bltu(3u, 8u);
    unsigned int x6 = f_bgeu(12u, 4u);

    return x1 + x2 + x3 + x4 + (int)x5 + (int)x6;
}