#ifndef BRAILLE_LETTERS_H
#define BRAILLE_LETTERS_H

#include <stdint.h>

extern uint8_t a_braille[6]; 
extern uint8_t b_braille[6];
extern uint8_t c_braille[6];
extern uint8_t d_braille[6];
extern uint8_t e_braille[6];
extern uint8_t f_braille[6];
extern uint8_t g_braille[6];
extern uint8_t h_braille[6];
extern uint8_t i_braille[6];
extern uint8_t j_braille[6];
extern uint8_t k_braille[6];
extern uint8_t l_braille[6];
extern uint8_t m_braille[6];
extern uint8_t n_braille[6];
extern uint8_t o_braille[6];
extern uint8_t p_braille[6];
extern uint8_t q_braille[6];
extern uint8_t r_braille[6];
extern uint8_t s_braille[6];
extern uint8_t t_braille[6];
extern uint8_t u_braille[6];
extern uint8_t v_braille[6];
extern uint8_t w_braille[6];
extern uint8_t x_braille[6];
extern uint8_t y_braille[6];
extern uint8_t z_braille[6];


typedef enum letter_status_e
{
    LETTER_STATUS_OK = 0,
    IS_NOT_A_LETTER = 1,
} letter_status_t;


uint8_t* get_braille_pattern(char c);
letter_status_t check_letter(char c);
void apply_braille_to_servos(char c);

#endif