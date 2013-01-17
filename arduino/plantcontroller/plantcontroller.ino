#include <ethernet.h>

byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x00, 0x0D };
byte ip[]  = {130,89,165,27};
byte server[] = {130,89,162,163};
//De poort waar de server op luistert
int port = 8000;

//Client client(server, port);

void setup(){
    Serial.begin(9600);
    String msg = "Hallo,";
    String args[] = {"hoi", "hai", "blub"};
    generatePostMessage(&msg, args, 3);
    Serial.println(msg);
}

void loop(){

}

void generatePostMessage(String * msg, String args[], int len){
  for(int i =0; i<len; i++){
    *msg = *msg + args[i];
  }
  Serial.println(*msg);
}






