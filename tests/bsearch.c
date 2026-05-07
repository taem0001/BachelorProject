typedef unsigned long size_t;

void *my_bsearch(const void *key, const void *base, size_t nmemb, size_t size,
				 int (*compar)(const void *, const void *)) {
	const unsigned char *array = (const unsigned char *)base;

	while (nmemb > 0) {
		size_t mid = nmemb >> 1;
		size_t offset = 0;
		size_t i = 0;

		while (i < mid) {
			offset += size;
			i++;
		}

		const void *elem = array + offset;

		int cmp = compar(key, elem);

		if (cmp == 0) {
			return (void *)elem;
		}

		if (cmp > 0) {
			array = (const unsigned char *)elem + size;
			nmemb = nmemb - mid - 1;
		} else {
			nmemb = mid;
		}
	}

	return (void *)0;
}

int int_compare(const void *a, const void *b) {
	int x = *(const int *)a;
	int y = *(const int *)b;

	if (x < y) return -1;
	if (x > y) return 1;
	return 0;
}

int main(void) {
	int values[] = {1, 3, 5, 7, 9, 11};
	int key = 8;

	int *found = (int *)my_bsearch(&key, values, 6, sizeof(int), int_compare);

	return found ? 69 : 420;
}