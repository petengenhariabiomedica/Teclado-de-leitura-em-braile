#include <Arduino.h>
#include <stddef.h>
#include "braille_letters.h"


// Matriz compacta de padrões Braille (6 bits por letra)
static const uint8_t braille_patterns[26][6] = 
{
    {1, 0, 0, 0, 0, 0}, // A
    {1, 0, 1, 0, 0, 0}, // B
    {1, 1, 0, 0, 0, 0}, // C
    {1, 1, 0, 1, 0, 0}, // D
    {1, 0, 0, 1, 0, 0}, // E
    {1, 1, 1, 0, 0, 0}, // F
    {1, 1, 1, 1, 0, 0}, // G
    {1, 0, 1, 1, 0, 0}, // H
    {0, 1, 1, 0, 0, 0}, // I
    {0, 1, 1, 1, 0, 0}, // J
    {1, 0, 0, 0, 1, 0}, // K
    {1, 0, 1, 0, 1, 0}, // L
    {1, 1, 0, 0, 1, 0}, // M
    {1, 1, 0, 1, 1, 0}, // N
    {1, 0, 0, 1, 1, 0}, // O
    {1, 1, 1, 0, 1, 0}, // P
    {1, 1, 1, 1 ,1 ,0}, // Q
    {1 ,0 ,1 ,1 ,1 ,0}, // R
    {0 ,1 ,1 ,0 ,1 ,0}, // S
    {0 ,1 ,1 ,1 ,1 ,0}, // T
    {1, 0, 0, 0, 1, 1}, // U
    {1, 0, 1, 0, 1, 1}, // V
    {0, 1, 1, 1, 0, 1}, // W
    {1, 1, 0, 0, 1, 1}, // X
    {1, 1, 0, 1, 1, 1}, // Y
    {1, 0, 0, 1, 1, 1}  // Z
};


uint8_t* get_braille_pattern(char c) 
{
    if (c >= 'A' && c <= 'Z') c += 32; // Converte para minúscula
    
    if (c >= 'a' && c <= 'z') {
        return (uint8_t*)braille_patterns[c - 'a'];
    }
    return NULL;
}


letter_status_t check_letter(char c) 
{
    if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z')) {
        return LETTER_STATUS_OK;
    }
    return IS_NOT_A_LETTER;
}

__attribute__((weak)) void apply_braille_to_servos(char* c) 
{
    if (c != NULL) 
    {
        return; // Função vazia, não faz nada, apenas para evitar erro de compilação
    }
}