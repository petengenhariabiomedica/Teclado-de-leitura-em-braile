#include <Arduino.h>
#include <consts.h>
#include "servo.h"
#include "braille_letters.h"
#include <ESP32Servo.h>

#define ANGLE_ON 0
#define ANGLE_OFF 90

// servo_t servo0 = { .channel = SERVO_CHANNEL_0, .pin = SERVO_PIN_0 }; // Pino 32
// servo_t servo1 = { .channel = SERVO_CHANNEL_1, .pin = SERVO_PIN_1 }; // Pino 33
// servo_t servo2 = { .channel = SERVO_CHANNEL_2, .pin = SERVO_PIN_2 }; // Pino 25
// servo_t servo3 = { .channel = SERVO_CHANNEL_3, .pin = SERVO_PIN_3 }; // Pino 26
// servo_t servo4 = { .channel = SERVO_CHANNEL_4, .pin = SERVO_PIN_4 }; // Pino 27
// servo_t servo5 = { .channel = SERVO_CHANNEL_5, .pin = SERVO_PIN_5 }; // Pino 14


// servo_t* servos[] = { &servo0, &servo1, &servo2, &servo3, &servo4, &servo5 };

extern uint8_t* braille_map[]; 

// Instâncias dos objetos Servo para cada servo
Servo servo0;
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

// Array para facilitar o acesso aos servos
Servo* servos[6] = {&servo0, &servo1, &servo2, &servo3, &servo4, &servo5};
// Array com as informações de pinos dos servos
servo_pin_t servoPins[6] = {SERVO_PIN_0, SERVO_PIN_1, SERVO_PIN_2, SERVO_PIN_3, SERVO_PIN_4, SERVO_PIN_5};


void setup() 
{
  Serial.begin(115200); 
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);


  for (int num_servo = 0; num_servo < 6; num_servo++) 
  {
    // servo_init(servos[num_servo]);                                  // Inicializa todos os servos
    // int set_angle_result = set_servo_angle(servos[num_servo], 0);   // Coloca todos os servos na posição 0 graus                               
    // if(set_angle_result != SET_ANGLE_SUCESS)                        
    // {} 
    // else 
    // {}
    servos[num_servo]->attach(servoPins[num_servo]);
  }
}

void loop() 
{
  if (Serial.available()) 
  {
    char incoming = Serial.read();

      if (check_letter(incoming) == IS_NOT_A_LETTER)
      {
        for (int num_servo = 0; num_servo < 6; num_servo++) 
          // set_servo_angle(servos[num_servo], ANGLE_OFF);
          servos[num_servo]->write(ANGLE_OFF);
      }
      else 
      {
        apply_braille_to_servos(incoming);
        Serial.println("OK");
      }
    }

    delay(1500); 
}




void apply_braille_to_servos(char c) 
{
  uint8_t* pattern = get_braille_pattern(c);

  if (pattern == nullptr) 
  {
    for (int num_servo = 0; num_servo < 6; num_servo++) 
    {
      // set_servo_angle(servos[num_servo], ANGLE_OFF);
      servos[num_servo]->write(ANGLE_OFF);
    }
  }

  else
  {
    servos[0]->write(ANGLE_OFF);
    servos[1]->write(ANGLE_OFF);
    servos[2]->write(ANGLE_OFF);
    servos[3]->write(ANGLE_OFF);
    servos[4]->write(ANGLE_OFF);
    servos[5]->write(ANGLE_OFF);
    delay(500);
    for (int num_servo = 0; num_servo < 6; num_servo++) 
    {
      int16_t angle = pattern[num_servo] ? ANGLE_ON : ANGLE_OFF;
      servos[num_servo]->write(angle);
      // int set_angle_result = set_servo_angle(servos[num_servo], angle);
      // if(set_angle_result != SET_ANGLE_SUCESS) 
      // {}
    }
  }
}


