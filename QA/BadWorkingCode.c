#include <stdio.h>

#define WTF_IS_MATH 1
#define MAGIC_NUMBER 42
#define DONT_TOUCH_THIS 666

int super_awful_calculator(int a, int b, char op) {
    // Absolutely no input validation? Check!
    int result = 0;
    
    // Nested ternary operators for maximum unreadability
    result = op == '+' ? a + b : 
             op == '-' ? a - b : 
             op == '*' ? a * b : 
             op == '/' ? (b != 0 ? a / b : MAGIC_NUMBER) : 
             op == '%' ? a % b : 
             DONT_TOUCH_THIS;
    
    // Random global variable side effect because why not?
    static int total_calculations = 0;
    total_calculations += WTF_IS_MATH;
    
    // Completely unnecessary and confusing type casting
    return (int)((double)result * 1.0);
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
