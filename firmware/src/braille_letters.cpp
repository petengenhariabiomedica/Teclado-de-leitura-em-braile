#include <Arduino.h>
#include "servo.h"
#include "braille_letters.h"

uint8_t a_braille[6] = {1, 0, 0, 0, 0, 0}; 
uint8_t b_braille[6] = {1, 0, 1, 0, 0, 0};
uint8_t c_braille[6] = {1, 1, 0, 0, 0, 0};
uint8_t d_braille[6] = {1, 1, 0, 1, 0, 0};
uint8_t e_braille[6] = {1, 0, 0, 1, 0, 0};
uint8_t f_braille[6] = {1, 1, 1, 0, 0, 0};
uint8_t g_braille[6] = {1, 1, 1, 1, 0, 0};
uint8_t h_braille[6] = {1, 0, 1, 1, 0, 0};
uint8_t i_braille[6] = {0, 1, 1, 0, 0, 0};
uint8_t j_braille[6] = {0, 1, 1, 1, 0, 0};
uint8_t k_braille[6] = {1, 0, 0, 0, 1, 0};
uint8_t l_braille[6] = {1, 0, 1, 0, 1, 0};
uint8_t m_braille[6] = {1, 1, 0, 0, 1, 0};
uint8_t n_braille[6] = {1, 1, 0, 1, 1, 0};
uint8_t o_braille[6] = {1, 0, 0, 1, 1, 0};
uint8_t p_braille[6] = {1, 1, 1, 0, 1, 0};
uint8_t q_braille[6] = {1, 1, 1, 1, 1, 0};
uint8_t r_braille[6] = {1, 0, 1, 1, 1, 0};
uint8_t s_braille[6] = {0, 1, 1, 0, 1, 0};
uint8_t t_braille[6] = {0, 1, 1, 1, 1, 0};
uint8_t u_braille[6] = {1, 0, 0, 0, 1, 1};
uint8_t v_braille[6] = {1, 0, 1, 0, 1, 1};
uint8_t w_braille[6] = {0, 1, 1, 1, 0, 1};
uint8_t x_braille[6] = {1, 1, 0, 0, 1, 1};
uint8_t y_braille[6] = {1, 1, 0, 1, 1, 1};
uint8_t z_braille[6] = {1, 0, 0, 1, 1, 1};

uint8_t* braille_map[] = 
{
    a_braille, b_braille, c_braille, d_braille, e_braille,
    f_braille, g_braille, h_braille, i_braille, j_braille,
    k_braille, l_braille, m_braille, n_braille, o_braille,
    p_braille, q_braille, r_braille, s_braille, t_braille,
    u_braille, v_braille, w_braille, x_braille, y_braille, z_braille
};



uint8_t* get_braille_pattern(char c) 
{
    if (c >= 'A' && c <= 'Z') c += 32; // Converte para minúscula
    return braille_map[c - 'a'];
}

letter_status_t check_letter(char c) 
{
    if (c >= 'A' && c <= 'Z') return LETTER_STATUS_OK;
    if (c >= 'a' && c <= 'z') return LETTER_STATUS_OK;
    return IS_NOT_A_LETTER;
}