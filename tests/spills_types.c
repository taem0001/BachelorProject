int spill_stress_mixed_types(int n) {
	char sc00 = 0, sc01 = 1, sc02 = -2, sc03 = 3, sc04 = 4;
	unsigned char uc00 = 5u, uc01 = 6u, uc02 = 7u, uc03 = 8u, uc04 = 9u;
	short ss00 = 10, ss01 = 11, ss02 = 12, ss03 = 13, ss04 = 14;
	unsigned short us00 = 15u, us01 = 16u, us02 = 17u, us03 = 18u, us04 = 19u;
	int si00 = 20, si01 = 21, si02 = 22, si03 = 23, si04 = 24;
	unsigned int ui00 = 25u, ui01 = 26u, ui02 = 27u, ui03 = 28u, ui04 = 29u;
	char sc05 = -30, sc06 = 31, sc07 = -32, sc08 = 33, sc09 = 34;
	unsigned char uc05 = 35u, uc06 = 36u, uc07 = 37u, uc08 = 38u, uc09 = 39u;

	for (int i = 0; i < n; i++) {
		sc00 += i + 0;
		sc01 += i + 1;
		sc02 += i + 2;
		sc03 += i + 3;
		sc04 += i + 4;
		uc00 += i + 5u;
		uc01 += i + 6u;
		uc02 += i + 7u;
		uc03 += i + 8u;
		uc04 += i + 9u;
		ss00 += i + 10;
		ss01 += i + 11;
		ss02 += i + 12;
		ss03 += i + 13;
		ss04 += i + 14;
		us00 += i + 15u;
		us01 += i + 16u;
		us02 += i + 17u;
		us03 += i + 18u;
		us04 += i + 19u;
		si00 += i + 20;
		si01 += i + 21;
		si02 += i + 22;
		si03 += i + 23;
		si04 += i + 24;
		ui00 += i + 25u;
		ui01 += i + 26u;
		ui02 += i + 27u;
		ui03 += i + 28u;
		ui04 += i + 29u;
		sc05 += i + 30;
		sc06 += i + 31;
		sc07 += i + 32;
		sc08 += i + 33;
		sc09 += i + 34;
		uc05 += i + 35u;
		uc06 += i + 36u;
		uc07 += i + 37u;
		uc08 += i + 38u;
		uc09 += i + 39u;
	}

	return sc00 + sc01 + sc02 + sc03 + sc04 + uc00 + uc01 + uc02 + uc03 + uc04 + ss00 + ss01 + ss02 + ss03 + ss04 + 
		   us00 + us01 + us02 + us03 + us04 + si00 + si01 + si02 + si03 + si04 + ui00 + ui01 + ui02 + ui03 + ui04 +
		   sc05 + sc06 + sc07 + sc08 + sc09 + uc05 + uc06 + uc07 + uc08 + uc09;
}

int main() {
	int res = spill_stress_mixed_types(64);
	return res;
}
