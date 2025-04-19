#include <Arduino.h>
#include <consts.h>
#include "servo.h"
#include "braille_letters.h"

#define ANGLE_ON 90
#define ANGLE_OFF 0

servo_t servo0 = { .channel = SERVO_CHANNEL_0, .pin = SERVO_PIN_0 };
servo_t servo1 = { .channel = SERVO_CHANNEL_1, .pin = SERVO_PIN_1 };
servo_t servo2 = { .channel = SERVO_CHANNEL_2, .pin = SERVO_PIN_2 };
servo_t servo3 = { .channel = SERVO_CHANNEL_3, .pin = SERVO_PIN_3 };
servo_t servo4 = { .channel = SERVO_CHANNEL_4, .pin = SERVO_PIN_4 };
servo_t servo5 = { .channel = SERVO_CHANNEL_5, .pin = SERVO_PIN_5 };

extern uint8_t* braille_map[]; 

servo_t* servos[] = { &servo0, &servo1, &servo2, &servo3, &servo4, &servo5 };

void setup() 
{
  Serial.begin(115200);

  for (int num_servo = 0; num_servo < 6; num_servo++) 
  {
    servo_init(servos[num_servo]);                                         // Inicializa todos os servos
    if(set_servo_angle(servos[num_servo], 0) != SET_ANGLE_SUCESS)   // Coloca todos os servos na posição 0 graus
    {
      //Serial.print("Erro ao definir o ângulo do servo ");
      //Serial.print(num_servo);
      //Serial.println(" na posição 0 graus.");
    } 
    else 
    {
      //Serial.print("Servo ");
      //Serial.print(num_servo);
      //Serial.println(" inicializado e definido para 0 graus.");
    } 
  }
}

void loop() 
{
  if (Serial.available()) 
  {
    char c = Serial.read();
    if (check_letter(c) == IS_NOT_A_LETTER) 
    {
      for (int num_servo = 0; num_servo < 6; num_servo++) 
      {
        set_servo_angle(servos[num_servo], ANGLE_OFF);
      }
      return;
    }
    else
    { 
    apply_braille_to_servos(c);
    Serial.println("OK");
    }
    delay(500); 
  }
}


void apply_braille_to_servos(char c) 
{
  uint8_t* pattern = get_braille_pattern(c);

  if (pattern == nullptr) 
  {
    //Serial.println("Letra inválida!");
    return;
  }

  for (int num_servo = 0; num_servo < 6; num_servo++) 
  {
    int16_t angle = pattern[num_servo] ? ANGLE_ON : ANGLE_OFF;
    if(set_servo_angle(servos[num_servo], angle) != SET_ANGLE_SUCESS) 
    {
      //Serial.print("Erro ao definir ângulo do servo ");
      //Serial.println(num_servo);
    }
  }
}


