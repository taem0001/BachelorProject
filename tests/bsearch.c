typedef unsigned long size_t;

void *my_bsearch(const void *key, const void *base0, size_t nmemb, size_t size,
				 int (*compar)(const void *, const void *)) {
	const char *base = (const char *)base0;
	int lim, cmp;
	const void *p;

	for (lim = nmemb; lim != 0; lim >>= 1) {
		p = base + (lim >> 1) * size;
		cmp = (*compar)(key, p);
		if (cmp == 0) return (void *)p;
		if (cmp > 0) {
			base = (const char *)p + size;
			lim--;
		}
	}
	return ((void *)0);
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
	int key = 7;

	int *found = (int *)my_bsearch(&key, values, 6, sizeof(int), int_compare);

	return found ? 1 : 2;
}