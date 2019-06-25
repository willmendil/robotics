// python-build-start
// action, upload
// board, arduino:avr:mega:cpu=atmega2560
// port, /dev/ttyACM0
// ide, 1.8.9
// python-build-end

#include <Servo.h>
#include <stdlib.h>
#include <stdio.h>
Servo servo_H;  // create servo object to control a servo
Servo servo_V;

// SERIAL INIT COMM. PYTHON : FORMAT XCCVVVE
char inputCharSerial[7];
bool stringComplete = false;
String command_code = "";
int command_value = 0;
int i = 0;
// PIN INIT
int LeftEnA = 7;
int LeftIn1 = 23;
int LeftIn2 = 25;

int RightEnB = 6;
int RightIn3 = 29;
int RightIn4 = 27;

int servo_H_PO = 4;
int servo_V_PO = 5;

// Global variables
int servo_pos = 0;
int servo_H_pos = 90;
int servo_V_pos = 90;
int servo_H_min = 10;
int servo_H_max = 165;
int servo_V_min = 15;
int servo_V_max = 145;

void setup(){
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(LeftEnA, OUTPUT);
  pinMode(LeftIn1, OUTPUT);
  pinMode(LeftIn2, OUTPUT);


  pinMode(RightEnB, OUTPUT);
  pinMode(RightIn3, OUTPUT);
  pinMode(RightIn4, OUTPUT);

  servo_H.attach(servo_H_PO);
  servo_V.attach(servo_V_PO);
  servo_H.write(servo_H_pos);  //min = 10 : max = 170
  servo_V.write(servo_V_pos);  //min = 15 : max = 150


}


int servoVUp(int value) {
	if(value <= servo_V_pos) {
		for (servo_pos = servo_V_pos; servo_pos >= value; servo_pos -= 1) {	// goes from 0 degrees to 180 degrees
			// in steps of 1 degree
      servo_V_pos = servo_pos;
			servo_V.write(servo_pos);              // tell servo to go to position in variable 'pos'
			//servo_V.write(servo_pos);              // tell servo to go to position in variable 'pos'
			delay(5);                       // waits 15ms for the servo to reach the position
		}

	}
	else if (value > servo_V_pos) {
		for (servo_pos = servo_V_pos; servo_pos <= value; servo_pos += 1) {	// goes from 0 degrees to 180 degrees
			// in steps of 1 degree
      servo_V_pos = servo_pos;
      //servo_H.write(servo_pos);              // tell servo to go to position in variable 'pos'
			servo_V.write(servo_pos);              // tell servo to go to position in variable 'pos'
			delay(5);                       // waits 15ms for the servo to reach the position
		}

	}

}


void processControl(String input, int value){

//  int value = map(rawvalue, 0, 170,0,120);
  // Serial.println(value);
   if (input == "df"){
     DcForward(value);
   }
   else if (input == "db"){
     DcBackward(value);
   }
   else if (input == "dl"){
     DcRotLeft(value);
   }
   else if (input == "dr"){
     DcRotRight(value);
   }
   else if (input == "sp"){
     DcStop();
   }
   else if (input == "gf"){
     int mappedValue = map(value, 0, 170,90,servo_V_max);
     servoVUp(mappedValue);
   }
   else if (input == "gb"){
     int mappedValue = map(value, 0, 170,servo_V_min,90);
     servoVUp(mappedValue);
   }

}

int digitToInt(char* d){
  char charToInt[4];
  for (int j = 0; j <=2; j++){
    charToInt[j] = d[j];
  }
  charToInt[3] = '\0';
  return (int) strtol(charToInt, NULL, 10);

}

