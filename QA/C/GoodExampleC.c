#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/aes.h>

#define BLOCK_SIZE AES_BLOCK_SIZE
#define HEX_BUF_SZ 4096

/* --------------------------------------------------------------------- 
*/
/*  Hex helpers                                                          
  */
/* --------------------------------------------------------------------- 
*/

static void hex_encode(const unsigned char *bin, size_t len, char *hex)
{
    static const char *const hex_chars = "0123456789abcdef";
    for (size_t i = 0; i < len; ++i) {
        unsigned char b = bin[i];
        hex[2 * i]     = hex_chars[(b >> 4) & 0x0F];
        hex[2 * i + 1] = hex_chars[b & 0x0F];
    }
    hex[2 * len] = '\0';
}

static int hex_decode(const char *hex, unsigned char *bin, size_t 
*out_len)
{
    size_t hex_len = strlen(hex);
    if (hex_len % 2 != 0) return -1;          /* odd number of hex digits 
*/

    size_t len = hex_len / 2;
    for (size_t i = 0; i < len; ++i) {
        char high = hex[2 * i];
        char low  = hex[2 * i + 1];
        unsigned char hb = (high >= '0' && high <= '9') ? high - '0' :
                           (high >= 'a' && high <= 'f') ? high - 'a' + 10 
:
                           (high >= 'A' && high <= 'F') ? high - 'A' + 10 
: 255;
        unsigned char lb = (low  >= '0' && low  <= '9') ? low  - '0' :
                           (low  >= 'a' && low  <= 'f') ? low  - 'a' + 10 
:
                           (low  >= 'A' && low  <= 'F') ? low  - 'A' + 10 
: 255;
        if (hb == 255 || lb == 255) return -1;
        bin[i] = (hb << 4) | lb;
    }
    *out_len = len;
    return 0;
}

/* --------------------------------------------------------------------- 
*/
/*  AES helpers                                                          
  */
/* --------------------------------------------------------------------- 
*/

static int aes_ecb_encrypt(const unsigned char *in, size_t in_len,
                          const unsigned char *key,
                          unsigned char *out)
{
    AES_KEY aes_key;
    if (AES_set_encrypt_key(key, 128, &aes_key) < 0) return -1;

    if (in_len % BLOCK_SIZE) return -1;   /* must be multiple of block */

    for (size_t i = 0; i < in_len; i += BLOCK_SIZE) {
        AES_encrypt(in + i, out + i, &aes_key);
    }
    return 0;
}

static int aes_ecb_decrypt(const unsigned char *in, size_t in_len,
                          const unsigned char *key,
                          unsigned char *out)
{
    AES_KEY aes_key;
    if (AES_set_decrypt_key(key, 128, &aes_key) < 0) return -1;

    if (in_len % BLOCK_SIZE) return -1;   /* must be multiple of block */

    for (size_t i = 0; i < in_len; i += BLOCK_SIZE) {
        AES_decrypt(in + i, out + i, &aes_key);
    }
    return 0;
}

/* --------------------------------------------------------------------- 
*/
/*  Main entry                                                           
  */
/* --------------------------------------------------------------------- 
*/

int main(int argc, char **argv)
{
    if (argc != 4) {
        fprintf(stderr,
                "Usage: %s <enc|dec> <hex‑key‑32‑chars> <hex‑data>\n",
                argv[0]);
        return EXIT_FAILURE;
    }

    const char *mode = argv[1];
    const char *key_hex = argv[2];
    const char *data_hex = argv[3];

    unsigned char key[BLOCK_SIZE];
    size_t key_len;
    if (hex_decode(key_hex, key, &key_len) != 0 || key_len != BLOCK_SIZE) 
{
        fprintf(stderr, "Invalid key: must be 32 hex characters\n");
        return EXIT_FAILURE;
    }

    unsigned char data[HEX_BUF_SZ];
    size_t data_len;
    if (hex_decode(data_hex, data, &data_len) != 0) {
        fprintf(stderr, "Invalid data: hex string expected\n");
        return EXIT_FAILURE;
    }

    /* Allocate output buffer */
    unsigned char out[HEX_BUF_SZ];
    if (strcmp(mode, "enc") == 0) {
        if (aes_ecb_encrypt(data, data_len, key, out) != 0) {
            fprintf(stderr, "Encryption failed (data must be a multiple of 16 bytes)\n");
            return EXIT_FAILURE;
        }
    } else if (strcmp(mode, "dec") == 0) {
        if (aes_ecb_decrypt(data, data_len, key, out) != 0) {
            fprintf(stderr, "Decryption failed (data must be a multiple of 16 bytes)\n");
            return EXIT_FAILURE;
        }
    } else {
        fprintf(stderr, "Unknown mode: %s (must be \"enc\" or \"dec\")\n", mode);
        return EXIT_FAILURE;
    }

    char hex_out[2 * HEX_BUF_SZ + 1];
    hex_encode(out, data_len, hex_out);
    printf("%s\n", hex_out);

    return EXIT_SUCCESS;
}
