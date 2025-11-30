/* ------------------------------------------------------------------
   bootloader_readable.c – a 512‑byte bootloader that loads the
   kernel from sectors 0–3 (i.e. 4 sectors) and jumps to 0x1000.
   ------------------------------------------------------------------ */
#include <stdint.h>

/* ------------------------------------------------------------------
   Constants – all of them are self‑explanatory.
   ------------------------------------------------------------------ */
#define SECTOR_SIZE        512
#define KERNEL_START_ADDR  0x1000        /* Where we load the kernel */
#define BIOS_INT13         0x13
#define AH_READ_SECTORS    0x02
#define DL_DISK_HDD        0x80          /* First hard‑disk  (LBA 0) */
#define ES_KERN            (KERNEL_START_ADDR >> 4) /* Segment of KERN */
#define BX_KERN_OFFSET     (KERNEL_START_ADDR & 0x0F) /* 16‑bit offset */

/* ------------------------------------------------------------------
   Helper – wrap the BIOS INT 13h sector read.
   The function returns 0 on success, non‑zero on error.
   ------------------------------------------------------------------ */
static inline int bios_read_sectors(uint8_t sector_count,
                                    uint8_t sector_number,
                                    uint16_t lba)
{
    uint16_t es = ES_KERN;
    uint16_t bx = BX_KERN_OFFSET;

    asm volatile (
        /* AH = function, AL = number of sectors, CL = sector #, DL = disk 
*/
        "movb %[sector_count], %%al\n\t"
        "movb %[sector_number], %%cl\n\t"
        "movb %[dl_disk], %%dl\n\t"
        "movb %[ah_read], %%ah\n\t"
        /* ES:BX is already set above */
        "int $0x13\n\t"
        /* AH will contain status code (0 = success) */
        : "=a" (es), "=b" (bx)
        : [sector_count] "i" (sector_count),
          [sector_number] "i" (sector_number),
          [dl_disk] "i" (DL_DISK_HDD),
          [ah_read] "i" (AH_READ_SECTORS)
        : "cx", "dx", "memory"
    );

    /* If AH == 0 => success, otherwise error */
    return es; /* AH is now in 'es' (unused) – we ignore it */
}

/* ------------------------------------------------------------------
   Main bootloader entry point – invoked at 0x7c00.
   ------------------------------------------------------------------ */
void _start(void)
{
    /* Load 4 sectors starting from sector 0 (i.e. the first 4 512‑byte
       blocks of the disk – this is where the kernel lives). */
    for (uint8_t i = 0; i < 4; ++i)
    {
        int err = bios_read_sectors(1, i, i);
        if (err) { /* Simple error handling – just hang */ }
    }

    /* Jump to the kernel entry point – it's at 0x1000. */
    asm volatile ("jmp 0x1000");
}
