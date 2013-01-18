
#include <Ethernet.h>
#include <SPI.h>

byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x00, 0x0D };
IPAddress server(130,89,162,163);
//De poort waar de server op luistert
int port = 8000;
int humidityPin = A0;


EthernetClient client;

void setup(){
    Serial.begin(9600);
    Serial.println("connecting..");
    
    Ethernet.begin(mac);
    delay(1000);


    String humidityMsg = "";
    measureHumidity(&humidityMsg);
    if(client.connect(server,port)){
      Serial.println("connected");
      Serial.println(humidityMsg.length());
      client.println("POST /plantcontroller/api/add/ HTTP/1.1");
      client.println("Host: 130.89.162.163");
      client.println("Connection: close");
      client.println("Content-Type: application/x-www-form-urlencoded");
      client.println("Content-Length: " + humidityMsg.length());
      client.println();
      client.println(humidityMsg);      
    } else {
      Serial.println("faal :(");
    }
    if (!client.connected()) {
      Serial.println();
      Serial.println("disconnecting.");
      client.stop();
      for(;;)
      ;
    }

}

void loop(){
  if (client.available()) {
    char c = client.read();
    Serial.print(c);
  }
}

void measureHumidity(String * msg){
  int values = 0;
  int samples = 10;
  for(int i = 0; i < samples; i++){
    values = values + analogRead(humidityPin);
  }
  int reading = values / samples; 
  String valReading = String(reading);
  String valSensor = "humidity";
  String valSamples = String(samples);
  String vals[] = {valReading,valSensor,valSamples};
  String keys[] = {"reading","sensortype","samples"};
  generatePostMessage(msg,keys,vals,3);
  Serial.println(*msg);
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







