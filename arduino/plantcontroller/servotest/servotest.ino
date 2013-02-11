#include <Servo.h> 

Servo myservo;

void setup() {
  myservo.attach(9);

}

void loop() {
  myservo.write(100);
  delay(10000);
  myservo.write(10);
  delay(10000);
  
}
