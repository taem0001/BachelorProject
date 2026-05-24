int signed_leaf(signed char a, short b) {
	signed char local_char = -1;
	short local_short = 2;

	return a + b + local_char + local_short;
}

int signed_middle(signed char a, short b) {
	signed char step = 1;
	short offset = 3;

	return signed_leaf((signed char)(a + step), (short)(b + offset));
}

int signed_outer(signed char a) {
	short base = 20;
	signed char lift = 1;

	return signed_middle((signed char)(a + lift), base);
}

int unsigned_leaf(unsigned char a, unsigned short b) {
	unsigned char local_char = 255u;
	unsigned short local_short = 2u;

	return a + b + local_char + local_short;
}

int unsigned_middle(unsigned char a, unsigned short b) {
	unsigned char step = 1u;
	unsigned short offset = 3u;

	return unsigned_leaf((unsigned char)(a + step), (unsigned short)(b + offset));
}

int unsigned_outer(unsigned char a) {
	unsigned short base = 20u;
	unsigned char lift = 1u;

	return unsigned_middle((unsigned char)(a + lift), base);
}

int main() { return unsigned_outer(251u) - signed_outer((signed char)-5); }
