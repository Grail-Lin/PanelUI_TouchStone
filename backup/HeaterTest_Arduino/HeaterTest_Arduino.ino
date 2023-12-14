// 最後編輯 2023-12-12 by Grail
// 初版

/*
  Board: MEGA 2560 PRO mini 5V / 16Mhz
  UART Serial : 9600
*/

// Version
String FW_Version = "Heater Test v1.0   2023.12.12";

#include <MsTimer2.h>
#include "Configuration.h"

#include <Servo.h>
Servo BLDC_PWM_ESC;


//------------------------------------------------------------------------------------------------
void setup() {
  // 設定 GPIO
  pinMode(TFT_LED, OUTPUT);
  digitalWrite(TFT_LED, LOW);

  pinMode(LED1R, OUTPUT);
  pinMode(LED1B, OUTPUT);
  pinMode(LED2R, OUTPUT);
  pinMode(LED2B, OUTPUT);
  pinMode(LED3R, OUTPUT);
  pinMode(LED3B, OUTPUT);

  pinMode(PB1, INPUT_PULLUP);
  pinMode(PB2, INPUT_PULLUP);
  pinMode(PB3, INPUT_PULLUP);

  pinMode(LSW1, INPUT_PULLUP);
  pinMode(LSW2, INPUT_PULLUP);
  pinMode(LSW3, INPUT_PULLUP);
  pinMode(LSW4, INPUT_PULLUP);
  pinMode(LSW5, INPUT_PULLUP);

  pinMode(HET1, OUTPUT);
  pinMode(HET2, OUTPUT);
  pinMode(HET3, OUTPUT);
  pinMode(HET4, OUTPUT);

  pinMode(TEC, OUTPUT);
  pinMode(FAN, OUTPUT);

  pinMode(PUMP, OUTPUT);

  pinMode(RGB, OUTPUT);

  pinMode(BLDCP, OUTPUT);
  digitalWrite(BLDCP, LOW);
  pinMode(BLDCD, OUTPUT);
  digitalWrite(BLDCD, LOW);
  pinMode(BLDCS, OUTPUT);
  BLDC_PWM_ESC.attach(BLDCS, ServoMinPulseRate, ServoMaxPulseRate);
  BLDC_PWM_ESC.write(90);

  pinMode(VAL1, OUTPUT);
  pinMode(VAL2, OUTPUT);
  pinMode(VAL3, OUTPUT);
  pinMode(VAL4, OUTPUT);

  pinMode(NTC1, INPUT);
  pinMode(NTC2, INPUT);
  pinMode(NTC3, INPUT);
  pinMode(NTC4, INPUT);
  pinMode(NTC5, INPUT);
  pinMode(NTC6, INPUT);
  pinMode(NTC7, INPUT);
  
  // Grail, 20221208, add NTC8 for cartridge sensors
  pinMode(NTC8, INPUT);


  pinMode(ENC0, INPUT_PULLUP);
  pinMode(ENC1, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENC0), Intereupt_RPM, RISING);  // LOW to HIGH
  //attachInterrupt(digitalPinToInterrupt(ENC0), Intereupt_RPM, FALLING);   // HIGH to LOW
  //attachInterrupt(digitalPinToInterrupt(ENC0), Intereupt_RPM, CHANGE);


  // 設定 RGB
  Pixels.setBrightness(BRIGHTNESS);
  Pixels.begin();  // INITIALIZE NeoPixel strip object
  Pixels.clear();  // Turn OFF all pixels ASAP
  Pixels.show();   // This sends the updated pixel color to the hardware.


  // 設定 SmoothThermistor AREF
  NTC_HET1_Thermistor.useAREF(true);
  NTC_HET2_Thermistor.useAREF(true);
  NTC_HET3_Thermistor.useAREF(true);
  NTC_HET4_Thermistor.useAREF(true);
  NTC_TEC_Thermistor.useAREF(true);
  NTC_FAN_Thermistor.useAREF(true);
  NTC_ROOM_Thermistor.useAREF(true);
  
  // Grail, 20221208, add for CART sensor
  NTC_CART_Thermistor.useAREF(true);


  // 設定 PID
  TEC_PID.Start(NTC_TEC_Steinhart, 0, TEC_SetPoint);     // input, current output, setpoint -4
  HET_PID1.Start(NTC_HET_Steinhart1, 0, HET_SetPoint1);  // input, current output, setpoint 55
  HET_PID2.Start(NTC_HET_Steinhart2, 0, HET_SetPoint2);  // input, current output, setpoint 95
  HET_PID3.Start(NTC_HET_Steinhart3, 0, HET_SetPoint1);  // input, current output, setpoint 55
  HET_PID4.Start(NTC_HET_Steinhart4, 0, HET_SetPoint2);  // input, current output, setpoint 95


  // 設定 StepMotor , using 12V power, Default is 12~16 rpm
  //StepperMotor_Linear.setMaxSpeed(500.0);
  //StepperMotor_Linear.setAcceleration(50.0);
  //StepperMotor_Linear.setRpm(16);
  //StepperMotor_Rotation.setMaxSpeed(1000.0);
  //StepperMotor_Rotation.setAcceleration(50.0);
  //StepperMotor_Rotation.setSpeed(200);
  StepperMotor_Linear.setSpeed(4);    // 5 cycle per minute
  StepperMotor_Rotation.setRpm(16);
  StepperMotor_Drawer.setRpm(16);
  StepperMotor_Clutch.setRpm(16);
  StepperMotor_Positioning.setRpm(16);


  // 設定 UART
  Serial.begin(9600);
  delay(500);
  Serial.println(FW_Version);


  // 設定 ILI9341 螢幕
  tft.begin();
  tft.setRotation(1);


  // 中斷 500ms
  MsTimer2::set(500, Intereupt_Sub);  // 0.5 秒 = 500ms
  MsTimer2::start();


  // 開機 Button LED 顯示
  ButtonLED_ACPower_Connected();
}


//------------------------------------------------------------------------------------------------
void Intereupt_RPM() {
  if (RPM_Intereupt_Counter >= 6100) {
    RPM_Intereupt_Counter = 0;
  } else {
    RPM_Intereupt_Counter++;
  }
}


//------------------------------------------------------------------------------------------------
void Intereupt_Sub() {
  //------------------------------------------------------
  // 按鍵 LED 閃爍
  if (Button_LedState == 1) {
    ButtonLED_Power_ON_OFF();
  } else if (Button_LedState == 2) {
    ButtonLED_Drawer_OpenClose();
  } else if (Button_LedState == 3) {
    ButtonLED_Processing();
  } else if (Button_LedState == 4) {
    ButtonLED_Error();
  }
}


//------------------------------------------------------------------------------------------------
void loop() {
  /*
    if (digitalRead(PB1) == 0)
    {
      delay(20);
      while (digitalRead(PB1) == 0);

      //BLDC_Spinning_Start();
      //BLDC_Spinning_6K();

      //Step_Initialization();
      //Rotation_TX_Angle_Align();
      //Clutch_None_Engage();
      //Step_11(); // BLDC
      Drawer_Open();
    }

    if (digitalRead(PB3) == 0)
    {
      delay(20);
      while (digitalRead(PB3) == 0);

      //BLDC_Spinning_Stop();
      Drawer_Close();
    }
  */

  // 按鍵偵測
  Button_Press();

  // ON/OFF 按鍵
  if (Button_OnOff_Press == HIGH) {
    Button_OnOff_Press = LOW;

    if (System_Processing_Done == LOW) {
      if (System_Power_ON == HIGH) {
        Step_Goodbye();
        ButtonLED_ACPower_Connected();
        System_Power_ON = LOW;
      } else {
        ButtonLED_Standby_Mode();
        System_Power_ON = HIGH;
        Step_Initialization();
      }
    }
  }

  // OPEN/CLOSE 按鍵
  if (Button_OpenClose_Press == HIGH) {
    Button_OpenClose_Press = LOW;

    if (System_Power_ON == HIGH && System_Processing == LOW && Error_Code == 0) {
      if (Drawer_Open_State == LOW) {
        Step_Drawer_Open();
      } else {
        Step_Drawer_Close();
      }
    }
  }

  // START 按鍵
  if (Button_StartStop_Press == HIGH) {
    Button_StartStop_Press = LOW;

    if (System_Power_ON == HIGH && System_Processing_Done == LOW && Error_Code == 0) {
      Step_Start();
    }
  }
}


