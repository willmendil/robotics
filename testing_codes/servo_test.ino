// python-build-start
// action, upload
// board, arduino:avr:mega:cpu=atmega2560
// port, /dev/ttyACM0
// ide, 1.8.9
// python-build-end

#include <Servo.h>

Servo servo_H;  // create servo object to control a servo
Servo servo_V;

int servo_H_min = 10;
int servo_H_max = 165;
int servo_V_min = 15;
int servo_V_max = 145;

boolean direction_motor = 0;
int enA = 7;
int in1 = 23;
int in2 = 25;
int in3 = 27;
int in4 = 29;
int enB = 6;


void setup() {
	Serial.begin(9600);
	servo_H.attach(4);  // attaches the servo on pin 9 to the servo object
	servo_V.attach(5);  // attaches the servo on pin 9 to the servo object
  servo_H.write(90);  //min = 10 : max = 170
  servo_V.write(90);  //min = 15 : max = 150

  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(enB, OUTPUT);
}

void loop() {
  demo_servo();
}

void demo_servo(){
	servo_position(0);
	delay(500);
	servo_position(1);
	delay(500);
  servo_position(2);
	delay(500);
	servo_position(3);
	delay(500);


}

boolean servo_position(int state) {
	if(state == 0) {
		for (servo_pos = servo_H_min; servo_pos <= servo_H_max; servo_pos += 1) {	// goes from 0 degrees to 180 degrees
			// in steps of 1 degree
			servo_H.write(servo_pos);              // tell servo to go to position in variable 'pos'
			//servo_V.write(servo_pos);              // tell servo to go to position in variable 'pos'
			delay(5);                       // waits 15ms for the servo to reach the position
		}

	}
	else if (state == 1) {
		for (servo_pos = servo_V_min; servo_pos <= servo_V_max; servo_pos += 1) {	// goes from 0 degrees to 180 degrees
			// in steps of 1 degree
      //servo_H.write(servo_pos);              // tell servo to go to position in variable 'pos'
			servo_V.write(servo_pos);              // tell servo to go to position in variable 'pos'
			delay(5);                       // waits 15ms for the servo to reach the position
		}

	}
  else if (state == 2) {
		for (servo_pos = servo_H_max; servo_pos >= servo_H_min; servo_pos -= 1) {	// goes from 0 degrees to 180 degrees
			// in steps of 1 degree
      servo_H.write(servo_pos);              // tell servo to go to position in variable 'pos'
			//servo_V.write(servo_pos);              // tell servo to go to position in variable 'pos'
			delay(5);                       // waits 15ms for the servo to reach the position
		}

	}
  else if (state == 3) {
		for (servo_pos = servo_V_max; servo_pos >= servo_V_min; servo_pos -= 1) {	// goes from 0 degrees to 180 degrees
			// in steps of 1 degree
      //servo_H.write(servo_pos);              // tell servo to go to position in variable 'pos'
			servo_V.write(servo_pos);              // tell servo to go to position in variable 'pos'
			delay(5);                       // waits 15ms for the servo to reach the position
		}

	}
}
