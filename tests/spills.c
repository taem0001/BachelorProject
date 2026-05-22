int spill_stress(int n) {
	signed char a00 = 0, a01 = 1, a02 = 2, a03 = 3, a04 = 4;
	signed char a05 = 5, a06 = 6, a07 = 7, a08 = 8, a09 = 9;
	unsigned char a10 = 10, a11 = 11, a12 = 12, a13 = 13, a14 = 14;
	unsigned short a15 = 15, a16 = 16, a17 = 17, a18 = 18, a19 = 19;
	signed short a20 = 20, a21 = 21, a22 = 22, a23 = 23, a24 = 24;
	unsigned short a25 = 25, a26 = 26, a27 = 27, a28 = 28, a29 = 29;
	signed short a30 = 30, a31 = 31, a32 = 32, a33 = 33, a34 = 34;
	unsigned char a35 = 35, a36 = 36, a37 = 37, a38 = 38, a39 = 39;

	for (int i = 0; i < n; i++) {
		a00 += i + 0;
		a01 += i + 1;
		a02 += i + 2;
		a03 += i + 3;
		a04 += i + 4;
		a05 += i + 5;
		a06 += i + 6;
		a07 += i + 7;
		a08 += i + 8;
		a09 += i + 9;
		a10 += i + 10;
		a11 += i + 11;
		a12 += i + 12;
		a13 += i + 13;
		a14 += i + 14;
		a15 += i + 15;
		a16 += i + 16;
		a17 += i + 17;
		a18 += i + 18;
		a19 += i + 19;
		a20 += i + 20;
		a21 += i + 21;
		a22 += i + 22;
		a23 += i + 23;
		a24 += i + 24;
		a25 += i + 25;
		a26 += i + 26;
		a27 += i + 27;
		a28 += i + 28;
		a29 += i + 29;
		a30 += i + 30;
		a31 += i + 31;
		a32 += i + 32;
		a33 += i + 33;
		a34 += i + 34;
		a35 += i + 35;
		a36 += i + 36;
		a37 += i + 37;
		a38 += i + 38;
		a39 += i + 39;
	}

	return a00 + a01 + a02 + a03 + a04 + a05 + a06 + a07 + a08 + a09 + a10 + a11 + a12 + a13 + a14 + a15 + a16 + a17 +
		   a18 + a19 + a20 + a21 + a22 + a23 + a24 + a25 + a26 + a27 + a28 + a29 + a30 + a31 + a32 + a33 + a34 + a35 +
		   a36 + a37 + a38 + a39;
}

int main() {
	int res = spill_stress(64);
	return res;
}