//------------------------------------------------------------------------------------------------
void Step_Start() {
  // 若沒關門
  if (Drawer_Open_State == HIGH) {
    // Display Start
    digitalWrite(TFT_LED, LOW);

    tft.fillScreen(ILI9341_BLACK);
    tft.setFont(Arial_bold_14);

    tft.setTextScale(2);
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    tft.printAlignedOffseted("DRAWER CLOSE", gTextAlignMiddleCenter, 0, -90);
    tft.setTextScale(1);

    tft.printAt("1. Linear L4 Distance", 40, 60);
    tft.printAt("2. Drawer Close", 40, 80);

    digitalWrite(TFT_LED, HIGH);


    // Display Button LED
    Button_LedState = 2;


    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    //------------------------------------------------------
    Linear_HighZ(Linear_L4_zDistance);
    tft.printAt(" OK ", 250, 60);

    //------------------------------------------------------
    Drawer_Close();
    tft.printAt(" OK ", 250, 80);
  }


  // Display Button LED
  Button_LedState = 3;
  System_Processing = HIGH;


  //------------------------------------------------------//
  //                  Processing Start                    //
  //------------------------------------------------------//

  if (true) {
    Step_HEATERTEST();
    //Step_TEC(60000);
    //Linear_HighZ(0);    
    //Show_Paras();
    /*
    if (CURRENT_STAGE == 0) {
      CURRENT_STAGE = 1;
      Show_Stage();
      Linear_HighZ(100);
    } else if (CURRENT_STAGE == 1) {
      CURRENT_STAGE = 2;
      Show_Stage();
      Linear_HighZ(50);
    } else if (CURRENT_STAGE == 2) {
      CURRENT_STAGE = 3;
      Show_Stage();
      Linear_HighZ(49);
    } else if (CURRENT_STAGE == 3) {
      CURRENT_STAGE = 4;
      Show_Stage();
      Linear_HighZ(48);
    } else if (CURRENT_STAGE == 4) {
      CURRENT_STAGE = 5;
      Show_Stage();
      Linear_HighZ(0);
      CURRENT_STAGE = 0;
    }
    Show_Paras();
    */
  } else {
    Step_11();
    delay(1000);
    Step_12();  // BLDC
    delay(1000);
    Step_13();
    delay(1000);
    Step_14();
    delay(1000);
    Step_15();
    delay(1000);
    Step_16();
    delay(1000);
    Step_17();
    delay(1000);
    Step_18();
    delay(1000);
    Step_19();
    delay(1000);
    Step_20();
    delay(1000);

    Step_21();  // BLDC
    delay(1000);
    Step_22();
    delay(1000);
    Step_23();
    delay(1000);
    Step_24();
    delay(1000);
    Step_25();
    delay(1000);
    Step_26();
    delay(1000);
    Step_27();
    delay(1000);
    Step_28();
    delay(1000);
    Step_29();
    delay(1000);
    Step_30();
    delay(1000);

    Step_31();
    delay(1000);
    Step_32();
    delay(1000);
    Step_33();
    delay(1000);
    Step_34();
    delay(1000);
    Step_35();
    delay(1000);
    Step_36();
    delay(1000);
    Step_37();
    delay(1000);
    Step_38();  // BLDC
    delay(1000);
    Step_39();
    delay(1000);
    Step_40();
    delay(1000);

    Step_41();
    delay(1000);
    Step_42();
    delay(1000);
    Step_43();
    delay(1000);
    Step_44();  // BLDC
    delay(1000);
    Step_45();
    delay(1000);
    Step_46();
    delay(1000);
    Step_47();
    delay(1000);
    Step_48();
    delay(1000);
    Step_49();
    delay(1000);
    Step_50();
    delay(1000);

    Step_51();
    delay(1000);
    Step_52();
    delay(1000);
    Step_53();  // BLDC
    delay(1000);
    Step_54();
    delay(1000);
    Step_55();
    delay(1000);
    Step_56();
    delay(1000);
    Step_57();
    delay(1000);
    Step_58();
    delay(1000);
    Step_59();
    delay(1000);
    Step_60();
    delay(1000);

    Step_61();
    delay(1000);
    Step_62();
    delay(1000);
    Step_63();
    delay(1000);
    Step_64();
    delay(1000);
    Step_65();
    delay(1000);
    Step_66();
    delay(1000);
    Step_67();
    delay(1000);
    Step_68();
    delay(1000);
    Step_69();
    delay(1000);
    Step_70();
    delay(1000);

    Step_71();
    delay(1000);
    Step_72();
    delay(1000);
    Step_73();
    delay(1000);
    Step_74();
    delay(1000);
    Step_75();
  }

  // Display Button LED
  Button_LedState = 0;
  System_Processing = LOW;
  //System_Processing_Done = HIGH;  // Grail, 20230118, mark this one to modify the stage machine
  ButtonLED_Standby_Mode();
}


//------------------------------------------------------------------------------------------------
void Step_Drawer_Close() {
  // Display Start
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("DRAWER CLOSE", gTextAlignMiddleCenter, 0, -90);
  tft.setTextScale(1);

  tft.printAt("1. Linear L4 Distance", 40, 60);
  tft.printAt("2. Drawer Close", 40, 80);

  digitalWrite(TFT_LED, HIGH);


  // Display Button LED
  Button_LedState = 2;


  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  //------------------------------------------------------
  Linear_HighZ(Linear_L4_zDistance);
  tft.printAt(" OK ", 250, 60);


  // Rotation Check, TBD
  Rotation_Angle(0);


  //------------------------------------------------------
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  delay(2000);


  // Display Button LED
  Button_LedState = 0;
  ButtonLED_Standby_Mode();


  // Display End
  tft.setTextScale(3);
  tft.fillScreen(ILI9341_BLACK);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("PRESS START", gTextAlignMiddleCenter, 0, 0);
}


//------------------------------------------------------------------------------------------------
void Step_Drawer_Open() {
  // Display Start
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("DRAWER OPEN", gTextAlignMiddleCenter, 0, -90);
  tft.setTextScale(1);

  tft.printAt("1. Linear L4 Distance", 40, 60);
  tft.printAt("2. Rotation T0", 40, 80);
  tft.printAt("3. Optical Inspection TX", 40, 100);
  tft.printAt("4. Drawer Open", 40, 120);
  tft.printAt("5. Linear L0 Distance", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // Display Button LED
  Button_LedState = 2;


  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  //------------------------------------------------------
  Linear_HighZ(Linear_L4_zDistance);
  tft.printAt(" OK ", 250, 60);

  //------------------------------------------------------
  Rotation_Angle(0);
  tft.printAt(" OK ", 250, 80);

  //------------------------------------------------------
  Rotation_TX_Angle_Align();
  if (Rotation_TX_Angle_Align_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  //------------------------------------------------------
  Drawer_Open();
  if (Drawer_Open_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 120);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 120);
  }

  //------------------------------------------------------
  Linear_HighZ(0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  delay(2000);


  // Display Button LED
  Button_LedState = 0;
  ButtonLED_Standby_Mode();
  System_Processing_Done = LOW;


  // Display End
  tft.setTextScale(2);
  tft.fillScreen(ILI9341_BLACK);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("PLEASE INSERT", gTextAlignMiddleCenter, 0, -30);
  tft.printAlignedOffseted("A CARTRIDGE", gTextAlignMiddleCenter, 0, 0);

  tft.setTextScale(1);
  tft.setTextColor(ILI9341_YELLOW, ILI9341_BLACK);
  tft.printAlignedOffseted("PRESS CLOSE OR START", gTextAlignMiddleCenter, 0, 40);
}


//------------------------------------------------------------------------------------------------
void Step_Goodbye() {
  // Display Start
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("GOODBYE", gTextAlignMiddleCenter, 0, -90);
  tft.setTextScale(1);

  digitalWrite(TFT_LED, HIGH);


  // Display Button LED
  Button_LedState = 1;


  //------------------------------------------------------
  tft.printAt("1. Linear Check", 40, 60);

  // Linear Check
  Linear_Now_HighZ = -1;
  Linear_HighZ(0);

  // Linear_L4_zDistance
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L4_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }


  //------------------------------------------------------
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);

  tft.printAt("2. Drawer Check", 40, 80);

  // Drawer Check
  if (digitalRead(LSW2) == 1)  // is open ?
  {
    Drawer_Close();
  }

  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }


  //------------------------------------------------------
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAt("3. Rotation Check", 40, 100);

  // Rotation Check
  Rotation_Angle(0);

  if (Rotation_Angle_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }


  //------------------------------------------------------
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAt("4. Optical Inspection Check", 40, 120);

  // Optical Inspection Check
  Rotation_TX_Angle_Align();

  if (Rotation_TX_Angle_Align_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 120);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 120);
  }


  //------------------------------------------------------
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAt("5. Thermometer Check", 40, 140);

  // Thermometer Check
  NTC_HET_Steinhart1 = NTC_HET1_Thermistor.temperature();
  NTC_HET_Steinhart2 = NTC_HET2_Thermistor.temperature();
  NTC_HET_Steinhart3 = NTC_HET3_Thermistor.temperature();
  NTC_HET_Steinhart4 = NTC_HET4_Thermistor.temperature();
  NTC_TEC_Steinhart = NTC_TEC_Thermistor.temperature();
  NTC_FAN_Steinhart = NTC_FAN_Thermistor.temperature();
  NTC_ROOM_Steinhart = NTC_ROOM_Thermistor.temperature();

  // Grail, 20221208, CART sensor
  NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
  

  tft.printAt("HET1   HET2   HET3   HET4", 60, 160);
  tft.printAt("TEC    FAN    ROOM   CART", 60, 195);

  tft.setTextColor(ILI9341_YELLOW, ILI9341_BLACK);

  dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 60, 175);
  dtostrf(NTC_HET_Steinhart2, 3, 1, textBuff);
  tft.printAt(textBuff, 113, 175);
  dtostrf(NTC_HET_Steinhart3, 3, 1, textBuff);
  tft.printAt(textBuff, 170, 175);
  dtostrf(NTC_HET_Steinhart4, 3, 1, textBuff);
  tft.printAt(textBuff, 225, 175);

  dtostrf(NTC_TEC_Steinhart, 3, 1, textBuff);
  tft.printAt(textBuff, 60, 210);
  dtostrf(NTC_FAN_Steinhart, 3, 1, textBuff);
  tft.printAt(textBuff, 113, 210);
  dtostrf(NTC_ROOM_Steinhart, 3, 1, textBuff);
  tft.printAt(textBuff, 168, 210);

  // Grail, 20221208, add for CART sensor
  dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 225, 210);


  delay(5000);


  // Display Button LED
  Button_LedState = 0;

  digitalWrite(TFT_LED, LOW);
  tft.fillScreen(ILI9341_BLACK);
}


