// 最後編輯 2022-9-21 by ShinWei Chiou
// 初版

/*------------------------------------------------------------------------------------------------
 * 錯誤碼：
------------------------------------------------------------------------------------------------*/
unsigned int Error_Code = 0;


//------------------------------------------------------------------------------------------------
const unsigned int Linear_L1_zDistance = 8;
const unsigned int Linear_L2_zDistance = 5;
const unsigned int Linear_L3_zDistance = 3;
const unsigned int Linear_L4_zDistance = 10;

const unsigned int Rotation_T1_Angle = 10;
const unsigned int Rotation_T2_Angle = 20;
const unsigned int Rotation_T3_Angle = 30;
const unsigned int Rotation_T4_Angle = 40;
const unsigned int Rotation_T5_Angle = 50;
const unsigned int Rotation_T6_Angle = 60;
const unsigned int Rotation_T7_Angle = 70;
const unsigned int Rotation_T8_Angle = 80;

const unsigned int Rotation_B1_Angle = 90;
const unsigned int Rotation_B2_Angle = 100;
const unsigned int Rotation_B3_Angle = 110;
const unsigned int Rotation_B4_Angle = 120;
const unsigned int Rotation_B5_Angle = 207; // 130;  Grail, 20230207, should equals to D_Angle
const unsigned int Rotation_B6_Angle = 166; // 140;  Grail, 20230207, should equals to C_Angle

const unsigned int Rotation_A_Angle = 99;  // 840 steps = 99.47 degree;    // Grail, 20221202, Place A for 55 dc heater, was 840 ok
const unsigned int Rotation_B_Angle = 54;   // 460 steps = 54.47 degree;    // Grail, 20221202, Place B for 95 dc heater, was 460 ok
const unsigned int Rotation_C_Angle = 166;  // 1400 steps = 165.78 degree;    // Grail, 20221218, 
const unsigned int Rotation_D_Angle = 207;  // 1750 steps = 207.23 degree;    // Grail, 20221222, 


const unsigned int ServoMinPulseRate      = 1000;   // PWM
const unsigned int ServoMaxPulseRate      = 2400;   // PWM
const unsigned int Spinning_F_3KRPM       = 98;     // 3K 98
const unsigned int Spinning_F_6KRPM       = 102;    // 6K 102
const unsigned int Spinning_F_9KRPM       = 107;    // 9K 107
const unsigned int Spinning_F_12KRPM      = 117;    // 12K 117
const unsigned int Spinning_B_3KRPM       = 78;     // 3K 78
const unsigned int Spinning_B_6KRPM       = 74;     // 6K 74
const unsigned int Spinning_B_9KRPM       = 66;     // 9K 66
const unsigned int Spinning_B_12KRPM      = 52;     // 12K 52
const unsigned int Spinning_C2_Sec        = 10;     // 3min 180
const unsigned int Spinning_C3_Sec        = 10;     // 3min 180
const unsigned int Spinning_3KRPM_C11_ms  = 10000;  // 20Sec 20000
const unsigned int Spinning_3KRPM_C12_ms  = 10000;  // 10Sec 10000

const unsigned int Vacuum_V1_ms = 500;
const unsigned int Vacuum_V2_ms = 500;
const unsigned int Vacuum_V3_ms = 500;
const unsigned int Vacuum_V4_ms = 500;

const unsigned int Heater_H11_95C_Sec = 8;          // 2min = 400ms x 300
const unsigned int Heater_H12_95C_Sec = 8;          // 3Sec = 400ms x 8
const unsigned int Heater_H21_55C_Sec = 8;          // 5min = 400ms x 750
const unsigned int Heater_H22_55C_Sec = 8;          // 1min = 400ms x 150

const unsigned int Cooler_4C_Sec = 30;              // 60Sec = 300ms x 200

const unsigned int LED_Blue_ms   = 3000;
const unsigned int LED_Orange_ms = 3000;
const unsigned int LED_Green_ms  = 3000;
const unsigned int LED_Red_ms    = 3000;


//------------------------------------------------------------------------------------------------
int CURRENT_STAGE = 0;                 // Grail, 20230117, for start button
boolean DOE_TEST_PRINT_TEMP = true;    // Grail, 20221128
//------------------------------------------------------------------------------------------------
boolean System_Power_ON = LOW;

boolean System_Processing = LOW;
boolean System_Processing_Done = LOW;

boolean Drawer_Open_State = LOW;

boolean Drawer_Open_Error = LOW;
boolean Drawer_Close_Error = LOW;
boolean Linear_HighZ_Error = LOW;
boolean Clutch_Engage_Error = LOW;
boolean Rotation_Angle_Error = LOW;
boolean Rotation_TX_Angle_Align_Error = LOW;

boolean LedState;
unsigned int Button_LedState = 0;

boolean Button_OnOff_Press;
boolean Button_OpenClose_Press;
boolean Button_StartStop_Press;

