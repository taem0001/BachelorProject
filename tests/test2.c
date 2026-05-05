int f1(int a, int b) { return a + b; }
int f2(int a, int b) { return a - b; }
int main() {
	int a = 11, b = 4;
	int x = f1(a, b);
	a = 4, b = 2;
	int y = f2(a, b);
    int z = x + y;
	return z;
}