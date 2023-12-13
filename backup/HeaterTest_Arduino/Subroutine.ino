// 最後編輯 2022-9-21 by ShinWei Chiou
// 初版

//------------------------------------------------------------------------------------------------
void PUMP_Valve(unsigned int iValue, unsigned int iTime)
{
  //const unsigned int Vacuum_V1_ms = 500;
  //const unsigned int Vacuum_V2_ms = 500;
  //const unsigned int Vacuum_V3_ms = 500;
  //const unsigned int Vacuum_V4_ms = 500;

  if (iValue != 0)
  {
    digitalWrite(PUMP, HIGH);
    delay(3000);
  }

  if (iValue == 1)
  {
    digitalWrite(VAL1, HIGH);
  }
  else if (iValue == 2)
  {
    digitalWrite(VAL2, HIGH);
  }
  else if (iValue == 3)
  {
    digitalWrite(VAL3, HIGH);
  }
  else if (iValue == 4)
  {
    digitalWrite(VAL4, HIGH);
  }

  delay(iTime);

  digitalWrite(VAL1, LOW);
  digitalWrite(VAL2, LOW);
  digitalWrite(VAL3, LOW);
  digitalWrite(VAL4, LOW);
  digitalWrite(PUMP, LOW);
}

//------------------------------------------------------------------------------------------------
void BLDC_Spinning_Start()
{
  // 啟動
  digitalWrite(BLDCP, HIGH);
  delay(1000);

  BLDC_PWM_ESC.write(90);
  delay(100);
}

//------------------------------------------------------------------------------------------------
/*
  BLDC_Spinning_Start();
  BLDC_Spinning_3K_10S_Cycle();
  BLDC_Spinning_3K_10S_Cycle();
  BLDC_Spinning_3K_10S_Cycle();
  BLDC_Spinning_Stop();
*/
void BLDC_Spinning_3K_10S_Cycle()
{
  for (int pos = 90; pos <= Spinning_F_3KRPM; pos += 1)
  {
    BLDC_PWM_ESC.write(pos);
    delay(50);
  }
  delay(Spinning_3KRPM_C12_ms);

  BLDC_PWM_ESC.write(0);
  delay(500);

  for (int pos = 90; pos >= Spinning_B_3KRPM; pos -= 1)
  {
    BLDC_PWM_ESC.write(pos);
    delay(50);
  }
  delay(Spinning_3KRPM_C12_ms);
  BLDC_PWM_ESC.write(90);
}

//------------------------------------------------------------------------------------------------
/*
  BLDC_Spinning_Start();
  BLDC_Spinning_3K_20S_Cycle();
  BLDC_Spinning_3K_20S_Cycle();
  BLDC_Spinning_3K_20S_Cycle();
  BLDC_Spinning_Stop();
*/
void BLDC_Spinning_3K_20S_Cycle()
{
  for (int pos = 90; pos <= Spinning_F_3KRPM; pos += 1)
  {
    BLDC_PWM_ESC.write(pos);
    delay(50);
  }
  delay(Spinning_3KRPM_C11_ms);

  BLDC_PWM_ESC.write(0);
  delay(500);

  for (int pos = 90; pos >= Spinning_B_3KRPM; pos -= 1)
  {
    BLDC_PWM_ESC.write(pos);
    delay(50);
  }
  delay(Spinning_3KRPM_C11_ms);
  BLDC_PWM_ESC.write(90);
}

//------------------------------------------------------------------------------------------------
/*
  BLDC_Spinning_Start();
  BLDC_Spinning_6K();
  for (int counter = 0; counter <= 120; counter += 1)
  {
    delay(1000);
  }
  BLDC_Spinning_Stop();
*/
void BLDC_Spinning_6K()
{
  for (int pos = 90; pos <= Spinning_F_6KRPM; pos += 1)
  {
    BLDC_PWM_ESC.write(pos);
    delay(50);
  }
}

//------------------------------------------------------------------------------------------------
/*
  BLDC_Spinning_Start();
  BLDC_Spinning_12K();
  for (int counter = 0; counter <= 120; counter += 1)
  {
    delay(1000);
  }
  BLDC_Spinning_Stop();
*/
void BLDC_Spinning_12K()
{
  for (int pos = 90; pos <= Spinning_F_12KRPM; pos += 1)
  {
    BLDC_PWM_ESC.write(pos);
    delay(50);
  }
}

