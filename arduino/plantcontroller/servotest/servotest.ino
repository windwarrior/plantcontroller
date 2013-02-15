#include <Servo.h> 

Servo myservo;

void setup() {
  myservo.attach(9);

}

void loop() {
  myservo.write(90);
  delay(10000);
  myservo.write(35);
  delay(10000);
  
}
