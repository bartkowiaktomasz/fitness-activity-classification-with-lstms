//#include <unwind-cxx.h>
#include <ArduinoSTL.h>
#include <system_configuration.h>

//#include <unwind-cxx.h>
//#include <StandardCplusplus.h>
//#include <utility.h>
//#include <system_configuration.h>

#include "keras_model.h"
#include "utils.h"

#include "quaternionFilters.h"
#include "MPU9250.h"
#include <string>
#include <SimbleeBLE.h>
#include <Wire.h>
#include <SPI.h>

#define AHRS true         // Set to false for basic data read
#define SerialDebug true  // Set to true to get Serial output for debugging

char data[32];

// Pin definitions
int intPin = 12;  // These can be changed, 2 and 3 are the Arduinos ext int pins
int myLed  = 13;  // Set up pin 13 led for toggling
int counter = 0;

int SEGMENT_TIME_SIZE = 40;
int N_FEATURES = 3;

MPU9250 myIMU;
Tensor data_tensor(SEGMENT_TIME_SIZE, N_FEATURES);
KerasModel model;

void setup()
{
  Wire.begin();
  // TWBR = 12;  // 400 kbit/sec I2C speed
  Serial.begin(9600);

  // Set up the interrupt pin, its set as active high, push-pull
  pinMode(intPin, INPUT);
  digitalWrite(intPin, LOW);
  pinMode(myLed, OUTPUT);
  digitalWrite(myLed, HIGH);

  // Read the WHO_AM_I register, this is a good test of communication
  byte c = myIMU.readByte(MPU9250_ADDRESS, WHO_AM_I_MPU9250);
  Serial.print("MPU9250 "); Serial.print("I AM "); Serial.print(c, HEX);
  Serial.print(" I should be "); Serial.println(0x71, HEX);

  if (c == 0x71) // WHO_AM_I should always be 0x71
  {
    Serial.println("MPU9250 is online...");

    // Start by performing self test and reporting values
    myIMU.MPU9250SelfTest(myIMU.SelfTest);
    Serial.print("x-axis self test: acceleration trim within : ");
    Serial.print(myIMU.SelfTest[0],1); Serial.println("% of factory value");
    Serial.print("y-axis self test: acceleration trim within : ");
    Serial.print(myIMU.SelfTest[1],1); Serial.println("% of factory value");
    Serial.print("z-axis self test: acceleration trim within : ");
    Serial.print(myIMU.SelfTest[2],1); Serial.println("% of factory value");
    Serial.print("x-axis self test: gyration trim within : ");
    Serial.print(myIMU.SelfTest[3],1); Serial.println("% of factory value");
    Serial.print("y-axis self test: gyration trim within : ");
    Serial.print(myIMU.SelfTest[4],1); Serial.println("% of factory value");
    Serial.print("z-axis self test: gyration trim within : ");
    Serial.print(myIMU.SelfTest[5],1); Serial.println("% of factory value");

    // Calibrate gyro and accelerometers, load biases in bias registers
    myIMU.calibrateMPU9250(myIMU.gyroBias, myIMU.accelBias);

    myIMU.initMPU9250();
    // Initialize device for active mode read of acclerometer, gyroscope, and
    // temperature
    Serial.println("MPU9250 initialized for active data mode....");

    // Read the WHO_AM_I register of the magnetometer, this is a good test of
    // communication
    byte d = myIMU.readByte(AK8963_ADDRESS, WHO_AM_I_AK8963);
    Serial.print("AK8963 "); Serial.print("I AM "); Serial.print(d, HEX);
    Serial.print(" I should be "); Serial.println(0x48, HEX);

    // Get magnetometer calibration from AK8963 ROM
    myIMU.initAK8963(myIMU.magCalibration);
    
    // Initialize device for active mode read of magnetometer
    Serial.println("AK8963 initialized for active data mode....");
    
    if (SerialDebug)
    {
      //  Serial.println("Calibration values: ");
      Serial.print("X-Axis sensitivity adjustment value ");
      Serial.println(myIMU.magCalibration[0], 2);
      Serial.print("Y-Axis sensitivity adjustment value ");
      Serial.println(myIMU.magCalibration[1], 2);
      Serial.print("Z-Axis sensitivity adjustment value ");
      Serial.println(myIMU.magCalibration[2], 2);
    }

  } // if (c == 0x71)
  else
  {
    Serial.print("Could not connect to MPU9250: 0x");
    Serial.println(c, HEX);
    while(1) ; // Loop forever if communication doesn't happen
  }

  SimbleeBLE.advertisementData = "MPU9250";
  SimbleeBLE.deviceName = "IMU";

  // start the BLE stack
  SimbleeBLE.begin();

  model.LoadModel();
}

