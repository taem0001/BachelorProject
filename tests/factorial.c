unsigned int factorial(unsigned int n) {
    if (n == 1) {
        return 1;
    }

    return n * factorial(n - 1);
}

int main() {
    unsigned int res = factorial(5u);
    return res;
}