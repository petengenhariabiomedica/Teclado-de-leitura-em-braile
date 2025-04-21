#include <Arduino.h>
#include <stddef.h>
#include "braille_letters.h"

/*---------------------------------
  Braille representation of letters

                1 2 
                3 4 
                5 6 

---------------------------------*/

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

/* 
Caracteres especiais, apenas alguns são utilizados
na linguagem brasileira de braile. Todos podem ser
encontrados na tabela unicode. Os únicos que iremos
utilizar são: À Á Â Ç È É Ê Ì Í Ò Ó Ô Ù Ú
*/ 
static const uint8_t braille_special_patterns[64][6] = 
{
    {1, 1, 1, 0, 0, 1}, // À Posição 127
    {1, 0, 1, 1, 1, 1}, // Á Posição 128
    {1, 0, 0, 0, 0, 1}, // Â Posição 129
    {0, 0, 0, 0, 0, 0}, // Ã Posição 130
    {0, 0, 0, 0, 0, 0}, // Ä Posição 131
    {0, 0, 0, 0, 0, 0}, // Å Posição 132
    {0, 0, 0, 0, 0, 0}, // Æ Posição 133
    {1, 1, 1, 0, 1, 1}, // Ç Posição 134
    {0, 1, 1, 0, 1, 1}, // È Posição 135
    {1, 1, 1, 1, 1, 1}, // É Posição 136
    {1, 0, 1, 0, 0, 1}, // Ê Posição 137
    {0, 0, 0, 0, 0, 0}, // Ë Posição 138
    {1, 1, 0, 0, 0, 1}, // Ì Posição 139
    {0, 1, 0, 0, 1, 0}, // Í Posiçaõ 140
    {0, 0, 0, 0, 0, 0}, // Î Posição 141
    {0, 0, 0, 0, 0, 0}, // Ï Posição 142
    {0, 0, 0, 0, 0, 0}, // Ð Posição 143
    {0, 0, 0, 0, 0, 0}, // Ñ Posição 144
    {0, 1, 1, 1, 0, 1}, // Ò Posição 145
    {0, 1, 0, 0, 1, 1}, // Ó Posição 146
    {1, 1, 0, 1, 0, 1}, // Ô Posição 147
    {0, 0, 0, 0, 0, 0}, // Õ Posição 148
    {0, 0, 0, 0, 0, 0}, // Ö Posição 149
    {0, 0, 0, 0, 0, 0}, // × Posição 150
    {0, 0, 0, 0, 0, 0}, // Ø Posição 151
    {1, 0, 0, 1, 0, 1}, // Ù Posição 152
    {0, 1, 1, 1, 1, 1}, // Ú Posição 153
    {0, 0, 0, 0, 0, 0}, // Û Posição 154
    {0, 0, 0, 0, 0, 0}, // Ü Posição 155
    {0, 0, 0, 0, 0, 0}, // Ý Posição 156
    {0, 0, 0, 0, 0, 0}, // Þ Posição 157
    {0, 0, 0, 0, 0, 0}, // ß Posição 158
    {1, 1, 1, 0, 0, 1}, // à Posição 159
    {1, 0, 1, 1, 1, 1}, // á Posição 160
    {1, 0, 0, 0, 0, 1}, // â Posição 161
    {0, 0, 0, 0, 0, 0}, // ã Posição 162
    {0, 0, 0, 0, 0, 0}, // ä Posição 163
    {0, 0, 0, 0, 0, 0}, // å Posição 164
    {0, 0, 0, 0, 0, 0}, // æ Posição 165
    {1, 1, 1, 0, 1, 1}, // ç Posição 166
    {0, 1, 1, 0, 1, 1}, // è Posição 167
    {1, 1, 1, 1, 1, 1}, // é Posição 168
    {1, 0, 1, 0, 0, 1}, // ê Posição 169
    {0, 0, 0, 0, 0, 0}, // ë Posição 170 
    {1, 1, 0, 0, 0, 1}, // ì Posição 171
    {0, 1, 0, 0, 1, 0}, // í Posiçaõ 172
    {0, 0, 0, 0, 0, 0}, // î Posição 173
    {0, 0, 0, 0, 0, 0}, // ï Posição 174
    {0, 0, 0, 0, 0, 0}, // ð Posição 175
    {0, 0, 0, 0, 0, 0}, // ñ Posição 176
    {0, 1, 1, 1, 0, 1}, // ò Posição 177
    {0, 1, 0, 0, 1, 1}, // ó Posição 178
    {1, 1, 0, 1, 0, 1}, // ô Posição 179
    {0, 0, 0, 0, 0, 0}, // õ Posição 180
    {0, 0, 0, 0, 0, 0}, // ö Posição 181
    {0, 0, 0, 0, 0, 0}, // ÷ Posição 182
    {0, 0, 0, 0, 0, 0}, // ø Posição 183
    {1, 0, 0, 1, 0, 1}, // ù Posição 184
    {0, 1, 1, 1, 1, 1}, // ú Posição 185
    {0, 0, 0, 0, 0, 0}, // û Posição 186
    {0, 0, 0, 0, 0, 0}, // ü Posição 187
    {0, 0, 0, 0, 0, 0}, // ý Posição 188
    {0, 0, 0, 0, 0, 0}, // þ Posição 189
    {0, 0, 0, 0, 0, 0}, // ÿ Posição 190
};



uint8_t* get_braille_pattern(char c) 
{
    if (c >= 'A' && c <= 'Z') c += 32; // Converte para minúscula
    
    if (c >= 'a' && c <= 'z') {
        return (uint8_t*)braille_patterns[c - 'a'];
    }
    else if(check_letter(c) == LETTER_STATUS_OK) 
    {
       return (uint8_t*)braille_special_patterns[c - 'A' - 127]; // 'A' = 65, subtrai 127 para pegar os caracteres especiais
    }
    else if (check_letter(c) == IS_A_SPACE) 
    {
        return NULL;
    }
    return NULL;
}


letter_status_t check_letter(char c) 
{
    if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z')) {
        return LETTER_STATUS_OK;
    }
    else if(c >= 0xC0 && c <= 0xFF) // Verifica se é um caractere especial
    {
        return LETTER_STATUS_OK;
    }
    else if (c == ' ') 
    {
        return IS_A_SPACE;
    }
    else if (c == '\n')
    {
        return IS_A_SPACE;
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
