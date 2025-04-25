#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include "consts.h"
#include <Arduino.h>

typedef enum servo_channel_e
{
    SERVO_CHANNEL_0 = 0,
    SERVO_CHANNEL_1 = 1,
    SERVO_CHANNEL_2 = 2,
    SERVO_CHANNEL_3 = 3,
    SERVO_CHANNEL_4 = 4,
    SERVO_CHANNEL_5 = 5,
} servo_channel_t;

typedef enum servo_pin_e
{
    SERVO_PIN_0 = 15,
    SERVO_PIN_1 = 2,
    SERVO_PIN_2 = 4,
    SERVO_PIN_3 = 16,
    SERVO_PIN_4 = 17,
    SERVO_PIN_5 = 5,
} servo_pin_t;

typedef struct servo_e
{
    servo_channel_t channel; // Canal do PWM
    servo_pin_t pin; // Pino do servo
} servo_t;

typedef enum set_angle_status_e
{
    SET_ANGLE_SUCESS = 0,
    SET_ANGLE_ERROR = 1,
    ANGLE_OUT_OF_MIN_RANGE = 2,
    ANGLE_OUT_OF_MAX_RANGE = 3,
} set_angle_status_t;

typedef enum pwm_status_e
{
    PWM_OK = 0,
    PWM_OUT_OF_RANGE,
} pwm_status_t;

uint16_t map_pulse(int16_t angle);
pwm_status_t setPWM(uint8_t channel, uint16_t duty);
set_angle_status_t setServoAngle(uint8_t channel, int16_t angle);
set_angle_status_t set_servo_angle(servo_t* servo, int16_t angle);
void servo_init(servo_t* servo);


#ifdef __cplusplus
}
#endif