void loop()
{
  // If intPin goes high, all data registers have new data
  // On interrupt, check if data ready interrupt
  if (myIMU.readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01)
  {  
    myIMU.readAccelData(myIMU.accelCount);  // Read the x/y/z adc values
    myIMU.getAres();

    // Now we'll calculate the accleration value into actual g's
    // This depends on scale being set
    myIMU.ax = (float)myIMU.accelCount[0]*myIMU.aRes; // - accelBias[0];
    myIMU.ay = (float)myIMU.accelCount[1]*myIMU.aRes; // - accelBias[1];
    myIMU.az = (float)myIMU.accelCount[2]*myIMU.aRes; // - accelBias[2];

    myIMU.readGyroData(myIMU.gyroCount);  // Read the x/y/z adc values
    myIMU.getGres();

    // Calculate the gyro value into actual degrees per second
    // This depends on scale being set
    myIMU.gx = (float)myIMU.gyroCount[0]*myIMU.gRes;
    myIMU.gy = (float)myIMU.gyroCount[1]*myIMU.gRes;
    myIMU.gz = (float)myIMU.gyroCount[2]*myIMU.gRes;

    myIMU.readMagData(myIMU.magCount);  // Read the x/y/z adc values
    myIMU.getMres();
    // User environmental x-axis correction in milliGauss, should be
    // automatically calculated
    myIMU.magbias[0] = +470.;
    // User environmental x-axis correction in milliGauss TODO axis??
    myIMU.magbias[1] = +120.;
    // User environmental x-axis correction in milliGauss
    myIMU.magbias[2] = +125.;

    // Calculate the magnetometer values in milliGauss
    // Include factory calibration per data sheet and user environmental
    // corrections
    // Get actual magnetometer value, this depends on scale being set
    myIMU.mx = (float)myIMU.magCount[0]*myIMU.mRes*myIMU.magCalibration[0] -
               myIMU.magbias[0];
    myIMU.my = (float)myIMU.magCount[1]*myIMU.mRes*myIMU.magCalibration[1] -
               myIMU.magbias[1];
    myIMU.mz = (float)myIMU.magCount[2]*myIMU.mRes*myIMU.magCalibration[2] -
               myIMU.magbias[2];
  } // if (readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01)

  // Must be called before updating quaternions!
  myIMU.updateTime();
  MahonyQuaternionUpdate(myIMU.ax, myIMU.ay, myIMU.az, myIMU.gx*DEG_TO_RAD,
                         myIMU.gy*DEG_TO_RAD, myIMU.gz*DEG_TO_RAD, myIMU.my,
                         myIMU.mx, myIMU.mz, myIMU.deltat);

  
    // Serial print and/or display at 0.5 s rate independent of data rates
    myIMU.delt_t = millis() - myIMU.count;
    
    int16_t ax, ay, az;
    int16_t gx, gy, gz;
    int16_t mx, my, mz;

    // update LCD once per half-second independent of read rate
    if (myIMU.delt_t > 500)
    {
      if(SerialDebug)
      { 
        // Acceleration is given in "mg" after multiplying by 1000
        // The order is ax, ay, az
        ax = (float)1000*myIMU.ax;
        ay = (float)1000*myIMU.ay;
        az = (float)1000*myIMU.az;

        // Unit is deg/s but after multiplying by 100 it is hdeg/s
        gx = (float)100*myIMU.gx;
        gy = (float)100*myIMU.gy;
        gz = (float)100*myIMU.gz;

        // Unit is deg/s
        mx = (float)myIMU.mx;
        my = (float)myIMU.my;
        mz = (float)myIMU.mz;

        data_tensor.data_ ={-14.44,  -1.68,  -2.40,
                            -14.44,  -1.68,  -2.40,
                            -14.63,   3.36,  -2.35,
                            -14.63,   3.36,  -2.35,
                            -14.63,   3.36,  -2.35,
                             -8.21,   1.66,  -6.38,
                             -8.21,   1.66,  -6.38,
                             -2.88,  -0.87,  -4.96,
                             -2.88,  -0.87,  -4.96,
                             -2.88,  -0.87,  -4.96,
                             -2.88,  -0.87,  -4.96,
                             -1.91,  -4.10,  -3.47,
                             -1.91,  -4.10,  -3.47,
                             -1.91,  -4.10,  -3.47,
                             -7.67,   2.92,  -5.25,
                             -7.67,   2.92,  -5.25,
                             -7.67,   2.92,  -5.25,
                            -20.00,  19.99, -12.99,
                            -20.00,  19.99, -12.99,
                            -20.00,  19.99, -12.99,
                            -20.00,  19.99, -16.21,
                            -20.00,  19.99, -16.21,
                             -7.29,   0.82,  -4.27,
                             -7.29,   0.82,  -4.27,
                             -7.29,   0.82,  -4.27,
                             -4.09,  -1.87,  -4.49,
                             -4.09,  -1.87,  -4.49,
                             -5.97,  -1.87,  -3.6 ,
                             -5.97,  -1.87,  -3.6 ,
                             -5.97,  -1.87,  -3.6 ,
                             -0.83,  -5.19,  -3.81,
                             -0.83,  -5.19,  -3.81,
                             -0.83,  -5.19,  -3.81,
                            -20.00,  18.28, -10.44,
                            -20.00,  18.28, -10.44,
                            -20.00,  18.28, -10.44,
                            -20.00,  16.40, -14.51,
                            -20.00,  16.40, -14.51,
                            -20.00,  16.40, -14.51,
                             -3.55,  -2.53,  -3.92};
                             
        Tensor output;
        model.Apply(&data_tensor, &output);
        const char* activity = softmax_to_label(output.data_).c_str();
        
        Serial.print(activity);
         
        /*
        Serial.print(ax);
        Serial.print(" ");
        Serial.print(ay);
        Serial.print(" ");
        Serial.print(az);
        Serial.print(" ");

        // Gyro measurements are given in "deg/s"
        // The order is gx, gy, gz
        Serial.print( myIMU.gx, 2);
        Serial.print(" ");
        Serial.print( myIMU.gy, 2);
        Serial.print(" ");
        Serial.print( myIMU.gz, 2);
        Serial.print(" ");

        // Magnetometer measurements are given in "mG"
        // The order is mx, my, mz
        Serial.print( (int)myIMU.mx );
        Serial.print(" ");
        Serial.print( (int)myIMU.my );
        Serial.print(" ");
        Serial.print( (int)myIMU.mz );
        Serial.println();
        */
      }

      int DATA_SIZE = 2;
      memcpy(data, &ax, sizeof(ax));
      memcpy(data + 1 * DATA_SIZE, &ay, sizeof(ay));
      memcpy(data + 2 * DATA_SIZE, &az, sizeof(az));
      memcpy(data + 3 * DATA_SIZE, &gx, sizeof(gx));
      memcpy(data + 4 * DATA_SIZE, &gy, sizeof(gy));
      memcpy(data + 5 * DATA_SIZE, &gz, sizeof(gz));
      memcpy(data + 6 * DATA_SIZE, &mx, sizeof(mx));
      memcpy(data + 7 * DATA_SIZE, &my, sizeof(my));
      memcpy(data + 8 * DATA_SIZE, &mz, sizeof(mz));
      
      SimbleeBLE.send(data, sizeof(data));

      myIMU.count = millis();
      myIMU.sumCount = 0;
      myIMU.sum = 0;

    }
}

