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
    String keys[] = {"key1", "key2", "key3"}
    String vals[] = {"hoi", "hai", "blub"};
    generatePostMessage(&msg, &keys, &vals, 3);

    Serial.println(msg);
}

void loop(){

}

void generatePostMessage(String * msg, String * keys[], String * vals[], int len){
  for(int i =0; i<len-1; i++){
    *msg = *msg + (*keys[i]).replace(" ", "+") + "=" + (*vals[i]).replace(" ", "+") + "&";
  }
  *msg = *msg + (*keys[len-1]).replace(" ", "+") + "=" + (*vals[len-1]).replace(" ", "+");
  Serial.println(*msg);
}







