int spill_stress_mixed_types(int n) {
	char sc00 = 0, sc01 = 1, sc02 = -2, sc03 = 3, sc04 = 4;
	unsigned char uc00 = 5, uc01 = 6, uc02 = 7, uc03 = 8, uc04 = 9;
	short ss00 = 10, ss01 = 11, ss02 = 12, ss03 = 13, ss04 = 14;
	unsigned short us00 = 15, us01 = 16, us02 = 17, us03 = 18, us04 = 19;
	int si00 = 20, si01 = 21, si02 = 22, si03 = 23, si04 = 24;
	unsigned int ui00 = 25, ui01 = 26, ui02 = 27, ui03 = 28, ui04 = 29;
	char sc05 = -30, sc06 = 31, sc07 = -32, sc08 = 33, sc09 = 34;
	unsigned char uc05 = 35, uc06 = 36, uc07 = 37, uc08 = 38, uc09 = 39;

	for (int i = 0; i < n; i++) {
		sc00 += i + 0;
		sc01 += i + 1;
		sc02 += i + 2;
		sc03 += i + 3;
		sc04 += i + 4;
		uc00 += i + 5;
		uc01 += i + 6;
		uc02 += i + 7;
		uc03 += i + 8;
		uc04 += i + 9;
		ss00 += i + 10;
		ss01 += i + 11;
		ss02 += i + 12;
		ss03 += i + 13;
		ss04 += i + 14;
		us00 += i + 15;
		us01 += i + 16;
		us02 += i + 17;
		us03 += i + 18;
		us04 += i + 19;
		si00 += i + 20;
		si01 += i + 21;
		si02 += i + 22;
		si03 += i + 23;
		si04 += i + 24;
		ui00 += i + 25;
		ui01 += i + 26;
		ui02 += i + 27;
		ui03 += i + 28;
		ui04 += i + 29;
		sc05 += i + 30;
		sc06 += i + 31;
		sc07 += i + 32;
		sc08 += i + 33;
		sc09 += i + 34;
		uc05 += i + 35;
		uc06 += i + 36;
		uc07 += i + 37;
		uc08 += i + 38;
		uc09 += i + 39;
	}

	return sc00 + sc01 + sc02 + sc03 + sc04 + uc00 + uc01 + uc02 + uc03 + uc04 + ss00 + ss01 + ss02 + ss03 + ss04 + 
		   us00 + us01 + us02 + us03 + us04 + si00 + si01 + si02 + si03 + si04 + ui00 + ui01 + ui02 + ui03 + ui04 +
		   sc05 + sc06 + sc07 + sc08 + sc09 + uc05 + uc06 + uc07 + uc08 + uc09;
}

int main() {
	int res = spill_stress_mixed_types(64);
	return res;
}
