#include "servo.h"

void servo_init(servo_t* servo) 
{
    ledcAttachPin(servo->pin, servo->channel);
    ledcSetup(servo->channel, FREQ, RESOLUTION);
}


uint16_t map_pulse(int16_t angle)
{
    uint16_t pulse = PULSEMIN + PULSERANGE*(angle + MAXANGLE)/ANGLERANGE;
    return pulse;
}


pwm_status_t setPWM(uint8_t channel, uint16_t duty) 
{    
    if(duty > ((1 << RESOLUTION) - 1))
    {
        return PWM_OUT_OF_RANGE; // Verifica se o valor do duty cycle está dentro do intervalo permitido
    }

    else
    {
        // Define o valor do PWM
        ledcWrite(channel, duty); 
        return PWM_OK;
    }
}


set_angle_status_t setServoAngle(uint8_t channel, int16_t angle) 
{
    if (angle > MAXANGLE) 
    {
        return ANGLE_OUT_OF_MAX_RANGE; // Verifica se o ângulo está dentro do intervalo permitido
    } 
    else if (angle < MINANGLE) 
    {
        return ANGLE_OUT_OF_MIN_RANGE; // Verifica se o ângulo está dentro do intervalo permitido
    }

    // Converte o ângulo (-90 a 90) para largura de pulso (1000us a 2000us)
    int pulseWidth = map_pulse(angle);
  
    // Converte de microssegundos para valor PWM com base no ciclo de 20ms e resolução
    uint16_t duty = (uint16_t)pulseWidth * ((1 << RESOLUTION) - 1) / CYCLELENGTH;

    if(setPWM(channel, duty) == PWM_OK)
    {
        return SET_ANGLE_SUCESS; // Se o PWM foi definido corretamente, retorna sucesso
    }
    else
    {
        return SET_ANGLE_ERROR; // PWM falhou ao ser configurado
    }
}


set_angle_status_t set_servo_angle(servo_t* servo, int16_t angle) 
{
    // Esta função abstrai o canal do servo, precisando apenas do servo e do ângulo
    return setServoAngle(servo->channel, angle);
}
  