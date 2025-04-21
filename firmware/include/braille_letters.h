#ifndef BRAILLE_LETTERS_H
#define BRAILLE_LETTERS_H

#include <stdint.h>

typedef enum letter_status_e{
    LETTER_STATUS_OK,
    IS_NOT_A_LETTER
} letter_status_t;

uint8_t* get_braille_pattern(char c);
letter_status_t check_letter(char c);
void apply_braille_to_servos(char c);

#endif