void loop(){

  // if(stringComplete){
  //   // Serial.print(inputCharSerial);
  //   if (inputCharSerial[0] == 'A'){
  //     char bufferValue[3];
  //     for (int j = 0; j <= 1 ; j++){
  //       command_code += inputCharSerial[j+1];
  //     }
  //     for (int i = 0; i <= 2 ; i++){
  //       bufferValue[i] = inputCharSerial[i+3];
  //     }
  //     command_value = digitToInt(bufferValue);
  //   }
  //   else if (inputCharSerial[0] == 'B'){
  //     for (int j = 0; j<= 1 ; j++){
  //       command_code += inputCharSerial[j+1];
  //       command_value = 0;
  //     }
  //   }
  //   else {
  //     DcStop();
  //   }
  //
  //   Serial.print("INPUT : ");
  //   Serial.print(command_code);
  //   Serial.print("     VALUE : ");
  //   Serial.print (command_value);
  //   Serial.print("      ");
  //   Serial.println(i);
  //   i = i + 1;
  //   processControl(command_code, command_value);
  //
  //   memset (inputCharSerial, 0, 7);
  //   stringComplete = false;
  //   command_code = "";
  //   command_value = 0;
  // }

  recvWithStartEndMarkers();
  showNewData();
}


// Example 3 - Receive with start- and end-markers

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;


void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '\x01';
    char endMarker = '\x00';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        // Serial.print("This just in ... ");
        // Serial.println(receivedChars);

      if (receivedChars[0] == 'A'){
        char bufferValue[3];
        for (int j = 0; j <= 1 ; j++){
          command_code += receivedChars[j+1];
        }
        for (int i = 0; i <= 2 ; i++){
          bufferValue[i] = receivedChars[i+3];
        }
        command_value = digitToInt(bufferValue);
      }
      else if (receivedChars[0] == 'B'){
        for (int j = 0; j<= 1 ; j++){
          command_code += receivedChars[j+1];
          command_value = 0;
        }
      }
      else {
        DcStop();
      }

      // Serial.print("INPUT : ");
      // Serial.print(command_code);
      // Serial.print("     VALUE : ");
      // Serial.print (command_value);
      // Serial.print("      ");
      // Serial.println(i);
      i = i + 1;
      processControl(command_code, command_value);

      memset (inputCharSerial, 0, 7);
      stringComplete = false;
      newData = false;
      command_code = "";
      command_value = 0;
    }
}











// void serialEvent(){
//
//
//   while (Serial.available()){
//   Serial.readBytes(inputCharSerial, 7);
//   Serial.print("inputCharSerial : ");
//   Serial.println(inputCharSerial);
//   if (inputCharSerial[6] == '\x00'){
//     stringComplete = true;
//   }
//   else if (inputCharSerial[6]!= '\x00'){
//     memset(inputCharSerial, 0, 7);
//   }
// }
//   delay(15);
//   Serial.flush();
//   // Serial.read();
//   // DcStop();
//
// }


void DcForward(int speed){
  digitalWrite(LeftIn1, 0);
  digitalWrite(LeftIn2, 1);
  digitalWrite(RightIn3, 1);
  digitalWrite(RightIn4, 0);
  analogWrite(LeftEnA, speed);
  analogWrite(RightEnB, speed);
}
void DcBackward(int speed){
  digitalWrite(LeftIn1, 1);
  digitalWrite(LeftIn2, 0);
  digitalWrite(RightIn3, 0);
  digitalWrite(RightIn4, 1);
  analogWrite(LeftEnA, speed);
  analogWrite(RightEnB, speed);
}
void DcRotRight(int speed){
  digitalWrite(LeftIn1, 1);
  digitalWrite(LeftIn2, 0);
  digitalWrite(RightIn3, 1);
  digitalWrite(RightIn4, 0);
  analogWrite(LeftEnA, speed);
  analogWrite(RightEnB, speed);
}
void DcRotLeft(int speed){
  digitalWrite(LeftIn1, 0);
  digitalWrite(LeftIn2, 1);
  digitalWrite(RightIn3, 0);
  digitalWrite(RightIn4, 1);
  analogWrite(LeftEnA, speed);
  analogWrite(RightEnB, speed);
}
void DcStop(){
  digitalWrite(LeftIn1, 0);
  digitalWrite(LeftIn2, 0);
  digitalWrite(RightIn3, 0);
  digitalWrite(RightIn4, 0);
  analogWrite(LeftEnA, 0);
  analogWrite(RightEnB, 0);
}