//------------------------------------------------------------------------------------------------
void BLDC_Spinning_Stop()
{
  BLDC_PWM_ESC.write(90);
  delay(1000);

  // 關閉
  digitalWrite(BLDCP, LOW);
  delay(100);
}

//------------------------------------------------------------------------------------------------
void RGB_LED(unsigned int iColors)
{
  if (iColors == 0)
  {
    Pixels.clear();  // Turn OFF all pixels ASAP
  }
  else if (iColors == 1)
  {
    Pixels.setPixelColor(0, Pixels.Color(0, 0, 255));   //BLUE
    Pixels.setPixelColor(1, Pixels.Color(0, 0, 255));
  }
  else if (iColors == 2)
  {
    Pixels.setPixelColor(0, Pixels.Color(250, 100, 0)); //ORANGE
    Pixels.setPixelColor(1, Pixels.Color(250, 100, 0));
  }
  else if (iColors == 3)
  {
    Pixels.setPixelColor(0, Pixels.Color(0, 255, 0));   //GREEN
    Pixels.setPixelColor(1, Pixels.Color(0, 255, 0));
  }
  else if (iColors == 4)
  {
    Pixels.setPixelColor(0, Pixels.Color(255, 0, 0));   //RED
    Pixels.setPixelColor(1, Pixels.Color(255, 0, 0));
  }

  Pixels.show(); // This sends the updated pixel color to the hardware.
}

//------------------------------------------------------------------------------------------------
void Cooler_PID(boolean iOnOff)
{
  float pid_PID;
  unsigned int TEC_PWM_Value;

  // 偵測溫度
  NTC_TEC_Steinhart = NTC_TEC_Thermistor.temperature();
  NTC_FAN_Steinhart = NTC_FAN_Thermistor.temperature();
  NTC_ROOM_Steinhart = NTC_ROOM_Thermistor.temperature();

  /*
    Serial.print(NTC_TEC_Steinhart);
    Serial.print(" , ");
    Serial.print(NTC_FAN_Steinhart);
    Serial.print(" , ");
    Serial.println(NTC_ROOM_Steinhart);
  */

  // 計算 PID 數值
  pid_PID = TEC_PID.Run(NTC_TEC_Steinhart);
  TEC_PWM_Value = map(pid_PID, 0, 255, 0, 255);

  // 驅動散熱器 & 致冷器 MOSFET
  if (iOnOff == HIGH)
  {
    digitalWrite(FAN, HIGH);
    analogWrite(TEC, TEC_PWM_Value);
  }
  else
  {
    analogWrite(TEC, 0);
    digitalWrite(FAN, LOW);
  }
}