//------------------------------------------------------------------------------------------------
void Step_Initialization() {
  // Display Start
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(3);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("WELCOME", gTextAlignMiddleCenter, 0, 0);

  tft.setTextScale(1);
  tft.printAlignedOffseted(FW_Version, gTextAlignMiddleCenter, 0, 110);

  digitalWrite(TFT_LED, HIGH);
  delay(3000);

  tft.setTextScale(2);
  tft.fillScreen(ILI9341_BLACK);
  tft.printAlignedOffseted("GETTING READY", gTextAlignMiddleCenter, 0, -90);
  tft.setTextScale(1);


  // Display Button LED
  Button_LedState = 1;


  //------------------------------------------------------
  tft.printAt("1. Linear Check", 40, 60);

  // Linear Check
  CURRENT_STAGE = 0;  // Grail, 20230118, for live demo
  Linear_Now_HighZ = -1;
  Linear_HighZ(0);
  //Linear_HighZ_Error = LOW;
  // Linear_L4_zDistance
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L4_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }


  //------------------------------------------------------
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);

  tft.printAt("2. Drawer Check", 40, 80);

  // Drawer Check
  if (digitalRead(LSW2) == 1)  // is open ?
  {
    Drawer_Close();
  }

  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }


  //------------------------------------------------------
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAt("3. Rotation Check", 40, 100);

  // Rotation Check
  Rotation_Angle(0);

  if (Rotation_Angle_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }


  //------------------------------------------------------
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAt("4. Optical Inspection Check", 40, 120);

  // Optical Inspection Check
  Rotation_TX_Angle_Align();

  if (Rotation_TX_Angle_Align_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 120);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 120);
  }


  //------------------------------------------------------
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAt("5. Thermometer Check", 40, 140);

  // Thermometer Check
  NTC_HET_Steinhart1 = NTC_HET1_Thermistor.temperature();
  NTC_HET_Steinhart2 = NTC_HET2_Thermistor.temperature();
  NTC_HET_Steinhart3 = NTC_HET3_Thermistor.temperature();
  NTC_HET_Steinhart4 = NTC_HET4_Thermistor.temperature();
  NTC_TEC_Steinhart = NTC_TEC_Thermistor.temperature();
  NTC_FAN_Steinhart = NTC_FAN_Thermistor.temperature();
  NTC_ROOM_Steinhart = NTC_ROOM_Thermistor.temperature();

  // Grail, 20221208, add for CART sensor
  NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();


  tft.printAt("HET1   HET2   HET3   HET4", 60, 160);
  tft.printAt("TEC    FAN    ROOM   CART", 60, 195);      // Grail, 20221208, add for CART sensor

  tft.setTextColor(ILI9341_YELLOW, ILI9341_BLACK);

  dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 60, 175);
  dtostrf(NTC_HET_Steinhart2, 3, 1, textBuff);
  tft.printAt(textBuff, 113, 175);
  dtostrf(NTC_HET_Steinhart3, 3, 1, textBuff);
  tft.printAt(textBuff, 170, 175);
  dtostrf(NTC_HET_Steinhart4, 3, 1, textBuff);
  tft.printAt(textBuff, 225, 175);

  dtostrf(NTC_TEC_Steinhart, 3, 1, textBuff);
  tft.printAt(textBuff, 60, 210);
  dtostrf(NTC_FAN_Steinhart, 3, 1, textBuff);
  tft.printAt(textBuff, 113, 210);
  dtostrf(NTC_ROOM_Steinhart, 3, 1, textBuff);
  tft.printAt(textBuff, 168, 210);

  // Grail, 20221208, add for CART sensor
  dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 225, 210);


  // Display Button LED
  delay(5000);
  Button_LedState = 0;
  ButtonLED_Standby_Mode();


  // Display End
  tft.setTextScale(2);
  tft.fillScreen(ILI9341_BLACK);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("SELF-INSPECTION", gTextAlignMiddleCenter, 0, -30);
  tft.printAlignedOffseted("COMPLETED", gTextAlignMiddleCenter, 0, 0);

  tft.setTextScale(1);
  tft.setTextColor(ILI9341_YELLOW, ILI9341_BLACK);
  tft.printAlignedOffseted("PRESS OPEN TO CONTINUE", gTextAlignMiddleCenter, 0, 40);
}


//------------------------------------------------------------------------------------------------
//  11 ~ 20 步驟程式
//------------------------------------------------------------------------------------------------
void Step_11() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 11", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. TX : Angle Align", 40, 100);
  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // TX : Angle Align //
  Rotation_TX_Angle_Align();
  if (Rotation_TX_Angle_Align_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_12() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 12", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. C2 : 6,000 RPM", 40, 100);
  tft.printAt("4. C2 : 3 Mins", 40, 120);
  tft.printAt("5. TX : Angle Align", 40, 140);
  tft.printAt("6. Valve = OFF", 40, 160);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // C2 : 6,000 RPM //
  Clutch_None_Engage();
  BLDC_Spinning_Start();
  BLDC_Spinning_6K();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 100);

  // C2 : 3 Mins //
  for (int counter = 0; counter <= Spinning_C2_Sec; counter += 1) {
    delay(1000);
  }
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // TX : Angle Align //
  Rotation_TX_Angle_Align();
  if (Rotation_TX_Angle_Align_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 140);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 140);
  }

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 160);
}

//------------------------------------------------------------------------------------------------
void Step_13() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 13", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B2 : Angle = ?", 40, 100);
  dtostrf(Rotation_B2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B2 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B2_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_14() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 14", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM3 : Z = ?", 40, 80);
  dtostrf(Linear_L3_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B2 : Angle = ?", 40, 100);
  dtostrf(Rotation_B2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM3 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L3_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B2 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B2_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_15() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 15", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM3 : Z = ?", 40, 80);
  dtostrf(Linear_L3_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B2 : Angle = ?", 40, 100);
  dtostrf(Rotation_B2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);

  tft.printAt("5. Valve 2 = ON , ?    ms", 40, 140);
  dtostrf(Vacuum_V2_ms, 4, 0, textBuff);
  tft.printAt(textBuff, 170, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM3 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L3_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B2 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B2_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve 2 = ON , ?    ms //
  PUMP_Valve(2, Vacuum_V2_ms);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_16() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 16", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B2 : Angle = ?", 40, 100);
  dtostrf(Rotation_B2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B2 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B2_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_17() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 17", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T1 : Angle = ?", 40, 100);
  dtostrf(Rotation_T1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_18() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 18", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM1 : Z = ?", 40, 80);
  dtostrf(Linear_L1_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T1 : Angle = ?", 40, 100);
  dtostrf(Rotation_T1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM1 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L1_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_19() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 19", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM1 : Z = ?", 40, 80);
  dtostrf(Linear_L1_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T1 : Angle = ?", 40, 100);
  dtostrf(Rotation_T1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);

  tft.printAt("5. Valve 1 = ON , ?    ms", 40, 140);
  dtostrf(Vacuum_V1_ms, 4, 0, textBuff);
  tft.printAt(textBuff, 170, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM1 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L1_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve 1 = ON , ?    ms //
  PUMP_Valve(1, Vacuum_V1_ms);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_20() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 20", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T1 : Angle = ?", 40, 100);
  dtostrf(Rotation_T1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}


//------------------------------------------------------------------------------------------------
//  21 ~ 30 步驟程式
//------------------------------------------------------------------------------------------------
void Step_21() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 21", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. C1 : 3,000 RPM", 40, 100);
  tft.printAt("4. C1 : Back & Forth 3 Cycle", 40, 120);
  tft.printAt("5. C1 : 20 Sec/Cycle", 40, 140);

  tft.printAt("6. T1 : Angle = ?", 40, 160);
  dtostrf(Rotation_T1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 160);

  tft.printAt("7. Valve = OFF", 40, 180);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // BLDC_Spinning_3K_20S_Cycle //
  Clutch_None_Engage();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 100);
  BLDC_Spinning_Start();
  BLDC_Spinning_3K_20S_Cycle();
  BLDC_Spinning_3K_20S_Cycle();
  BLDC_Spinning_3K_20S_Cycle();
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // TX : Angle Align //
  Rotation_TX_Angle_Align();

  // T1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 160);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 160);
  }

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 180);
}

