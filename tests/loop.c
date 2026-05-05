int f(int n) {
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        sum += i;
    }
    return sum;
}

int main() {
    int sum1 = f(5);
    int sum2 = f(8);
    return sum1 + sum2;
}