//------------------------------------------------------------------------------------------------
void Heater_PID(boolean iOnOff)
{
  float pid_PID;
  unsigned int HET_PWM_Value1, HET_PWM_Value2, HET_PWM_Value3, HET_PWM_Value4;

  // 偵測加熱器溫度
  NTC_HET_Steinhart1 = NTC_HET1_Thermistor.temperature();
  NTC_HET_Steinhart2 = NTC_HET2_Thermistor.temperature();
  NTC_HET_Steinhart3 = NTC_HET3_Thermistor.temperature();
  NTC_HET_Steinhart4 = NTC_HET4_Thermistor.temperature();

  /*
    Serial.print(NTC_HET_Steinhart1);
    Serial.print(" , ");
    Serial.print(NTC_HET_Steinhart2);
    Serial.print(" , ");
    Serial.print(NTC_HET_Steinhart3);
    Serial.print(" , ");
    Serial.println(NTC_HET_Steinhart4);
  */

  // 計算 PID 數值
  pid_PID = HET_PID1.Run(NTC_HET_Steinhart1);
  HET_PWM_Value1 = map(pid_PID, 0, 255, 0, 255);

  pid_PID = HET_PID2.Run(NTC_HET_Steinhart2);
  HET_PWM_Value2 = map(pid_PID, 0, 255, 0, 255);

  pid_PID = HET_PID3.Run(NTC_HET_Steinhart3);
  HET_PWM_Value3 = map(pid_PID, 0, 255, 0, 255);

  pid_PID = HET_PID4.Run(NTC_HET_Steinhart4);
  HET_PWM_Value4 = map(pid_PID, 0, 255, 0, 255);

  // 驅動加熱器 MOSFET
  if (iOnOff == HIGH)
  {
    analogWrite(HET1, HET_PWM_Value1);
    analogWrite(HET2, HET_PWM_Value2);
    analogWrite(HET3, HET_PWM_Value3);
    analogWrite(HET4, HET_PWM_Value4);
  }
  else
  {
    analogWrite(HET1, 0);
    analogWrite(HET2, 0);
    analogWrite(HET3, 0);
    analogWrite(HET4, 0);
  }
}
//------------------------------------------------------------------------------------------------
// Grail, 20221129, Heaters seperatly
// bTempHigh = true means 95
// bTempHigh = false means 55
void Heater1_PID(boolean iOnOff)
{
  float pid_PID;
  unsigned int HET_PWM_Value1;

  // 偵測加熱器溫度
  NTC_HET_Steinhart1 = NTC_HET1_Thermistor.temperature();

  /*
    Serial.print(NTC_HET_Steinhart1);
  */

  // 計算 PID 數值
  pid_PID = HET_PID1.Run(NTC_HET_Steinhart1);

  HET_PWM_Value1 = map(pid_PID, 0, 255, 0, 255);

  // 驅動加熱器 MOSFET
  if (iOnOff == HIGH)
  {
    analogWrite(HET1, HET_PWM_Value1);
  }
  else
  {
    analogWrite(HET1, 0);
  }
}
void Heater2_PID(boolean iOnOff)
{
  float pid_PID;
  unsigned int HET_PWM_Value2;

  // 偵測加熱器溫度
  NTC_HET_Steinhart2 = NTC_HET2_Thermistor.temperature();

  /*
    Serial.print(NTC_HET_Steinhart2);
  */

  // 計算 PID 數值
  pid_PID = HET_PID2.Run(NTC_HET_Steinhart2);
  HET_PWM_Value2 = map(pid_PID, 0, 255, 0, 255);

  // 驅動加熱器 MOSFET
  if (iOnOff == HIGH)
  {
    analogWrite(HET2, HET_PWM_Value2);
  }
  else
  {
    analogWrite(HET2, 0);
  }
}
void Heater3_PID(boolean iOnOff)
{
  float pid_PID;
  unsigned int HET_PWM_Value3;

  // 偵測加熱器溫度
  NTC_HET_Steinhart3 = NTC_HET3_Thermistor.temperature();

  /*
    Serial.print(NTC_HET_Steinhart3);
  */

  // 計算 PID 數值
  pid_PID = HET_PID3.Run(NTC_HET_Steinhart3);
  HET_PWM_Value3 = map(pid_PID, 0, 255, 0, 255);

  // 驅動加熱器 MOSFET
  if (iOnOff == HIGH)
  {
    analogWrite(HET3, HET_PWM_Value3);
  }
  else
  {
    analogWrite(HET3, 0);
  }
}
void Heater4_PID(boolean iOnOff)
{
  float pid_PID;
  unsigned int HET_PWM_Value4;

  // 偵測加熱器溫度
  NTC_HET_Steinhart4 = NTC_HET4_Thermistor.temperature();

  /*
    Serial.print(NTC_HET_Steinhart4);
  */

  // 計算 PID 數值
  pid_PID = HET_PID4.Run(NTC_HET_Steinhart4);
  HET_PWM_Value4 = map(pid_PID, 0, 255, 0, 255);

  // 驅動加熱器 MOSFET
  if (iOnOff == HIGH)
  {
    analogWrite(HET4, HET_PWM_Value4);
  }
  else
  {
    analogWrite(HET4, 0);
  }
}

void Heater1_PID_high(boolean iOnOff)
{
  float pid_PID;
  unsigned int HET_PWM_Value1;

  // 偵測加熱器溫度
  NTC_HET_Steinhart1 = NTC_HET1_Thermistor.temperature();

  /*
    Serial.print(NTC_HET_Steinhart1);
  */

  // 計算 PID 數值
  pid_PID = HET_PID2.Run(NTC_HET_Steinhart1);

  HET_PWM_Value1 = map(pid_PID, 0, 255, 0, 255);

  // 驅動加熱器 MOSFET
  if (iOnOff == HIGH)
  {
    analogWrite(HET1, HET_PWM_Value1);
  }
  else
  {
    analogWrite(HET1, 0);
  }
}