//------------------------------------------------------------------------------------------------
void Step_22() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 22", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B1 : Angle = ?", 40, 100);
  dtostrf(Rotation_B1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_23() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 23", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM3 : Z = ?", 40, 80);
  dtostrf(Linear_L3_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B1 : Angle = ?", 40, 100);
  dtostrf(Rotation_B1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM3 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L3_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_24() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 24", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM3 : Z = ?", 40, 80);
  dtostrf(Linear_L3_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B1 : Angle = ?", 40, 100);
  dtostrf(Rotation_B1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);

  tft.printAt("5. Valve 3 = ON , ?    ms", 40, 140);
  dtostrf(Vacuum_V3_ms, 4, 0, textBuff);
  tft.printAt(textBuff, 170, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM3 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L3_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve 3 = ON , ?    ms //
  PUMP_Valve(3, Vacuum_V3_ms);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_25() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 25", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B1 : Angle = ?", 40, 100);
  dtostrf(Rotation_B1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_26() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 26", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T7 : Angle = ?", 40, 100);
  dtostrf(Rotation_T7_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T7 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T7_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_27() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 27", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM1 : Z = ?", 40, 80);
  dtostrf(Linear_L1_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T7 : Angle = ?", 40, 100);
  dtostrf(Rotation_T7_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM1 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L1_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T7 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T7_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_28() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 28", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM1 : Z = ?", 40, 80);
  dtostrf(Linear_L1_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T7 : Angle = ?", 40, 100);
  dtostrf(Rotation_T7_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);

  tft.printAt("5. Valve 1 = ON , ?    ms", 40, 140);
  dtostrf(Vacuum_V1_ms, 4, 0, textBuff);
  tft.printAt(textBuff, 170, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM1 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L1_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T7 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T7_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve 1 = ON , ?    ms //
  PUMP_Valve(1, Vacuum_V1_ms);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_29() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 29", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T7 : Angle = ?", 40, 100);
  dtostrf(Rotation_T7_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T7 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T7_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_30() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 30", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T2 : Angle = ?", 40, 100);
  dtostrf(Rotation_T2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T2 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T2_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}


//------------------------------------------------------------------------------------------------
//  31 ~ 40 步驟程式
//------------------------------------------------------------------------------------------------
void Step_31() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 31", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM1 : Z = ?", 40, 80);
  dtostrf(Linear_L1_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T2 : Angle = ?", 40, 100);
  dtostrf(Rotation_T2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM1 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L1_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T2 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T2_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_32() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 32", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM1 : Z = ?", 40, 80);
  dtostrf(Linear_L1_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T2 : Angle = ?", 40, 100);
  dtostrf(Rotation_T2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);

  tft.printAt("5. Valve 1 = ON , ?    ms", 40, 140);
  dtostrf(Vacuum_V1_ms, 4, 0, textBuff);
  tft.printAt(textBuff, 170, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM1 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L1_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T2 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T2_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve 1 = ON , ?    ms //
  PUMP_Valve(1, Vacuum_V1_ms);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_33() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 33", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T1 : Angle = ?", 40, 100);
  dtostrf(Rotation_T1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_34() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 34", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T3 : Angle = ?", 40, 100);
  dtostrf(Rotation_T3_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T3 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T3_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_35() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 35", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM1 : Z = ?", 40, 80);
  dtostrf(Linear_L1_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T3 : Angle = ?", 40, 100);
  dtostrf(Rotation_T3_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM1 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L1_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T3 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T3_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_36() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 36", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM1 : Z = ?", 40, 80);
  dtostrf(Linear_L1_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T3 : Angle = ?", 40, 100);
  dtostrf(Rotation_T3_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);

  tft.printAt("5. Valve 1 = ON , ?    ms", 40, 140);
  dtostrf(Vacuum_V1_ms, 4, 0, textBuff);
  tft.printAt(textBuff, 170, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM1 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L1_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T3 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T3_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve 1 = ON , ?    ms //
  PUMP_Valve(1, Vacuum_V1_ms);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_37() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 37", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T3 : Angle = ?", 40, 100);
  dtostrf(Rotation_T2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T3 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T3_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_38() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 38", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. C1 : 3,000 RPM", 40, 100);
  tft.printAt("4. C1 : Back & Forth 3 Cycle", 40, 120);
  tft.printAt("5. C1 : 10 Sec/Cycle", 40, 140);

  tft.printAt("6. T3 : Angle = ?", 40, 160);
  dtostrf(Rotation_T3_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 160);

  tft.printAt("7. Valve = OFF", 40, 180);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // BLDC_Spinning_3K_20S_Cycle //
  Clutch_None_Engage();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 100);
  BLDC_Spinning_Start();
  BLDC_Spinning_3K_10S_Cycle();
  BLDC_Spinning_3K_10S_Cycle();
  BLDC_Spinning_3K_10S_Cycle();
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // TX : Angle Align //
  Rotation_TX_Angle_Align();

  // T3 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T3_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 160);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 160);
  }

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 180);
}

//------------------------------------------------------------------------------------------------
void Step_39() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 39", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B2 : Angle = ?", 40, 100);
  dtostrf(Rotation_B2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B2 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B2_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_40() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 40", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM3 : Z = ?", 40, 80);
  dtostrf(Linear_L3_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B2 : Angle = ?", 40, 100);
  dtostrf(Rotation_B2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM3 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L3_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B2 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B2_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}


//------------------------------------------------------------------------------------------------
//  41 ~ 50 步驟程式
//------------------------------------------------------------------------------------------------
void Step_41() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 41", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM3 : Z = ?", 40, 80);
  dtostrf(Linear_L3_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B2 : Angle = ?", 40, 100);
  dtostrf(Rotation_B2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);

  tft.printAt("5. Valve 1 = ON , ?    ms", 40, 140);
  dtostrf(Vacuum_V1_ms, 4, 0, textBuff);
  tft.printAt(textBuff, 170, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM3 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L3_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B2 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B2_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve 1 = ON , ?    ms //
  PUMP_Valve(1, Vacuum_V1_ms);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_42() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 42", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM3 : Z = ?", 40, 80);
  dtostrf(Linear_L3_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B2 : Angle = ?", 40, 100);
  dtostrf(Rotation_B2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);
  tft.printAt("6. Cooler = -4 C", 40, 160);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM3 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L3_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B2 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B2_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // Cooler = -4 C //
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLUE);
  tft.printAt(" ON ", 250, 160);
  /*
  for (int counter = 0; counter <= Cooler_4C_Sec; counter += 1) {
    Cooler_PID(HIGH);
  }
  Cooler_PID(LOW);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 160);
  */
  Step_TEC(60000);
}

//------------------------------------------------------------------------------------------------
void Step_43() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 43", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B2 : Angle = ?", 40, 100);
  dtostrf(Rotation_B2_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B2 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B2_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_44() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 44", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. C3 : 12,000 RPM", 40, 100);
  tft.printAt("4. C3 : 3 Mins", 40, 120);
  tft.printAt("5. TX : Angle Align", 40, 140);
  tft.printAt("6. Valve = OFF", 40, 160);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // C3 : 12,000 RPM //
  Clutch_None_Engage();
  BLDC_Spinning_Start();
  BLDC_Spinning_12K();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 100);

  // C3 : 3 Mins //
  for (int counter = 0; counter <= Spinning_C3_Sec; counter += 1) {
    delay(1000);
  }
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // TX : Angle Align //
  Rotation_TX_Angle_Align();
  if (Rotation_TX_Angle_Align_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 140);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 140);
  }

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 160);
}

//------------------------------------------------------------------------------------------------
void Step_45() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 45", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B1 : Angle = ?", 40, 100);
  dtostrf(Rotation_B1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_46() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 46", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM3 : Z = ?", 40, 80);
  dtostrf(Linear_L3_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B1 : Angle = ?", 40, 100);
  dtostrf(Rotation_B1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM3 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L3_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_47() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 47", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM3 : Z = ?", 40, 80);
  dtostrf(Linear_L3_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B1 : Angle = ?", 40, 100);
  dtostrf(Rotation_B1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);

  tft.printAt("5. Valve 3 = ON , ?    ms", 40, 140);
  dtostrf(Vacuum_V3_ms, 4, 0, textBuff);
  tft.printAt(textBuff, 170, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM3 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L3_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve 3 = ON , ?    ms //
  PUMP_Valve(3, Vacuum_V3_ms);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_48() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 48", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B1 : Angle = ?", 40, 100);
  dtostrf(Rotation_B1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_49() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 49", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T4 : Angle = ?", 40, 100);
  dtostrf(Rotation_T4_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T4 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T4_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_50() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 50", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM1 : Z = ?", 40, 80);
  dtostrf(Linear_L1_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T4 : Angle = ?", 40, 100);
  dtostrf(Rotation_T4_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM1 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L1_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T4 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T4_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}


//------------------------------------------------------------------------------------------------
//  51 ~ 60 步驟程式
//------------------------------------------------------------------------------------------------
void Step_51() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 51", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM1 : Z = ?", 40, 80);
  dtostrf(Linear_L1_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T4 : Angle = ?", 40, 100);
  dtostrf(Rotation_T4_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);

  tft.printAt("5. Valve 1 = ON , ?    ms", 40, 140);
  dtostrf(Vacuum_V1_ms, 4, 0, textBuff);
  tft.printAt(textBuff, 170, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM1 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L1_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T4 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T4_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve 1 = ON , ?    ms //
  PUMP_Valve(1, Vacuum_V1_ms);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_52() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 52", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. T4 : Angle = ?", 40, 100);
  dtostrf(Rotation_T4_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T4 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T4_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_53() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 53", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. C1 : 3,000 RPM", 40, 100);
  tft.printAt("4. C1 : Back & Forth 3 Cycle", 40, 120);
  tft.printAt("5. C1 : 20 Sec/Cycle", 40, 140);

  tft.printAt("6. T4 : Angle = ?", 40, 160);
  dtostrf(Rotation_T4_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 160);

  tft.printAt("7. Valve = OFF", 40, 180);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // BLDC_Spinning_3K_20S_Cycle //
  Clutch_None_Engage();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 100);
  BLDC_Spinning_Start();
  BLDC_Spinning_3K_20S_Cycle();
  BLDC_Spinning_3K_20S_Cycle();
  BLDC_Spinning_3K_20S_Cycle();
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // TX : Angle Align //
  Rotation_TX_Angle_Align();

  // T4 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T4_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 160);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 160);
  }

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 180);
}

