int equal(unsigned int a, int b) {
	if (a == b) {
		return 4;
	}
	return 9;
}

int not_equal(int a, unsigned int b) {
	if (a != b) {
		return 8;
	}
	return -4;
}

int greater_than(int a, int b) {
	if (a >= b) {
		return 5;
	}
	return 2;
}

int greater_than_unsigned(unsigned int a, unsigned int b) {
	if (a >= b) {
		return 10;
	}
	return -2;
}

int lesser_than(int a, int b) {
	if (a < b) {
		return 3;
	}
	return -6;
}

int lesser_than_unsigned(unsigned int a, unsigned int b) {
	if (a < b) {
		return 7;
	}
	return -9;
}

int main() {
	int a = equal(5u, 5);					// 4
	int b = not_equal(4, 4u);				// -4
	int c = greater_than(6, -4);			// 5
	int d = greater_than_unsigned(-1u, 4u); // 10
	int e = lesser_than(4, -4);				// -6
	int f = lesser_than_unsigned(4u, 5u);	// 7
	return a + b + c + d + e + f;			// 16
}