//------------------------------------------------------------------------------------------------
void Linear_HighZ(unsigned int IndexHighZ_01mm)
{
  //return;
  // 1 IndexHighZ = 0.1mm
  // 1 mm = 1024 steps
  // 0.1 mm = 102.4 steps
  uint16_t i;
  unsigned int IndexHighZ = 0;   // steps
  
  float count_step = 0.0;
  count_step = float(IndexHighZ_01mm) * float(stepsPerMM) * 0.1;

  if (IndexHighZ_01mm > 100) 
  {
    count_step = 10240;
  }
    
  IndexHighZ = floor(count_step);
  
  //IndexHighZ = IndexHighZ_01mm;
  //int Linear_Now_HighZ_step = 0;  // = Linear_Now_HighZ


  // 回至歸零點
  if (IndexHighZ == 0 && Linear_Now_HighZ == -1)
  {
    Linear_Now_HighZ = 0;
    /*
    i = 0;
    while (digitalRead(LSW3) == 1)
    {
      StepperMotor_Linear.step(1);
      if (i >= 10240) {
        Linear_HighZ_Error = HIGH;
        break;
      } else {
        Linear_Now_HighZ = 0;
        i++;
      }
    }
    */
  }
  // 轉至高度 IndexHighZ
  else
  {
    if (IndexHighZ > Linear_Now_HighZ)
    {
      Linear_Now_HighZ = IndexHighZ - Linear_Now_HighZ;

      /*
      for (int i = 0; i < Linear_Now_HighZ; i += 1)
      {
        StepperMotor_Linear.step(-1);
      }
      */
      StepperMotor_Linear.step((-1)*Linear_Now_HighZ);
      Linear_Now_HighZ = IndexHighZ;
    }
    else if (IndexHighZ < Linear_Now_HighZ)
    {
      Linear_Now_HighZ = Linear_Now_HighZ - IndexHighZ;
      /*
      for (int i = 0; i < Linear_Now_HighZ; i += 1)
      {
        StepperMotor_Linear.step(1);
      }
      */
      StepperMotor_Linear.step(Linear_Now_HighZ);

      Linear_Now_HighZ = IndexHighZ;
    }
    // if IndexHighZ == Linear_Now_HighZ, no need to move
  }

  // 解除停止 Linear Stepper Motor
  StepperMotor_Linear_Stop();
}

//------------------------------------------------------------------------------------------------
void Rotation_Angle(unsigned int IndexAngle_1d)
{
  // Grail, 20221227, 360degree = 3040 steps (IndexAngle)
  // IndexAngle should be between 0-3040 (in fact, < 2994, to avoid stucked) 
  // 回至歸零點
  // Grail, 20230207, use degree as input (instead of steps)
  // 1 IndexAngle_1d = 1 degree
  // 360 degrees = 3040 steps
  // 1 mm = 8.444 steps
  uint16_t i;
  unsigned int IndexAngle = 0;   // steps
  
  float count_step = 0.0;
  count_step = float(IndexAngle_1d) * float(stepsPer360Deg) / float(360);

  if (IndexAngle_1d > 351) 
  {
    count_step = 2964;
  }
    
  IndexAngle = floor(count_step);

  if (IndexAngle == 0)
  {
    i = 0;
    while (digitalRead(LSW4) == 1)
    {
      StepperMotor_Rotation.moveDegrees (moveanticlockwise, 1);
      if (i >= 3600) {
        Rotation_Angle_Error = HIGH;
        break;
      } else {
        Rotation_Angle_Error = LOW;
        Rotation_Now_Angle = 0;
        i++;
      }
    }
  }

  // 轉至角度
  else
  {
    if (IndexAngle > Rotation_Now_Angle)
    {
      Rotation_Now_Angle = IndexAngle - Rotation_Now_Angle;

      for (int i = 0; i < Rotation_Now_Angle; i += 1)
      {
        StepperMotor_Rotation.moveDegrees (moveClockwise, 1);
      }

      Rotation_Now_Angle = IndexAngle;

      /* Grail, 20221226, trying to find limitation of the rotation, have some side effect */
      /*      
      for (i = 0; i < 100; i += 1)
      {
        StepperMotor_Rotation.moveDegrees (moveClockwise, 1);
      }

      while (digitalRead(LSW4) == 1)
      {
        StepperMotor_Rotation.moveDegrees (moveClockwise, 1);        
        if (i >= Rotation_Now_Angle)
        {
          Rotation_Now_Angle = IndexAngle;
          i = 0;
          break;
        } else {
          i += 1;
        }
      }
      if (i != 0) {
        Rotation_Now_Angle = IndexAngle + i - Rotation_Now_Angle;
        Rotation_Angle_Error = HIGH;       
      }
      */
    }
    else if (IndexAngle < Rotation_Now_Angle)
    {
      Rotation_Now_Angle = Rotation_Now_Angle - IndexAngle;

      for (int i = 0; i < Rotation_Now_Angle; i += 1)
      {
        StepperMotor_Rotation.moveDegrees (moveanticlockwise, 1);
      }

      Rotation_Now_Angle = IndexAngle;

      /* Grail, 20221226, trying to find limitation of the rotation, have some side effect */
      /*
      for (i = 0; i < 100; i += 1)
      {
        StepperMotor_Rotation.moveDegrees (moveanticlockwise, 1);
      }

      while (digitalRead(LSW4) == 1)
      {
        StepperMotor_Rotation.moveDegrees (moveanticlockwise, 1);        
        if (i >= Rotation_Now_Angle)
        {
          Rotation_Now_Angle = IndexAngle;
          i = 0;
          break;
        } else {
          i += 1;
        }
      }
      if (i != 0) {
        Rotation_Now_Angle = IndexAngle - i + Rotation_Now_Angle;
        Rotation_Angle_Error = HIGH;       
      }
      */
    }
  }

  // 解除停止 Rotation Stepper Motor
  StepperMotor_Rotation_Stop();
}