//------------------------------------------------------------------------------------------------
void Step_54() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 54", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B3 : Angle = ?", 40, 100);
  dtostrf(Rotation_B3_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B3 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B3_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_55() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 55", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM3 : Z = ?", 40, 80);
  dtostrf(Linear_L3_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B3 : Angle = ?", 40, 100);
  dtostrf(Rotation_B3_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM3 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L3_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B3 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B3_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_56() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 56", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM3 : Z = ?", 40, 80);
  dtostrf(Linear_L3_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B3 : Angle = ?", 40, 100);
  dtostrf(Rotation_B3_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);

  tft.printAt("5. Valve 4 = ON , ?    ms", 40, 140);
  dtostrf(Vacuum_V4_ms, 4, 0, textBuff);
  tft.printAt(textBuff, 170, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM1 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L1_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // T1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_T1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve 4 = ON , ?    ms //
  PUMP_Valve(4, Vacuum_V4_ms);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_57() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 57", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B1 : Angle = ?", 40, 100);
  dtostrf(Rotation_B1_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B1 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B1_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_58() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 58", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B5 : Angle = ?", 40, 100);
  dtostrf(Rotation_B5_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B5 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B5_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_59() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 59", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B5 : Angle = ?", 40, 100);
  dtostrf(Rotation_B5_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);
  tft.printAt("6. Heat 1-1 = 95 C", 40, 160);
  tft.printAt("7. Heat 1-1 = 2 Mins", 40, 180);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B5 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B5_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // Heat 1-1 = 95 C //
  tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
  tft.printAt(" ON ", 250, 160);
  /*
  for (int counter = 0; counter <= Heater_H11_95C_Sec; counter += 1) {
    Heater_PID(HIGH);
  }
  Heater_PID(LOW);

  // Heat 1-1 = 2 Mins //
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 180);
  */
  Step_HEAT_95_2(120000);
}

//------------------------------------------------------------------------------------------------
void Step_60() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 60", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B6 : Angle = ?", 40, 100);
  dtostrf(Rotation_B6_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B6 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B6_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}


//------------------------------------------------------------------------------------------------
//  61 ~ 70 步驟程式
//------------------------------------------------------------------------------------------------
void Step_61() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 61", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B6 : Angle = ?", 40, 100);
  dtostrf(Rotation_B6_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);
  tft.printAt("6. Heat 2-1 = 55 C", 40, 160);
  tft.printAt("7. Heat 2-1 = 5 Mins", 40, 180);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B6 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B6_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // Heat 2-1 = 55 C //
  tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
  tft.printAt(" ON ", 250, 160);
  
  /*
  for (int counter = 0; counter <= Heater_H21_55C_Sec; counter += 1) {
    Heater_PID(HIGH);
  }
  Heater_PID(LOW);

  // Heat 2-1 = 5 Mins //
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 180);
  */
  Step_HEAT_55_1(300000);

}

//------------------------------------------------------------------------------------------------
void Step_62() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 62", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B5 : Angle = ?", 40, 100);
  dtostrf(Rotation_B5_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B5 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B5_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_63() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 63", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B5 : Angle = ?", 40, 100);
  dtostrf(Rotation_B5_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);
  tft.printAt("6. Heat 1-2 = 95 C", 40, 160);
  tft.printAt("7. Heat 1-2 = 3 Sec", 40, 180);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B5 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B5_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // Heat 1-2 = 95 C //
  tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
  tft.printAt(" ON ", 250, 160);
  /*
  for (int counter = 0; counter <= Heater_H12_95C_Sec; counter += 1) {
    Heater_PID(HIGH);
  }
  Heater_PID(LOW);

  // Heat 1-2 = 3 Sec //
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 180);
  */
  Step_HEAT_95_2(30000);

}

//------------------------------------------------------------------------------------------------
void Step_64() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 64", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B6 : Angle = ?", 40, 100);
  dtostrf(Rotation_B6_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B6 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B6_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_65() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 65", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B6 : Angle = ?", 40, 100);
  dtostrf(Rotation_B6_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);
  tft.printAt("6. Heat 2-2 = 55 C", 40, 160);
  tft.printAt("7. Heat 2-2 = 60 Sec", 40, 180);
  tft.printAt("8. LED = 3 Sec", 40, 200);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B6 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B6_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // Heat 2-2 = 55 C //
  tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
  tft.printAt(" ON ", 250, 160);
  /*
  for (int counter = 0; counter <= Heater_H22_55C_Sec; counter += 1) {
    Heater_PID(HIGH);
  }
  Heater_PID(LOW);

  // Heat 2-2 = 60 Sec //
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 180);
  */
  Step_HEAT_55_1(60000);

  // LED = 3 Sec //
  RGB_LED(1);
  delay(LED_Blue_ms);
  //tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  //tft.printAt(" OK ", 250, 200);
  RGB_LED(0);
}

//------------------------------------------------------------------------------------------------
void Step_66() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 66", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B5 : Angle = ?", 40, 100);
  dtostrf(Rotation_B5_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B5 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B5_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_67() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 67", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B5 : Angle = ?", 40, 100);
  dtostrf(Rotation_B5_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);
  tft.printAt("6. Heat 1-2 = 95 C", 40, 160);
  tft.printAt("7. Heat 1-2 = 3 Sec", 40, 180);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B5 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B5_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // Heat 1-2 = 95 C //
  tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
  tft.printAt(" ON ", 250, 160);
  /*
  for (int counter = 0; counter <= Heater_H12_95C_Sec; counter += 1) {
    Heater_PID(HIGH);
  }
  Heater_PID(LOW);

  // Heat 1-2 = 3 Sec //
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 180);
  */
  Step_HEAT_95_2(30000);

}

//------------------------------------------------------------------------------------------------
void Step_68() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 68", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B6 : Angle = ?", 40, 100);
  dtostrf(Rotation_B6_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B6 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B6_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_69() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 69", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B6 : Angle = ?", 40, 100);
  dtostrf(Rotation_B6_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);
  tft.printAt("6. Heat 2-2 = 55 C", 40, 160);
  tft.printAt("7. Heat 2-2 = 60 Sec", 40, 180);
  tft.printAt("8. LED = 3 Sec", 40, 200);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B6 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B6_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // Heat 2-2 = 55 C //
  tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
  tft.printAt(" ON ", 250, 160);
  
  /*
  for (int counter = 0; counter <= Heater_H22_55C_Sec; counter += 1) {
    Heater_PID(HIGH);
  }
  Heater_PID(LOW);

  // Heat 2-2 = 60 Sec //
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 180);
  */
  Step_HEAT_55_1(60000);


  // LED = 3 Sec //
  RGB_LED(3);
  delay(LED_Green_ms);
  //tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  //tft.printAt(" OK ", 250, 200);
  RGB_LED(0);
}

//------------------------------------------------------------------------------------------------
void Step_70() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 70", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B5 : Angle = ?", 40, 100);
  dtostrf(Rotation_B5_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B5 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B5_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}


//------------------------------------------------------------------------------------------------
//  71 ~ 75 步驟程式
//------------------------------------------------------------------------------------------------
void Step_71() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 71", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B5 : Angle = ?", 40, 100);
  dtostrf(Rotation_B5_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);
  tft.printAt("6. Heat 1-2 = 95 C", 40, 160);
  tft.printAt("7. Heat 1-2 = 3 Sec", 40, 180);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B5 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B5_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // Heat 1-2 = 95 C //
  tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
  tft.printAt(" ON ", 250, 160);
  /*
  for (int counter = 0; counter <= Heater_H12_95C_Sec; counter += 1) {
    Heater_PID(HIGH);
  }
  Heater_PID(LOW);

  // Heat 1-2 = 3 Sec //
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 180);
  */
  Step_HEAT_95_2(30000);

}

//------------------------------------------------------------------------------------------------
void Step_72() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 72", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B6 : Angle = ?", 40, 100);
  dtostrf(Rotation_B6_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B6 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B6_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);
}

//------------------------------------------------------------------------------------------------
void Step_73() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 73", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B6 : Angle = ?", 40, 100);
  dtostrf(Rotation_B6_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);
  tft.printAt("6. Heat 2-2 = 55 C", 40, 160);
  tft.printAt("7. Heat 2-2 = 60 Sec", 40, 180);
  tft.printAt("8. LED = 3 Sec", 40, 200);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B6 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B6_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // Heat 2-2 = 55 C //
  tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
  tft.printAt(" ON ", 250, 160);
  /*
  for (int counter = 0; counter <= Heater_H22_55C_Sec; counter += 1) {
    Heater_PID(HIGH);
  }
  Heater_PID(LOW);

  // Heat 2-2 = 60 Sec //
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 180);
  */
  Step_HEAT_55_1(60000);

  // LED = 3 Sec //
  RGB_LED(4);
  delay(LED_Red_ms);
  //tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  //tft.printAt(" OK ", 250, 200);
  RGB_LED(0);
}

//------------------------------------------------------------------------------------------------
void Step_74() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP 74", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);
  tft.printAt("1. DW : Closed", 40, 60);

  tft.printAt("2. LM2 : Z = ?", 40, 80);
  dtostrf(Linear_L2_zDistance, 4, 0, textBuff);
  tft.printAt(textBuff, 130, 80);

  tft.printAt("3. B6 : Angle = ?", 40, 100);
  dtostrf(Rotation_B6_Angle, 4, 0, textBuff);
  tft.printAt(textBuff, 153, 100);

  tft.printAt("4. C0 : 0 RPM", 40, 120);
  tft.printAt("5. Valve = OFF", 40, 140);
  tft.printAt("6. Display Test Result", 40, 160);

  digitalWrite(TFT_LED, HIGH);


  // DW : Closed //
  Drawer_Close();
  if (Drawer_Close_Error == LOW) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 60);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 60);
  }

  // LM2 : Z = ? //
  if (Linear_HighZ_Error == LOW) {
    Linear_HighZ(Linear_L2_zDistance);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 80);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 80);
  }

  // B6 : Angle = ? //
  if (Rotation_Angle_Error == LOW) {
    Rotation_Angle(Rotation_B6_Angle);
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 100);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" FAIL ", 250, 100);
  }

  // C0 : 0 RPM //
  BLDC_Spinning_Stop();
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 120);

  // Valve = OFF //
  PUMP_Valve(0, 0);
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 140);

  // Display Test Result //
  tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
  tft.printAt(" OK ", 250, 160);


  // Test Completed //
  delay(2000);

  digitalWrite(TFT_LED, LOW);
  tft.fillScreen(ILI9341_BLUE);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLUE);
  tft.printAlignedOffseted("Test Completed", gTextAlignMiddleCenter, 0, -70);

  tft.setTextScale(1);
  tft.printAlignedOffseted("Ch1 : CT = 20 ~ 40", gTextAlignMiddleCenter, 0, -20);
  tft.printAlignedOffseted("Ch2 : CT = 20 ~ 40", gTextAlignMiddleCenter, 0, 0);
  tft.printAlignedOffseted("Ch3 : CT = 20 ~ 40", gTextAlignMiddleCenter, 0, 20);
  tft.printAlignedOffseted("Ch4 : CT = 20 ~ 40", gTextAlignMiddleCenter, 0, 40);

  tft.setTextColor(ILI9341_YELLOW, ILI9341_BLUE);
  tft.printAlignedOffseted("This page is demonstration.", gTextAlignMiddleCenter, 0, 80);

  digitalWrite(TFT_LED, HIGH);
  delay(5000);
}

