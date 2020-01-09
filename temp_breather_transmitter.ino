#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <OneWire.h> 
#include <DallasTemperature.h>
/********************************************************************/
// Data wire is plugged into pin 2 on the Arduino 
#define ONE_WIRE_BUS 2 
/********************************************************************/
// Setup a oneWire instance to communicate with any OneWire devices  
// (not just Maxim/Dallas temperature ICs) 
OneWire oneWire(ONE_WIRE_BUS); 
/********************************************************************/
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

RF24 radio(7,8); // CE,CSN
const byte address[6]="00001";

float temp;
 
void setup() {


  Serial.begin(9600);
  // initialize radio object and set address:
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
  
  sensors.begin();
  sensors.setResolution(10);
}
 
void loop() {
 

  sensors.requestTemperatures();

  temp=sensors.getTempCByIndex(0);

  radio.write(&temp, sizeof(temp));

  delay(1);


  
}
