
#include <Ethernet.h>
#include <SPI.h>

byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x00, 0x0D };
IPAddress server(130,89,162,163);
//De poort waar de server op luistert
int port = 8000;

EthernetClient client;

void setup(){
    Serial.begin(9600);
    Serial.println("connecting..");
    
    Ethernet.begin(mac);
    delay(1000);


    String msg = "";
    String keys[] = {"key1", "key2", "key3"};
    String vals[] = {"hoi", "hai", "blub"};
    generatePostMessage(&msg, keys, vals, 3);
    
    Serial.println(msg);
    if(client.connect(server,port)){
      Serial.println("connected");
      
      client.println("POST /plantcontroller/api/add/ HTTP/1.1");
      client.println("Host: 130.89.162.163");
      client.println("Connection: close");
      client.println("Content-Type: application/x-www-form-urlencoded");
      client.println("Content-Length: 27");
      client.println();
      client.println("key1=hoi&key2=hai&key3=blub");      
    } else {
      Serial.println("faal :(");
    }

}

void loop(){
  if (client.available()) {
    char c = client.read();
    Serial.print(c);
  }
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
}