//------------------------------------------------------------------------------------------------
void Drawer_Open()
{
  uint16_t i;

  // 啟動 Drawer Stepper Motor
  i = 0;
  while (digitalRead(LSW1) == 0)
  {
    StepperMotor_Drawer.moveDegrees (moveClockwise, 1);

    if (i >= 1400) {
      Drawer_Open_Error = HIGH;
      break;
    } else {
      i++;
    }
  }

  // 解除停止 Drawer Stepper Motor
  StepperMotor_Drawer_Stop();
  Drawer_Open_State = HIGH;
}

//------------------------------------------------------------------------------------------------
void Drawer_Close()
{
  uint16_t i;

  // 啟動 Drawer Stepper Motor
  i = 0;
  while (digitalRead(LSW2) == 1)
  {
    StepperMotor_Drawer.moveDegrees (moveanticlockwise, 1);

    if (i >= 1400) {
      Drawer_Close_Error = HIGH;
      break;
    } else {
      i++;
    }
  }

  // 解除停止 Drawer Stepper Motor
  StepperMotor_Drawer_Stop();
  Drawer_Open_State = LOW;
}

//------------------------------------------------------------------------------------------------
void Clutch_None_Engage()
{
  //return;

  if (digitalRead(LSW5) == 0)
  {
    StepperMotor_Clutch.moveDegrees (moveanticlockwise, 90);
    StepperMotor_Clutch_Stop();
  }
}

//------------------------------------------------------------------------------------------------
void Rotation_TX_Angle_Align()
{
  return;
  
  uint16_t i;

  // 先停止 BLDC 轉動
  BLDC_Spinning_Stop();


  delay(500);


  // 脫離 Clutch Engage
  if (digitalRead(LSW5) == 0)
  {
    StepperMotor_Clutch.moveDegrees (moveanticlockwise, 90);
    StepperMotor_Clutch_Stop();
  }

  // 接合 Clutch Engage
  i = 0;
  while (digitalRead(LSW5) == 1)
  {
    StepperMotor_Clutch.moveDegrees (moveClockwise, 1);

    if (i >= 200) {
      Clutch_Engage_Error = HIGH;
      break;
    } else {
      i++;
    }
  }

  // 解除停止 Clutch Stepper Motor
  StepperMotor_Clutch_Stop();


  delay(500);


  // 對齊 TX Align
  i = 0;
  while (digitalRead(ENC0) == 0 || digitalRead(ENC1) == 0)
  {
    StepperMotor_Positioning.moveDegrees (moveClockwise, 1);

    if (i >= 800) {
      Rotation_TX_Angle_Align_Error = HIGH;
      break;
    } else {
      i++;
    }
  }

  // 解除停止 Positioning Stepper Motor
  StepperMotor_Positioning_Stop();
}

