char *my_strcpy(char *dest, const char *src) {
	char *original_dest = dest;

	while ((*dest = *src) != '\0') {
		dest++;
		src++;
	}

	return original_dest;
}

int main(void) {
	char src[] = "hello";
	char dest[6];

	my_strcpy(dest, src);

	if (dest[0] == 'h' && dest[1] == 'e' && dest[2] == 'l' && dest[3] == 'l' && dest[4] == 'o' && dest[5] == '\0') {
		return 1;
	}

	return 2;
}