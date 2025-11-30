/* ------------------------------------------------------------------
   bootloader_unreadable.c – the same logic as the readable version
   but intentionally obfuscated to make it “extremely unreadable”.
   ------------------------------------------------------------------ */
#include <stdint.h>

/* ------------------------------------------------------------------
   1.  Very long, nonsense identifiers
   2.  Heavy use of macros – each macro expands to a small block of
       code, making the control flow hard to follow.
   ------------------------------------------------------------------ */
#define U0P5Z4E 512
#define K0R3N3 0x1000
#define B1_0 0x13
#define A_H1R 0x02
#define D_L 0x80
#define E_S_K (K0R3N3 >> 4)
#define B_X_K (K0R3N3 & 0x0F)

/*------------------------------------------------------------------
   A single macro that expands into an inline assembly block.
   The macro arguments are purposely named “x”, “y”, “z” – no
   semantic hinting.
   ------------------------------------------------------------------*/
#define _R3AD_(x,y,z)                                            \
    asm volatile (                                               \
        "movb %[x], %%al\n\t"                                    \
        "movb %[y], %%cl\n\t"                                    \
        "movb %[z], %%dl\n\t"                                    \
        "movb %[A_H1R], %%ah\n\t"                                \
        "int $0x13\n\t"                                          \
        : "=a" (z), "=b" (x)                                     \
        : [x] "i" (x), [y] "i" (y), [z] "i" (z),                \
          [z] "i" (z), [A_H1R] "i" (A_H1R)                       \
        : "cx", "dx", "memory"                                   \
    )

/*------------------------------------------------------------------
   “Main” – it looks like a random string of numbers.
   ------------------------------------------------------------------*/
void _s2t7(void)
{
    /* 4 loop iterations – but the loop counter is stored in a
       magic constant “0xF” (decimal 15) – look! */
    for (uint8_t N9K = 0; N9K < 0xF; ++N9K)
    {
        /* The call to the macro above – the arguments are
           deliberately shuffled. */
        _R3AD_(1, N9K, N9K);
    }

    /* The final jump – the address is split into segment:offset
       and the values are shuffled again. */
    asm volatile ("jmp %0:%1"
        : : "n" (E_S_K), "n" (B_X_K));
}
