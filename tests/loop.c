unsigned short f(signed char n) {
    unsigned short sum = 0u;
    for (unsigned char i = 1u; i <= (unsigned char)n; i++) {
        sum = (unsigned short)(sum + (unsigned short)i);
    }
    return sum;
}

long g(unsigned short n, signed char m) {
    long sum = 0;
    for (unsigned short i = 1u; i <= n; i++) {
        for (unsigned char j = 1u; j <= (unsigned char)m; j++) {
            sum += (long)j << 2;
        }
        sum += (long)i << 1;
    }
    return sum;
}

int main() {
    unsigned short sum1 = f((signed char)5); // 15
    int sum2 = f((signed char)8); // 36
    unsigned int sum3 = (unsigned int)g((unsigned short)5, (signed char)3); // 150
    return sum1 + sum2 + sum3;
}