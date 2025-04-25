#pragma once

#ifndef CONSTS_H
#define CONSTS_H

#define PULSEMIN 1000                       // 1ms = -90°
#define PULSEMAX 2000                       // 2ms = 90°
#define PULSERANGE (PULSEMAX - PULSEMIN)    // 1000us = 1ms
#define CYCLELENGTH 20000                   // 20000us = 20ms / 50Hz
#define FREQ (1/CYCLELENGTH)*100000         // 50Hz
#define MINANGLE -90                        // DEGREES
#define MAXANGLE 90                         // DEGREES
#define ANGLERANGE (MAXANGLE - MINANGLE)    // 180°
#define RESOLUTION 16                       // BITS
#define MAXDUTY ((1 << RESOLUTION) - 1)     // 65535


/********************************************************************************************************************************  
 * 
 * 
 * 
INFORMAÇÕES EXTRAÍDAS DO DATASHEET DO SERVOMOTOR MG90S : 
https://www.electronicoscaldas.com/datasheet/MG90S_Tower-Pro.pdf?srsltid=AfmBOorbeO-KZeVL2aaSOqxCvHmfIUwKgwjKMQDwnSNF8DTOBoHBYEaq
 * 
 * 
 * 
********************************************************************************************************************************/

#endif