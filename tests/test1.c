int f1(int a, int b) {
    return a + b;
}
int f2(unsigned int a, int b) {
    return a - b;
}
int f3(int a, unsigned int b) {
    return a >> b;
}
unsigned int f4(unsigned int a, unsigned int b) {
    return a << b;
}
int main() {
    int x = f1(5, 3);
    int y = f2(10, 4);
    int z = f3(16, 2);
    unsigned int w = f4(1, 3);
    return x + y + z + w;
}