#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

// Compact error handling enum
typedef enum {
    CALC_OK,
    ERR_DIV_ZERO,
    ERR_OVERFLOW,
    ERR_INVALID_OP
} CalcError;

// Function pointer type for operations
typedef int64_t (*MathOperation)(const int64_t*, const int64_t*);

// Pointer-based mathematical operations
int64_t add_op(const int64_t* a, const int64_t* b) { return *a + *b; }
int64_t sub_op(const int64_t* a, const int64_t* b) { return *a - *b; }
int64_t mul_op(const int64_t* a, const int64_t* b) { return *a * *b; }

// Safe division with pointer handling
int64_t div_op(const int64_t* a, const int64_t* b) {
    return *b != 0 ? *a / *b : 0;
}

// Modulo with pointer safety
int64_t mod_op(const int64_t* a, const int64_t* b) {
    return *b != 0 ? *a % *b : 0;
}

// Calculation structure for advanced state management
typedef struct {
    int64_t* result;         // Pointer to calculation result
    CalcError* status;       // Pointer to error status
    MathOperation operation; // Function pointer for math operation
} CalcContext;

// Unified calculation engine with pointer-based design
void calculate(const int64_t* a, const int64_t* b, CalcContext* ctx) {
    // Validate input pointers
    if (!a || !b || !ctx->result || !ctx->status || !ctx->operation) {
        if (ctx->status) *ctx->status = ERR_INVALID_OP;
        return;
    }

    // Perform calculation via function pointer
    *ctx->result = ctx->operation(a, b);
    *ctx->status = CALC_OK;
}

// Interactive calculator with pointer-based design
int main() {
    // Allocate memory for key components
    int64_t* num1 = malloc(sizeof(int64_t));
    int64_t* num2 = malloc(sizeof(int64_t));
    int64_t* result = malloc(sizeof(int64_t));
    CalcError* status = malloc(sizeof(CalcError));

    // Operation lookup table
    MathOperation ops[] = {
        ['+'] = add_op,
        ['-'] = sub_op,
        ['*'] = mul_op,
        ['/'] = div_op,
        ['%'] = mod_op
    };

    // Main calculation loop
    while (1) {
        // Reset status
        *status = CALC_OK;

        // User input prompt
        printf("Enter calculation (number operator number): ");
        
        // Safe input with pointer-based parsing
        if (scanf("%ld %*c %ld", num1, num2) != 2) {
            printf("Invalid input format!\n");
            // Clear input buffer
            while (getchar() != '\n');
            continue;
        }

        // Capture operation
        char op;
        scanf(" %c", &op);

        // Prepare calculation context
        CalcContext ctx = {
            .result = result,
            .status = status,
            .operation = ops[op]
        };

        // Perform calculation
        calculate(num1, num2, &ctx);

        // Error handling
        switch (*status) {
            case CALC_OK:
                printf("Result: %ld\n", *result);
                break;
            case ERR_DIV_ZERO:
                printf("Error: Division by zero\n");
                break;
            default:
                printf("Calculation error\n");
        }

        printf("Continue? (y/n): ");
        // Continue prompt handling
        char continue_choice;
        scanf(" %c", &continue_choice);
        
        if (continue_choice != 'y' && continue_choice != 'Y') {
            break;
        }
    }

    // Critical: Memory cleanup
    free(num1);
    free(num2);
    free(result);
    free(status);

    return 0;
}
