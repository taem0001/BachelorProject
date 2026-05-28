int div(int a, int b) {
    return a / b;
}

int mul(int a, int b) {
    return a * b;
}

int rem(int a, int b) {
    return a % b;
}

unsigned int divu(unsigned int a, unsigned int b) {
    return a / b;
}

unsigned int mulu(unsigned int a, unsigned int b) {
    return a * b;
}

unsigned int remu(unsigned int a, unsigned int b) {
    return a % b;
}

int main() {
    int a = div(10, -2);
    int b = mul(-5, 2);
    int c = rem(-13, 5);
    unsigned int d = divu(-1u, 4u);
    unsigned int e = mulu(40u, 5u);
    unsigned int f = remu(13u, 5u);
    return a + b + c + d + e + f;
}