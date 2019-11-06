#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
//#include<cmath>

RF24 radio(7,8); // CE,CSN
const byte address[6]="00001";



const int numReadings = 200;
 
int readings[numReadings];      // the readings from the analog input
int readIndex = 0;              // the index of the current reading
int total = 0;                  // the running total
int average = 0;                // the average
int avgconstant=1;
int breathein=1;

int inputPin = A3;
int ledpin = 2;

unsigned long timer;
 
void setup() {

  timer=millis();

  Serial.begin(9600);
  // initialize radio object and set address:
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
  
  // initialize all the readings to 0:
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;

   pinMode(ledpin,OUTPUT);
   digitalWrite(ledpin,LOW);
  }
}
 
void loop() {
  // subtract the last reading (only useful when wrapping to beginning):
  total = total - readings[readIndex];
  // read from the sensor:
  readings[readIndex] = analogRead(inputPin);
  // add the reading to the total:
  total = total + readings[readIndex];
  // advance to the next position in the array:
  readIndex = readIndex + 1;
 
  // if we're at the end of the array...
  if (readIndex >= numReadings) {
    // ...wrap around to the beginning:
    readIndex = 0;
  }
 
  // calculate the average:
  average = 5*(total / numReadings);
  average-=280;

  //if (average<0){
  //  average=0;
 // }

 // else {
 //   average=average*5;
 // }




  
  // send it to the computer as ASCII digits
  Serial.println(average);

  
  delay(1);        // delay in between reads for stability

  

  radio.write(&average, sizeof(average));


  
}