//------------------------------------------------------------------------------------------------
/*
  if (Button_OnOff_Press == HIGH)
  {
    Button_OnOff_Press = LOW;
    ButtonLED_Standby_Mode();
  }
*/
void Button_Press()
{
  if (digitalRead(PB1) == 0)
  {
    delay(20);
    while (digitalRead(PB1) == 0)
    {
      Button_OnOff_Press = HIGH;
    }
  }

  if (digitalRead(PB2) == 0)
  {
    delay(20);
    while (digitalRead(PB2) == 0)
    {
      Button_OpenClose_Press = HIGH;
    }
  }

  if (digitalRead(PB3) == 0)
  {
    delay(20);
    while (digitalRead(PB3) == 0)
    {
      Button_StartStop_Press = HIGH;
    }
  }
}

//------------------------------------------------------------------------------------------------
/*
  for (int i = 0; i < 20; i += 1)
  {
    ButtonLED_Power_ON_OFF();
    delay(200);
  }
*/
void ButtonLED_ACPower_Connected()
{
  digitalWrite(LED1B, LOW);
  digitalWrite(LED2B, LOW);
  digitalWrite(LED3B, LOW);
  digitalWrite(LED1R, HIGH);
  digitalWrite(LED2R, LOW);
  digitalWrite(LED3R, LOW);
}

void ButtonLED_Power_ON_OFF()       // Button_LedState = 1;
{
  digitalWrite(LED1R, LOW);
  digitalWrite(LED2R, LOW);
  digitalWrite(LED3R, LOW);

  LedState = ! LedState;
  digitalWrite(LED1B, LedState);

  digitalWrite(LED2B, HIGH);
  digitalWrite(LED3B, HIGH);
}

void ButtonLED_Standby_Mode()
{
  digitalWrite(LED1R, LOW);
  digitalWrite(LED2R, LOW);
  digitalWrite(LED3R, LOW);
  digitalWrite(LED1B, HIGH);
  digitalWrite(LED2B, HIGH);
  digitalWrite(LED3B, HIGH);
}

void ButtonLED_Drawer_OpenClose()  // Button_LedState = 2;
{
  digitalWrite(LED1R, LOW);
  digitalWrite(LED2R, LOW);
  digitalWrite(LED3R, LOW);
  digitalWrite(LED1B, HIGH);

  LedState = ! LedState;
  digitalWrite(LED2B, LedState);

  digitalWrite(LED3B, HIGH);
}

void ButtonLED_Processing()       // Button_LedState = 3;
{
  digitalWrite(LED1R, LOW);
  digitalWrite(LED2R, LOW);
  digitalWrite(LED3R, LOW);
  digitalWrite(LED1B, HIGH);
  digitalWrite(LED2B, HIGH);

  LedState = ! LedState;
  digitalWrite(LED3B, LedState);
}

void ButtonLED_Error()            // Button_LedState = 4;
{
  digitalWrite(LED1B, LOW);
  digitalWrite(LED2B, LOW);
  digitalWrite(LED3B, LOW);

  LedState = ! LedState;
  digitalWrite(LED1R, LedState);
  digitalWrite(LED2R, LedState);
  digitalWrite(LED3R, LedState);
}

//------------------------------------------------------------------------------------------------
void StepperMotor_Linear_Stop()
{
  //StepperMotor_Linear.stop();
  digitalWrite(STM11, LOW);
  digitalWrite(STM12, LOW);
  digitalWrite(STM13, LOW);
  digitalWrite(STM14, LOW);
}

void StepperMotor_Rotation_Stop()
{
  StepperMotor_Rotation.stop();
  digitalWrite(STM21, LOW);
  digitalWrite(STM22, LOW);
  digitalWrite(STM23, LOW);
  digitalWrite(STM24, LOW);
}

void StepperMotor_Drawer_Stop()
{
  StepperMotor_Drawer.stop();
  digitalWrite(STM31, LOW);
  digitalWrite(STM32, LOW);
  digitalWrite(STM33, LOW);
  digitalWrite(STM34, LOW);
}

void StepperMotor_Clutch_Stop()
{
  StepperMotor_Clutch.stop();
  digitalWrite(STM41, LOW);
  digitalWrite(STM42, LOW);
  digitalWrite(STM43, LOW);
  digitalWrite(STM44, LOW);
}

void StepperMotor_Positioning_Stop()
{
  StepperMotor_Positioning.stop();
  digitalWrite(STM51, LOW);
  digitalWrite(STM52, LOW);
  digitalWrite(STM53, LOW);
  digitalWrite(STM54, LOW);
}