unsigned int Linear_Now_HighZ = 0;        // 升降即時數據
unsigned int Rotation_Now_Angle = 0;      // 轉盤即時數據
unsigned int RPM_Intereupt_Counter = 0;   // 轉速即時數據


//------------------------------------------------------------------------------------------------
#define HET1    3
#define HET2    5
#define HET3    7
#define HET4    9

#define TEC     2
#define FAN     4

#define PUMP    6

#define BLDCP   8   // MOSFET Power Input
#define BLDCS   10  // PWM
#define BLDCD   11  // Directional

#define ENC0    20
#define ENC1    21

#define LSW1    A1  // Drawer Open
#define LSW2    A3  // Drawer Close
#define LSW3    A5  // Linear L0
#define LSW4    A7  // Rotation T0
#define LSW5    A9  // Clutch Engage

#define PB1     A11
#define PB2     A13
#define PB3     A15

#define LED1R   15
#define LED1B   14
#define LED2R   17
#define LED2B   16
#define LED3R   19
#define LED3B   18

#define VAL1    32
#define VAL2    34
#define VAL3    36
#define VAL4    38


//------------------------------------------------------------------------------------------------
#include <SPI.h>

#include <ILI9341_due_config.h>
#include <ILI9341_due.h>
#include "fonts/Arial_bold_14.h"

#define TFT_MISO  50
#define TFT_MOSI  51
#define TFT_CLK   52
#define TFT_RST   48
#define TFT_DC    49
#define TFT_CS    53
#define TFT_LED   12

char textBuff[20];

ILI9341_due tft = ILI9341_due(TFT_CS, TFT_DC, TFT_RST);


//------------------------------------------------------------------------------------------------
#include <SmoothThermistor.h>

/*
            AREF        Analog Pin
             |              |
      3.3V |-+---/\/\/\-----+-----/\/\/\-----| GND
                   ^                ^
           100K thermistor      10K resistor

  SmoothThermistor smoothThermistor(A0,              // the analog pin to read from
                                   ADC_SIZE_10_BIT, // the ADC size
                                   10000,           // the nominal resistance
                                   10000,           // the series resistance
                                   3950,            // the beta coefficient of the thermistor
                                   25,              // the temperature for nominal resistance
                                   10);             // the number of samples to take for each measurement
               ADC_SIZE_8_BIT
               ADC_SIZE_10_BIT
               ADC_SIZE_12_BIT
               ADC_SIZE_16_BIT
*/

#define NTC1    A0    // HET1
#define NTC2    A2    // HET2
#define NTC3    A4    // HET3
#define NTC4    A6    // HET4
#define NTC5    A8    // TEC
#define NTC6    A10   // Fan
#define NTC7    A12   // Room

// Grail, 20221129, need to add another NTC100K
#define NTC8    A14   // Cartridge

#define THERMISTOR_NOMINAL    98000   // NTC 100K ( 降低設定值 可調降溫度讀取數值 )
#define TEMP_SERIESRESISTOR   9900    // 10K the value of the 'other' resistor
#define TEMPERATURE_NOMINAL   25      // Temp. for nominal resistance (almost always 25 C)
#define TEMP_NUMSAMPLES       10      // how many samples to take and average, more takes longer
#define TEMP_BCOEFFICIENT     3950    // The beta coefficient of the thermistor (usually 3000-4000)

// create a SmoothThermistor instance, reading from analog pin
SmoothThermistor NTC_HET1_Thermistor(NTC1, ADC_SIZE_10_BIT, THERMISTOR_NOMINAL, TEMP_SERIESRESISTOR, TEMP_BCOEFFICIENT, TEMPERATURE_NOMINAL, TEMP_NUMSAMPLES);
SmoothThermistor NTC_HET2_Thermistor(NTC2, ADC_SIZE_10_BIT, THERMISTOR_NOMINAL, TEMP_SERIESRESISTOR, TEMP_BCOEFFICIENT, TEMPERATURE_NOMINAL, TEMP_NUMSAMPLES);
SmoothThermistor NTC_HET3_Thermistor(NTC3, ADC_SIZE_10_BIT, THERMISTOR_NOMINAL, TEMP_SERIESRESISTOR, TEMP_BCOEFFICIENT, TEMPERATURE_NOMINAL, TEMP_NUMSAMPLES);
SmoothThermistor NTC_HET4_Thermistor(NTC4, ADC_SIZE_10_BIT, THERMISTOR_NOMINAL, TEMP_SERIESRESISTOR, TEMP_BCOEFFICIENT, TEMPERATURE_NOMINAL, TEMP_NUMSAMPLES);
SmoothThermistor NTC_TEC_Thermistor(NTC5, ADC_SIZE_10_BIT, THERMISTOR_NOMINAL, TEMP_SERIESRESISTOR, TEMP_BCOEFFICIENT, TEMPERATURE_NOMINAL, TEMP_NUMSAMPLES);
SmoothThermistor NTC_FAN_Thermistor(NTC6, ADC_SIZE_10_BIT, THERMISTOR_NOMINAL, TEMP_SERIESRESISTOR, TEMP_BCOEFFICIENT, TEMPERATURE_NOMINAL, TEMP_NUMSAMPLES);
SmoothThermistor NTC_ROOM_Thermistor(NTC7, ADC_SIZE_10_BIT, THERMISTOR_NOMINAL, TEMP_SERIESRESISTOR, TEMP_BCOEFFICIENT, TEMPERATURE_NOMINAL, TEMP_NUMSAMPLES);
// Grail, 20221129, need to add another NTC100K
SmoothThermistor NTC_CART_Thermistor(NTC8, ADC_SIZE_10_BIT, THERMISTOR_NOMINAL, TEMP_SERIESRESISTOR, TEMP_BCOEFFICIENT, TEMPERATURE_NOMINAL, TEMP_NUMSAMPLES);