//------------------------------------------------------------------------------------------------
void Step_75() {
  uint16_t i, j;

  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLUE);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLUE);
  tft.printAlignedOffseted("Report Sent", gTextAlignMiddleCenter, 0, 0);

  digitalWrite(TFT_LED, HIGH);

  delay(1000);
  tft.drawRect(35, 175, 251, 20, ILI9341_WHITE);
  for (i = 1; i < 242; i += 2.4) {
    tft.fillRect(40, 180, i, 10, ILI9341_WHITE);
    j = i / 2.4;
    delay(20);
  }

  tft.fillScreen(ILI9341_BLUE);
  tft.printAlignedOffseted("SEQUENCE", gTextAlignMiddleCenter, 0, -30);
  tft.printAlignedOffseted("COMPLETED", gTextAlignMiddleCenter, 0, 0);

  tft.setTextScale(1);
  tft.setTextColor(ILI9341_YELLOW, ILI9341_BLUE);
  tft.printAlignedOffseted("PRESS OPEN TO CONTINUE", gTextAlignMiddleCenter, 0, 40);
}

//---------------------------------------------------------------------


void Step_TEC(unsigned long iTimeMs) {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP DOE_TEC", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);

  tft.printAt("1. Cooler = -4 C", 40, 160);

  digitalWrite(TFT_LED, HIGH);


  // Cooler = -4 C //
  NTC_TEC_Steinhart = NTC_TEC_Thermistor.temperature();
  NTC_FAN_Steinhart = NTC_FAN_Thermistor.temperature();
  NTC_ROOM_Steinhart = NTC_ROOM_Thermistor.temperature();
  NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();

  tft.printAt("TEC temp. =", 40, 60);
  dtostrf(NTC_TEC_Steinhart, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 60);

  tft.printAt("FAN temp. =", 40, 80);
  dtostrf(NTC_FAN_Steinhart, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 80);

  tft.printAt("Cooling Time =", 40, 100);

  tft.printAt("Keeping Time =", 40, 120);

  tft.printAt("Cart. temp. =", 40, 140);
  dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 140);


  tft.setTextColor(ILI9341_WHITE, ILI9341_BLUE);
  tft.printAt(" ON ", 250, 160);

  unsigned long startTime = 0;
  unsigned long currentTime = 0;

  float deltaTime = 0;

  startTime = millis();

  while (NTC_TEC_Steinhart > TEC_SetPoint) {
    Cooler_PID(HIGH);

    // showing the Cooling Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 100);

    // showing the temperature
    dtostrf(NTC_TEC_Steinhart, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    dtostrf(NTC_FAN_Steinhart, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 80);

    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 140);


    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_TEC_Steinhart);
      Serial.println(NTC_FAN_Steinhart);
      Serial.println(NTC_CART_Steinhart1);
    }

    if (NTC_FAN_Steinhart >= 60) break;
  }


  startTime = millis();
  deltaTime = 0;

  while (deltaTime < iTimeMs) {    // 600000 ms = 600 sec, 60000 ms = 60sec
    Cooler_PID(HIGH);

    // showing the Cooling Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 120);

    // showing the temperature
    dtostrf(NTC_TEC_Steinhart, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    dtostrf(NTC_FAN_Steinhart, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 80);

    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 140);

    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_TEC_Steinhart);
      Serial.println(NTC_FAN_Steinhart);
      Serial.println(NTC_CART_Steinhart1);
    }

    if (NTC_FAN_Steinhart >= 60) break;
  }

  Cooler_PID(LOW);


  if (NTC_FAN_Steinhart >= 100) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" WARN ", 250, 160);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 160);
  }
}

//---------------------------------------------------------------------
void Step_HEAT_55() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP DOE_HEAT55", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);

  tft.printAt("1. Heat 1,3 = 55 C", 40, 160);

  digitalWrite(TFT_LED, HIGH);

  // Heat 1,3 = 55 C //
  NTC_HET_Steinhart1 = NTC_HET1_Thermistor.temperature();
  NTC_HET_Steinhart3 = NTC_HET3_Thermistor.temperature();
  NTC_ROOM_Steinhart = NTC_ROOM_Thermistor.temperature();
  NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();

  tft.printAt("Heat1 temp. =", 40, 60);
  dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 60);

  tft.printAt("Heat3 temp. =", 40, 80);
  dtostrf(NTC_HET_Steinhart3, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 80);

  tft.printAt("Heating Time =", 40, 100);

  tft.printAt("Keeping Time =", 40, 120);

  tft.printAt("Cart. temp. =", 40, 140);
  dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 140);


  tft.setTextColor(ILI9341_WHITE, ILI9341_BLUE);
  tft.printAt(" ON ", 250, 160);

  unsigned long startTime = 0;
  unsigned long currentTime = 0;

  float deltaTime = 0;

  startTime = millis();
  // HET_SetPoint1 = 55
  while ((NTC_HET_Steinhart1 < HET_SetPoint1) || (NTC_HET_Steinhart3 < HET_SetPoint1)) {
    Heater1_PID(HIGH);
    Heater3_PID(HIGH);
    
    // showing the Heating Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 100);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    dtostrf(NTC_HET_Steinhart3, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 80);

    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 140);


    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart1);
      Serial.println(NTC_HET_Steinhart3);
      
      Serial.println(NTC_CART_Steinhart1);
    }

    if (NTC_HET_Steinhart1 >= 120) break;
    if (NTC_HET_Steinhart3 >= 120) break;
  }


  startTime = millis();
  deltaTime = 0;

  while (deltaTime < 60000) {   // 60000 ms = 60 sec
    Heater1_PID(HIGH);
    Heater3_PID(HIGH);

    // showing the Cooling Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 120);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    dtostrf(NTC_HET_Steinhart3, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 80);

    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 140);


    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart1);
      Serial.println(NTC_HET_Steinhart3);

      Serial.println(NTC_CART_Steinhart1);

    }

    if (NTC_HET_Steinhart1 >= 120) break;
    if (NTC_HET_Steinhart3 >= 120) break;
  }

  Heater1_PID(LOW);
  Heater3_PID(LOW);
  

if ((NTC_HET_Steinhart1 >= 120) || (NTC_HET_Steinhart3 >= 120)) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" WARN ", 250, 160);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 160);
  }
}

void Step_HEAT_95() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP DOE_HEAT95", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);

  tft.printAt("1. Heat 2,4 = 95 C", 40, 160);

  digitalWrite(TFT_LED, HIGH);




  // Heat 2,4 = 95 C //
  NTC_HET_Steinhart2 = NTC_HET2_Thermistor.temperature();
  NTC_HET_Steinhart4 = NTC_HET4_Thermistor.temperature();
  NTC_ROOM_Steinhart = NTC_ROOM_Thermistor.temperature();
  NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();

  tft.printAt("Heat2 temp. =", 40, 60);
  dtostrf(NTC_HET_Steinhart2, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 60);

  tft.printAt("Heat4 temp. =", 40, 80);
  dtostrf(NTC_HET_Steinhart4, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 80);

  tft.printAt("Heating Time =", 40, 100);

  tft.printAt("Keeping Time =", 40, 120);

  tft.printAt("Cart. temp. =", 40, 140);
  dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 140);



  tft.setTextColor(ILI9341_WHITE, ILI9341_BLUE);
  tft.printAt(" ON ", 250, 160);

  unsigned long startTime = 0;
  unsigned long currentTime = 0;

  float deltaTime = 0;

  startTime = millis();
  // HET_SetPoint2 = 95, but it's 55 now  !!!WARN!!!
  while ((NTC_HET_Steinhart2 < HET_SetPoint2) || (NTC_HET_Steinhart4 < HET_SetPoint2)) {
    Heater2_PID(HIGH);
    Heater4_PID(HIGH);
    
    // showing the Heating Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 100);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart2, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    dtostrf(NTC_HET_Steinhart4, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 80);

    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 140);


    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart2);
      Serial.println(NTC_HET_Steinhart4);
      Serial.println(NTC_CART_Steinhart1);
    }

    if (NTC_HET_Steinhart2 >= 120) break;
    if (NTC_HET_Steinhart4 >= 120) break;
  }


  startTime = millis();
  deltaTime = 0;

  while (deltaTime < 60000) {   // 60000 ms = 60 sec
    Heater2_PID(HIGH);
    Heater4_PID(HIGH);

    // showing the Cooling Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 120);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart2, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    dtostrf(NTC_HET_Steinhart4, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 80);

    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 140);


    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart2);
      Serial.println(NTC_HET_Steinhart4);
      Serial.println(NTC_CART_Steinhart1);
    }

    if (NTC_HET_Steinhart2 >= 120) break;
    if (NTC_HET_Steinhart4 >= 120) break;
  }

  Heater2_PID(LOW);
  Heater4_PID(LOW);
  

