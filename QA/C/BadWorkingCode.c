// Standard C libraries (because why not include EVERYTHING)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <ctype.h>
#include <limits.h>
#include <float.h>
#include <errno.h>
#include <signal.h>
#include <setjmp.h>
#include <stdarg.h>
#include <stddef.h>

// POSIX libraries (let's go overboard)
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <dirent.h>
#include <pthread.h>
#include <semaphore.h>

// Network libraries (why not?)
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>

// Graphics libraries (totally unnecessary)
#include <X11/Xlib.h>
#include <X11/Xutil.h>

// Audio libraries (because calculation needs sound?)
#include <alsa/asoundlib.h>

// Compression libraries (for no reason)
#include <zlib.h>
#include <bzlib.h>

// Cryptography (security through absurdity)
#include <openssl/md5.h>
#include <openssl/sha.h>

// JSON parsing (why not?)
#include <json-c/json.h>

// Exotic includes just to be ridiculous
#include <tiffio.h>
#include <jpeglib.h>
#include <png.h>


#define CHAOS_FACTOR 0xDEADBEEF
#define RANDOM_SEED 42
#define ENTROPY_LEVEL 9001

volatile int global_entropy = 0;



// Union of chaos
union MathChaosUnion {
    int integer_value;
    float float_value;
    double double_value;
    char char_value;
    void* pointer_value;
    uint64_t bit_chaos;
    struct {
        int x;
        int y;
    } coordinate;
    unsigned char byte_array[sizeof(double)];
};

int super_union_calculator(int a, int b, char op) {
    // Create a union that will hold our calculation chaos
    union MathChaosUnion input_a = { .integer_value = a };
    union MathChaosUnion input_b = { .integer_value = b };
    union MathChaosUnion result_union = { 0 };

    // Perform calculations using union shenanigans
    switch(op) {
        case '+':
            // Add using bit manipulation and union trickery
            result_union.bit_chaos = 
                input_a.bit_chaos + 
                input_b.bit_chaos ^ CHAOS_MAGIC;
            break;
        
        case '-':
            // Subtraction with coordinate swap
            result_union.coordinate.x = input_a.integer_value;
            result_union.coordinate.y = input_b.integer_value;
            result_union.integer_value = 
                result_union.coordinate.x - 
                result_union.coordinate.y;
            break;
        
        case '*':
            // Multiplication via float shenanigans
            input_a.float_value = (float)input_a.integer_value;
            input_b.float_value = (float)input_b.integer_value;
            result_union.float_value = 
                input_a.float_value * input_b.float_value;
            result_union.integer_value ^= UNION_WTFACTOR;
            break;
        
        case '/':
            // Division with multiple representation checks
            if (input_b.integer_value == 0) {
                // Division by zero? No problem!
                result_union.bit_chaos = CHAOS_MAGIC;
            } else {
                // Use double for "precision"
                input_a.double_value = (double)input_a.integer_value;
                input_b.double_value = (double)input_b.integer_value;
                result_union.double_value = 
                    input_a.double_value / input_b.double_value;
                
                // Scramble the result because why not
                for (int i = 0; i < sizeof(result_union.byte_array); i++) {
                    result_union.byte_array[i] ^= 
                        (result_union.byte_array[i] << 1) & 0xFF;
                }
            }
            break;
        
        case '%':
            // Modulo with pointer-based chaos
            result_union.pointer_value = &input_a;
            result_union.integer_value = 
                input_a.integer_value % input_b.integer_value;
            result_union.char_value = 
                result_union.integer_value & 0xFF;
            break;
        
        default:
            // Ultimate chaos mode
            result_union.bit_chaos = 
                input_a.bit_chaos ^ 
                input_b.bit_chaos ^ 
                CHAOS_MAGIC;
    }

    // Return the integer representation of our chaotic result
    return result_union.integer_value;
}

int main() {
    // Demonstrate the horror
    printf("5 + 3 = %d\n", super_awful_calculator(5, 3, '+'));
    printf("10 - 4 = %d\n", super_awful_calculator(10, 4, '-'));
    printf("6 * 7 = %d\n", super_awful_calculator(6, 7, '*'));
    printf("20 / 5 = %d\n", super_awful_calculator(20, 5, '/'));
    printf("17 % 5 = %d\n", super_awful_calculator(17, 5, '%'));
    
    // Bonus: division by zero handling that makes no sense
    printf("Divide by zero = %d\n", super_awful_calculator(10, 0, '/'));
    
    return 0;
}
