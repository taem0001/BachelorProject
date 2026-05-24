int div(int a, int b) {
    return a / b;
}

int mul(int a, int b) {
    return a * b;
}

unsigned int divu(unsigned int a, unsigned int b) {
    return a / b;
}

unsigned int mulu(unsigned int a, unsigned int b) {
    return a * b;
}

int main() {
    int x = div(15, -3);
    int y = mul(6, 3);
    unsigned int z = divu(-1u, 2u);
    unsigned int k = mulu(400u, 600u);
    unsigned int res = z + k;

    return res;
}