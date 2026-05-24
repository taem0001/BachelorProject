typedef unsigned long usize;

void *my_memcpy(void *dst, const void *src, usize n) {
    unsigned char *d = (unsigned char *)dst;
    const unsigned char *s = (const unsigned char *)src;

    while (n != 0) {
        *d = *s;
        d++;
        s++;
        n--;
    }

    return dst;
}

int main(void) {
    int src[4] = {1, 2, 3, 6};
    int dst[4];

    my_memcpy(dst, src, sizeof(src));

    return dst[0] + dst[1] + dst[2] + dst[3];
}