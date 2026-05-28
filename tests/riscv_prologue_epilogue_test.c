short test(char x1, char x2, char x3, char x4, char x5, char x6, char x7, char x8, char x9, char x10, char x11, char x12, char x13,
        char x14, char x15, char x16, char x17, char x18, char x19, char x20, char x21, char x22, char x23, char x24, char x25, char x26) {
    return (x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 + x20
                + x21 + x22 + x23 + x24 + x25 + x26);
}


int main() {
    char x1 = 1;
    char x2 = x1 + 1;
    char x3 = x2 + x1;
    char x4 = x3 + x1;
    char x5 = x4 + x1;
    char x6 = x5 + x1;
    char x7 = x6 + x1;
    char x8 = x6 + x1;
    char x9 = x7 + x1;
    char x10 = x8 + x1;
    char x11 = x9 + x1;
    char x12 = x10 + x1;
    char x13 = x11 + x1;
    char x14 = x12 + x1;
    char x15 = x13 + x1;
    char x16 = x14 + x1;
    char x17 = x15 + x1;
    char x18 = x16 + x1;
    char x19 = x16 + x1;
    char x20 = x17 + x1;
    char x21 = x18 + x1;
    char x22 = x19 + x1;
    char x23 = x20 + x1;
    char x24 = x21 + x1;
    char x25 = x22 + x1;
    char x26 = x23 + x1;
    char x27 = x24 + x1;
    char x28 = x25 + x1;
    char x29 = x26 + x1;
    char x30 = x28 + x1;
    char x31 = x29 + x1;
    char x32 = x30 + x1;
    char x33 = x31 + x1;

    short test_res = test(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24, x25, x26);

    short test2_res = test(x33, x32, x31, x10, x11, x12, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x14, x15, x16, x29, x28, x27);
    short res = (x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 + x20
                + x21 + x22 + x23 + x24 + x25 + x26 + x27 + x28 + x29 + x30 + x31 + x32 + x33 + test_res);
    return res + test_res + test2_res;
}