if ((NTC_HET_Steinhart2 >= 120) || (NTC_HET_Steinhart4 >= 120)) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" WARN ", 250, 160);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 160);
  }
}

//----------------------------------------------------------------------------------------------------------------------
// Heat 1 only, for 55 dC
void Step_HEAT_55_1(unsigned long iTimeMs) {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP DOE_HEAT55", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);

  tft.printAt("1. Heat 1 = 55 C", 40, 160);

  digitalWrite(TFT_LED, HIGH);

  // Heat 1 = 55 C //
  NTC_HET_Steinhart1 = NTC_HET1_Thermistor.temperature();
  NTC_HET_Steinhart3 = NTC_HET2_Thermistor.temperature();
  NTC_ROOM_Steinhart = NTC_ROOM_Thermistor.temperature();
  NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();

  tft.printAt("Heat1 temp. =", 40, 60);
  dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 60);

  //tft.printAt("Heat3 temp. =", 40, 80);
  //dtostrf(NTC_HET_Steinhart3, 3, 1, textBuff);
  //tft.printAt(textBuff, 150, 80);

  tft.printAt("Heating Time =", 40, 100);

  tft.printAt("Keeping Time =", 40, 120);

  tft.printAt("Cart. temp. =", 40, 140);
  dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 140);


  tft.setTextColor(ILI9341_WHITE, ILI9341_BLUE);
  tft.printAt(" ON ", 250, 160);

  unsigned long startTime = 0;
  unsigned long currentTime = 0;

  float deltaTime = 0;

  startTime = millis();
  // HET_SetPoint1 = 55
  while (NTC_HET_Steinhart1 < HET_SetPoint1) {
    Heater1_PID(HIGH);
    //Heater3_PID(LOW);
    
    // showing the Heating Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 100);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    //dtostrf(NTC_HET_Steinhart3, 3, 1, textBuff);
    //tft.printAt(textBuff, 150, 80);

    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 140);


    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart1);
      Serial.println(NTC_HET_Steinhart3);
      Serial.println(NTC_CART_Steinhart1);
    }

    if (NTC_HET_Steinhart1 >= 120) break;
    //if (NTC_HET_Steinhart3 >= 120) break;
  }


  startTime = millis();
  deltaTime = 0;

  while (deltaTime < iTimeMs) {   // 60000 ms = 60 sec
    Heater1_PID(HIGH);
    //Heater3_PID(LOW);

    // showing the Heating Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 120);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    //dtostrf(NTC_HET_Steinhart3, 3, 1, textBuff);
    //tft.printAt(textBuff, 150, 80);

    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 140);


    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart1);
      Serial.println(NTC_HET_Steinhart3);
      Serial.println(NTC_CART_Steinhart1);

    }

    if (NTC_HET_Steinhart1 >= 120) break;
    //if (NTC_HET_Steinhart3 >= 120) break;
  }

  Heater1_PID(LOW);
  //Heater3_PID(LOW);
  
if ((NTC_HET_Steinhart1 >= 120) || (NTC_HET_Steinhart3 >= 120)) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" WARN ", 250, 160);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 160);
  }
}

void Step_HEAT_95_2(unsigned long iTimeMs) {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP DOE_HEAT95", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);

  tft.printAt("1. Heat 2 = 95 C", 40, 160);

  digitalWrite(TFT_LED, HIGH);

  // Heat 2 = 95 C //
  NTC_HET_Steinhart2 = NTC_HET2_Thermistor.temperature();
  NTC_HET_Steinhart4 = NTC_HET1_Thermistor.temperature();
  NTC_ROOM_Steinhart = NTC_ROOM_Thermistor.temperature();
  NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();

  tft.printAt("Heat2 temp. =", 40, 60);
  dtostrf(NTC_HET_Steinhart2, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 60);

  //tft.printAt("Heat4 temp. =", 40, 80);
  //dtostrf(NTC_HET_Steinhart4, 3, 1, textBuff);
  //tft.printAt(textBuff, 150, 80);

  tft.printAt("Heating Time =", 40, 100);

  tft.printAt("Keeping Time =", 40, 120);

  tft.printAt("Cart. temp. =", 40, 140);
  dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 140);



  tft.setTextColor(ILI9341_WHITE, ILI9341_BLUE);
  tft.printAt(" ON ", 250, 160);

  unsigned long startTime = 0;
  unsigned long currentTime = 0;

  float deltaTime = 0;

  startTime = millis();
  // HET_SetPoint2 = 95, but it's 55 now  !!!WARN!!!
  while (NTC_HET_Steinhart2 < HET_SetPoint2) {
    Heater2_PID(HIGH);
    //Heater4_PID(LOW);
    
    // showing the Heating Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 100);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart2, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    //dtostrf(NTC_HET_Steinhart4, 3, 1, textBuff);
    //tft.printAt(textBuff, 150, 80);

    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 140);


    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart2);
      Serial.println(NTC_HET_Steinhart4);
      Serial.println(NTC_CART_Steinhart1);
    }

    if (NTC_HET_Steinhart2 >= 120) break;
    //if (NTC_HET_Steinhart4 >= 120) break;
  }


  startTime = millis();
  deltaTime = 0;

  while (deltaTime < iTimeMs) {   // 60000 ms = 60 sec
    Heater2_PID(HIGH);
    //Heater4_PID(LOW);

    // showing the Cooling Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 120);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart2, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    //dtostrf(NTC_HET_Steinhart4, 3, 1, textBuff);
    //tft.printAt(textBuff, 150, 80);

    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 140);


    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart2);
      Serial.println(NTC_HET_Steinhart4);
      Serial.println(NTC_CART_Steinhart1);
    }

    if (NTC_HET_Steinhart2 >= 120) break;
    //if (NTC_HET_Steinhart4 >= 120) break;
  }

  Heater2_PID(LOW);
  //Heater4_PID(LOW);
  
if ((NTC_HET_Steinhart2 >= 120) || (NTC_HET_Steinhart4 >= 120)) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" WARN ", 250, 160);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 160);
  }
}

//----------------------------------------------------------------------------------------------------------------------
void Step_HEAT_55_cart(unsigned long iTimeMs) 
{
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP DOE_HEAT55_cart", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);

  tft.printAt("1. Heat 1 = 55 C", 40, 160);

  digitalWrite(TFT_LED, HIGH);




  // Heat 1 = 55 C //
  NTC_HET_Steinhart1 = NTC_HET1_Thermistor.temperature();
  NTC_ROOM_Steinhart = NTC_ROOM_Thermistor.temperature();
  NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();

  tft.printAt("Heat1 temp. =", 40, 60);
  dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 60);

  tft.printAt("CART temp. =", 40, 80);
  dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 80);

  tft.printAt("Heating Time =", 40, 100);

  tft.printAt("Keeping Time =", 40, 120);


  tft.setTextColor(ILI9341_WHITE, ILI9341_BLUE);
  tft.printAt(" ON ", 250, 160);

  unsigned long startTime = 0;
  unsigned long currentTime = 0;

  float deltaTime = 0;

  startTime = millis();
  // HET_SetPoint1 = 55
  
  if (NTC_CART_Steinhart1 <= HET_SetPoint1) {
      // use heater only, no TEC
      while (NTC_CART_Steinhart1 < HET_SetPoint1) {
        Heater1_PID(HIGH);
    
        // showing the Heating Time
        currentTime = millis();
        deltaTime = currentTime - startTime;
        tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
        dtostrf(deltaTime, 3, 1, textBuff);
        tft.printAt(textBuff, 160, 100);

        // showing the temperature
        dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
        tft.printAt(textBuff, 150, 60);
        
        NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
        dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
        tft.printAt(textBuff, 150, 80);        

        if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
          Serial.println(deltaTime);
          Serial.println(NTC_HET_Steinhart1);
          Serial.println(NTC_CART_Steinhart1);
        }

        if (NTC_HET_Steinhart1 >= 60) break;
      }
  }
  else
  {
      // use heater and TEC
      while (NTC_CART_Steinhart1 > HET_SetPoint1) {
        Heater1_PID(HIGH);
    
        // showing the Heating Time
        currentTime = millis();
        deltaTime = currentTime - startTime;
        tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
        dtostrf(deltaTime, 3, 1, textBuff);
        tft.printAt(textBuff, 160, 100);

        // showing the temperature
        dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
        tft.printAt(textBuff, 150, 60);
        
        NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
        dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
        tft.printAt(textBuff, 150, 80);


        if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
          Serial.println(deltaTime);
          Serial.println(NTC_HET_Steinhart1);
          Serial.println(NTC_CART_Steinhart1);

        }

        if (NTC_HET_Steinhart1 >= 100) break;
      }
  }
  
  startTime = millis();
  deltaTime = 0;

  while (deltaTime < iTimeMs) {   // 60000 ms = 60 sec
    Heater1_PID(HIGH);

    // showing the Cooling Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 120);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);

    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart1);
    }

    if (NTC_HET_Steinhart1 >= 100) break;
  }

  Heater1_PID(LOW);
  

if (NTC_HET_Steinhart1 >= 100) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" WARN ", 250, 160);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 160);
  }
}