float NTC_TEC_Steinhart;
float NTC_FAN_Steinhart;
float NTC_ROOM_Steinhart;
float NTC_HET_Steinhart1;
float NTC_HET_Steinhart2;
float NTC_HET_Steinhart3;
float NTC_HET_Steinhart4;
// Grail, 20221129, need to add another NTC100K
float NTC_CART_Steinhart1;


//------------------------------------------------------------------------------------------------
#include <PID_v2.h>

float HET_SetPoint1 = 55;   // 55 預計數值目標
float HET_SetPoint2 = 75;   // 95 預計數值目標
float HET_Kp = 9.1;         // 12 數值是否能達到目標值
float HET_Ki = 0.3;         // 0.05 誤差積累
float HET_Kd = 1.8;         // 35 誤差變化率

float TEC_SetPoint = -4;     // -4 預計數值目標,                     /* Grail, 20221122 */  BT use value = 1
float TEC_Kp = 200;         // 200 數值是否能達到目標值
float TEC_Ki = 10;          // 10 誤差積累
float TEC_Kd = 5;           // 5 誤差變化率

PID_v2 TEC_PID(TEC_Kp, TEC_Ki, TEC_Kd, REVERSE);  // 致冷器
PID_v2 HET_PID1(HET_Kp, HET_Ki, HET_Kd, DIRECT);  // 加熱器
PID_v2 HET_PID2(HET_Kp, HET_Ki, HET_Kd, DIRECT);  // 加熱器
PID_v2 HET_PID3(HET_Kp, HET_Ki, HET_Kd, DIRECT);  // 加熱器
PID_v2 HET_PID4(HET_Kp, HET_Ki, HET_Kd, DIRECT);  // 加熱器


//------------------------------------------------------------------------------------------------
#include <CheapStepper.h>

boolean moveClockwise = HIGH;
boolean moveanticlockwise = LOW;

#define STM11   25
#define STM12   27
#define STM13   29
#define STM14   31
//CheapStepper StepperMotor_Linear (STM11, STM12, STM13, STM14);

#define STM21   24
#define STM22   26
#define STM23   28
#define STM24   30
CheapStepper StepperMotor_Rotation (STM21, STM22, STM23, STM24);

#define STM31   33
#define STM32   35
#define STM33   37
#define STM34   39
CheapStepper StepperMotor_Drawer (STM31, STM32, STM33, STM34);

#define STM41   41
#define STM42   43
#define STM43   45
#define STM44   47
CheapStepper StepperMotor_Clutch (STM41, STM42, STM43, STM44);

#define STM51   40
#define STM52   42
#define STM53   44
#define STM54   46
CheapStepper StepperMotor_Positioning (STM51, STM52, STM53, STM54);

//------------------------------------------------------------------------------------------------
//#include <AccelStepper.h>    /* Grail, 20221228, add accel stepper, not use anymore */
//#define FULLSTEP 4
//#define HALFSTEP 8
//AccelStepper StepperMotor_Linear(FULLSTEP, STM11, STM12, STM13, STM14);

//#include <Unistep2.h>        /* not use unistep2 anymore */

#include <Stepper.h>           /* Grail, 20230113, use Stepper lib instead of cheapStepper */
#define stepsPerRevolution 2048
#define stepsPerMM 1024        // Grail, 20230207, steps for vertical motion
#define stepsPer360Deg 3040    // Grail, 20230207, steps for rotation
Stepper StepperMotor_Linear(stepsPerRevolution, STM11, STM13, STM12, STM14);

//------------------------------------------------------------------------------------------------
#include <Adafruit_NeoPixel.h>

#define RGB         13      // Which pin on the Arduino is connected to the NeoPixels?
#define NUMPIXELS   2       // How many NeoPixels are attached ?
#define BRIGHTNESS  250     // 0~255

Adafruit_NeoPixel Pixels = Adafruit_NeoPixel(NUMPIXELS, RGB, NEO_GRB + NEO_KHZ800);
