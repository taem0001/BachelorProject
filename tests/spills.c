unsigned int spill_stress(unsigned int n) {
    unsigned int a00 = 0u, a01 = 1u, a02 = 2u, a03 = 3u, a04 = 4u;
    unsigned int a05 = 5u, a06 = 6u, a07 = 7u, a08 = 8u, a09 = 9u;
    unsigned int a10 = 10u, a11 = 11u, a12 = 12u, a13 = 13u, a14 = 14u;
    unsigned int a15 = 15u, a16 = 16u, a17 = 17u, a18 = 18u, a19 = 19u;
    unsigned int a20 = 20u, a21 = 21u, a22 = 22u, a23 = 23u, a24 = 24u;
    unsigned int a25 = 25u, a26 = 26u, a27 = 27u, a28 = 28u, a29 = 29u;
    unsigned int a30 = 30u, a31 = 31u, a32 = 32u, a33 = 33u, a34 = 34u;
    unsigned int a35 = 35u, a36 = 36u, a37 = 37u, a38 = 38u, a39 = 39u;

    for (unsigned int i = 0u; i < n; i++) {
        a00 += i + 0u;
        a01 += i + 1u;
        a02 += i + 2u;
        a03 += i + 3u;
        a04 += i + 4u;
        a05 += i + 5u;
        a06 += i + 6u;
        a07 += i + 7u;
        a08 += i + 8u;
        a09 += i + 9u;
        a10 += i + 10u;
        a11 += i + 11u;
        a12 += i + 12u;
        a13 += i + 13u;
        a14 += i + 14u;
        a15 += i + 15u;
        a16 += i + 16u;
        a17 += i + 17u;
        a18 += i + 18u;
        a19 += i + 19u;
        a20 += i + 20u;
        a21 += i + 21u;
        a22 += i + 22u;
        a23 += i + 23u;
        a24 += i + 24u;
        a25 += i + 25u;
        a26 += i + 26u;
        a27 += i + 27u;
        a28 += i + 28u;
        a29 += i + 29u;
        a30 += i + 30u;
        a31 += i + 31u;
        a32 += i + 32u;
        a33 += i + 33u;
        a34 += i + 34u;
        a35 += i + 35u;
        a36 += i + 36u;
        a37 += i + 37u;
        a38 += i + 38u;
        a39 += i + 39u;
    }

    return a00 + a01 + a02 + a03 + a04 + a05 + a06 + a07 + a08 + a09 + a10 + a11 + a12 + a13 + a14 + a15 + a16 + a17 +
           a18 + a19 + a20 + a21 + a22 + a23 + a24 + a25 + a26 + a27 + a28 + a29 + a30 + a31 + a32 + a33 + a34 + a35 +
           a36 + a37 + a38 + a39;
}

int main() {
    unsigned int res = spill_stress(64u);
    res /= 3u;
    return res;
}