void Step_HEAT_95_cart(unsigned long iTimeMs) 
{
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP DOE_HEAT95_cart", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);

  tft.printAt("1. Heat 1 = 95 C", 40, 160);

  digitalWrite(TFT_LED, HIGH);




  // Heat 2 = 95 C //
  NTC_HET_Steinhart2 = NTC_HET2_Thermistor.temperature();
  NTC_ROOM_Steinhart = NTC_ROOM_Thermistor.temperature();
  NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();

  tft.printAt("Heat2 temp. =", 40, 60);
  dtostrf(NTC_HET_Steinhart2, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 60);

  tft.printAt("CART temp. =", 40, 80);
  dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 80);

  tft.printAt("Heating Time =", 40, 100);

  tft.printAt("Keeping Time =", 40, 120);


  tft.setTextColor(ILI9341_WHITE, ILI9341_BLUE);
  tft.printAt(" ON ", 250, 160);

  unsigned long startTime = 0;
  unsigned long currentTime = 0;

  float deltaTime = 0;

  startTime = millis();
  // HET_SetPoint2 = 95
  while (NTC_CART_Steinhart1 < HET_SetPoint2) {
    Heater2_PID(HIGH);
    
    // showing the Heating Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 100);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart2, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    
    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 80);

    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart2);
      Serial.println(NTC_CART_Steinhart1);
    }

    if (NTC_HET_Steinhart1 >= 60) break;
  }


  startTime = millis();
  deltaTime = 0;

  while (deltaTime < iTimeMs) {   // 60000 ms = 60 sec
    Heater2_PID(HIGH);

    // showing the Cooling Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 120);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart2, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    
    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 80);

    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart2);
      Serial.println(NTC_CART_Steinhart1);
    }

    if (NTC_HET_Steinhart2 >= 100) break;
  }

  Heater2_PID(LOW);
  

if (NTC_HET_Steinhart2 >= 100) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" WARN ", 250, 160);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 160);
  }
}


void Step_THERMALCYCLE() {
    // Rotate to PLACE C
    Rotation_Angle(Rotation_C_Angle);
    
    // Heat to 55 and keep 60sec
    //Step_HEAT_55_cart(60000);
    Step_HEAT_55_1(60000);
    // Rotate to PLACE D
    Rotation_Angle(Rotation_D_Angle);

    // Heat to 95 and keep 60sec
    //Step_HEAT_95_cart(60000);
    Step_HEAT_95_2(60000);
    // Rotate to PLACE A
    Rotation_Angle(Rotation_C_Angle);

    // Heat to 55 and keep 60sec
    //Step_HEAT_55_cart(60000);
    Step_HEAT_55_1(60000);
    // Rotate to PLACE B
    Rotation_Angle(Rotation_D_Angle);

    // Heat to 95 and keep 60sec
    //Step_HEAT_95_cart(60000);
    Step_HEAT_95_2(60000);
    // Rotate to PLACE A
    Rotation_Angle(Rotation_C_Angle);

    // Heat to 55 and keep 60sec
    //Step_HEAT_55(60000);
    Step_HEAT_55_1(60000);
    // Rotate to PLACE B
    Rotation_Angle(Rotation_D_Angle);

    // Heat to 95 and keep 60sec
    //Step_HEAT_95_cart(60000);
    Step_HEAT_95_2(60000);
    // Rotate to PLACE A
    Rotation_Angle(Rotation_C_Angle);

    // Heat to 55 and keep 60sec
    //Step_HEAT_55_cart(60000);
    Step_HEAT_55_1(60000);
}


// Heat 1 only, for 75 dC
void Step_HEAT_75_1(unsigned long iTimeMs) {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STEP DOE_HEAT75", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);

  tft.printAt("1. Heat 1 = 75 C", 40, 160);

  digitalWrite(TFT_LED, HIGH);

  // Heat 1 = 55 C //
  NTC_HET_Steinhart1 = NTC_HET1_Thermistor.temperature();
  NTC_HET_Steinhart3 = NTC_HET2_Thermistor.temperature();
  NTC_ROOM_Steinhart = NTC_ROOM_Thermistor.temperature();
  NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();

  tft.printAt("Heat1 temp. =", 40, 60);
  dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 60);

  tft.printAt("Heating Time =", 40, 100);

  tft.printAt("Keeping Time =", 40, 120);

  tft.printAt("Cart. temp. =", 40, 140);
  dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
  tft.printAt(textBuff, 150, 140);


  tft.setTextColor(ILI9341_WHITE, ILI9341_BLUE);
  tft.printAt(" ON ", 250, 160);

  unsigned long startTime = 0;
  unsigned long currentTime = 0;

  float deltaTime = 0;

  startTime = millis();
  // HET_SetPoint1 = 55
  while (NTC_HET_Steinhart1 < HET_SetPoint2) {
    Heater1_PID_high(HIGH);
    //Heater3_PID(LOW);
    
    // showing the Heating Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 100);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);

    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 140);


    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart1);
      Serial.println(NTC_HET_Steinhart3);
      Serial.println(NTC_CART_Steinhart1);
    }

    if (NTC_HET_Steinhart1 >= 120) break;
  }


  startTime = millis();
  deltaTime = 0;

  while (deltaTime < iTimeMs) {   // 60000 ms = 60 sec
    Heater1_PID_high(HIGH);
    //Heater3_PID(LOW);

    // showing the Heating Time
    currentTime = millis();
    deltaTime = currentTime - startTime;
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
    dtostrf(deltaTime, 3, 1, textBuff);
    tft.printAt(textBuff, 160, 120);

    // showing the temperature
    dtostrf(NTC_HET_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 60);
    //dtostrf(NTC_HET_Steinhart3, 3, 1, textBuff);
    //tft.printAt(textBuff, 150, 80);

    NTC_CART_Steinhart1 = NTC_CART_Thermistor.temperature();
    dtostrf(NTC_CART_Steinhart1, 3, 1, textBuff);
    tft.printAt(textBuff, 150, 140);


    if (DOE_TEST_PRINT_TEMP) {  // Grail, 20221128, add for temperature records
      Serial.println(deltaTime);
      Serial.println(NTC_HET_Steinhart1);
      Serial.println(NTC_HET_Steinhart3);
      Serial.println(NTC_CART_Steinhart1);

    }

    if (NTC_HET_Steinhart1 >= 120) break;
    //if (NTC_HET_Steinhart3 >= 120) break;
  }

  Heater1_PID_high(LOW);
  //Heater3_PID(LOW);
  
if ((NTC_HET_Steinhart1 >= 120) || (NTC_HET_Steinhart3 >= 120)) {
    tft.setTextColor(ILI9341_WHITE, ILI9341_RED);
    tft.printAt(" WARN ", 250, 160);
  } else {
    tft.setTextColor(ILI9341_WHITE, ILI9341_GREEN);
    tft.printAt(" OK ", 250, 160);
  }
}



void Step_HEATERTEST() {
    // Heat1 to 75 and keep 60 sec
    Step_HEAT_75_1(60000);

    // Heat1 to 55 and keep 60 sec
    Step_HEAT_55_1(60000);

    // Heat1 to 75 and keep 60 sec
    Step_HEAT_75_1(60000);

    // Heat1 to 55 and keep 60 sec
    Step_HEAT_55_1(60000);

    // Heat1 to 75 and keep 60 sec
    Step_HEAT_75_1(60000);

    // Heat1 to 55 and keep 60 sec
    Step_HEAT_55_1(60000);
    
    // Heat1 to 75 and keep 60 sec
    Step_HEAT_75_1(60000);

    // Heat1 to 55 and keep 60 sec
    Step_HEAT_55_1(60000);

    // Heat1 to 75 and keep 60 sec
    Step_HEAT_75_1(60000);

    // Heat1 to 55 and keep 60 sec
    Step_HEAT_55_1(60000);

}



void Show_Stage() {

  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("STAGE", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);


  digitalWrite(TFT_LED, HIGH);

  tft.printAt("CURRENT_STAGE =", 40, 60);
  dtostrf(CURRENT_STAGE, 3, 0, textBuff);
  tft.printAt(textBuff, 200, 60);

}



void Show_Paras() {
  digitalWrite(TFT_LED, LOW);

  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(Arial_bold_14);

  tft.setTextScale(2);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.printAlignedOffseted("SHOW PARAs", gTextAlignMiddleCenter, 0, -90);

  tft.setTextScale(1);


  digitalWrite(TFT_LED, HIGH);

  tft.printAt("Rot_Now_Angle(steps) =", 40, 60);
  dtostrf(Rotation_Now_Angle, 3, 1, textBuff);
  tft.printAt(textBuff, 60, 80);

  tft.printAt("Linear_Now_HighZ(mm) =", 40, 100);
  dtostrf(double(Linear_Now_HighZ) / double(stepsPerMM), 3, 1, textBuff);
  tft.printAt(textBuff, 60, 120);


}


/*

// 这是Arduino的C/C++代码的简化版本，仅供参考

#include <PID_v1.h>

const int pwmPinHeater = 3;
const int pwmPinTEC = 5;
const int relayPinBFan = 7;
const int relayPinSFan = 8;

double Setpoint = 75;  // 设置目标温度
double Input = 0;      // 传感器输入
double Output = 0;     // 控制输出

PID pid(&Input, &Output, &Setpoint, 9.1, 0.3, 1.8, DIRECT);

void setup() {
  // 初始化代码
  pid.SetMode(AUTOMATIC);
  pinMode(pwmPinHeater, OUTPUT);
  pinMode(pwmPinTEC, OUTPUT);
  pinMode(relayPinBFan, OUTPUT);
  pinMode(relayPinSFan, OUTPUT);
}

void loop() {
  // 从传感器读取数据
  Input = analogRead(A0);  // 假设传感器连接到A0

  // 运行PID控制
  pid.Compute();

  // 控制加热器
  analogWrite(pwmPinHeater, Output);

  // 其他控制逻辑...
}


*/