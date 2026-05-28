int f(int a, int b) {
    return a << b;
}

int g(int a, int b) {
    return a >> b;
}

unsigned int h(unsigned int a, unsigned int b) {
    return a >> b;
}

int main() {
    int x = 5;

    int a = f(1, 4);
    int b = g(-12, 2);
    unsigned int c = h(-1u, 16u);

    if (a >> 2 == 4) {
        return b;
    } else if (b >> 1 == -1) {
        return a;
    } else if (c >> 2 == 16383) {
        return c;
    }
    return 1;
}
