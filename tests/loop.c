int f(int n) {
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        sum += i;
    }
    return sum;
}

int g(int n, int m) {
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            sum += j << 2;
        }
        sum += i << 1;
    }
    return sum;
}

int main() {
    int sum1 = f(5); // 15
    int sum2 = f(8); // 36
    int sum3 = g(5, 3); // 150
    return sum1 + sum2 + sum3;
}