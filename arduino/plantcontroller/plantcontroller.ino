#include <Ethernet.h>
#include <SPI.h>

byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x00, 0x0D };
byte ip[]  = {130,89,165,27};
IPAddress server(130,89,162,163);
//De poort waar de server op luistert
int port = 8000;

EthernetClient client;

void setup(){
    Serial.begin(9600);
    Ethernet.begin(mac, ip);
    delay(1000);
    
    if(client.connect(server,port)){
      Serial.println("connected");
      client.println("GET /plantcontroller HTTP/1.0");
      client.println();
    } else {
      Serial.println("faal :(");
    }

    String msg = "Hallo,";
    String keys[] = {"key1", "key2", "key3"};
    String vals[] = {"hoi", "hai", "blub"};
    generatePostMessage(&msg, keys, vals, 3);

    Serial.println(msg);
}

void loop(){

}

void generatePostMessage(String * msg, String keys[], String vals[], int len){
  for(int i =0; i<len; i++){
    String key_repl = keys[i];
    key_repl.replace(' ', '+');
    String val_repl = vals[i];
    val_repl.replace(' ', '+');
    *msg = *msg + key_repl + "=" + val_repl;
    if(i < len - 1){
      *msg = *msg  + "&";
    }
  }
  Serial.println(*msg);
}







