
#include <Ethernet.h>
#include <SPI.h>

byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x00, 0x0D };
IPAddress server(130,89,162,163);
//De poort waar de server op luistert
int port = 8000;
int humidityPin = A0;
//De tijd die tussen twee loops zit
unsigned long time = 5000;


EthernetClient client;

void setup(){
    Serial.begin(9600);
    Serial.println("connecting..");
    
    Ethernet.begin(mac);
    client.connect(server,port);
    delay(1000);
    if (!client.connected()) {
      Serial.println();
      Serial.println("disconnecting.");
      client.stop();
      for(;;)
      ;
    } else {
      Serial.println("connected");
    }

}

void loop(){
  unsigned long beginTime = millis();
  String humidityMsg = "";
  measureHumidity(&humidityMsg);
  if(client.connected()){
    Serial.println(humidityMsg.length());
    Serial.println(humidityMsg);
    client.println("POST /plantcontroller/api/add/ HTTP/1.1");
    client.println("Host: 86.90.155.93");
//    client.println("Connection: close");
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.println("Content-Length: " + humidityMsg.length());
    client.println();
    client.println(humidityMsg);
  } else {
    Serial.println("faal");
  }
  while (!client.available()){
    ;//Loop om te wachten totdat er een bericht binnenkomt
  }
  boolean reading = true;
  char prev = ' ';
  while (reading) {
    if (client.available()){
      char c = client.read();
      Serial.print(c);
      if (prev == c && c == '\n'){
        Serial.println("debug1");
        while(client.available()){
          Serial.print(client.read());
        }
        reading = false;
      }
      prev = c;
    }
  }
  //Zorgt ervoor dat de loop elke time milliseconden wordt uitgevoerd. Moet altijd onderin de loop staan
  unsigned long endTime = millis();
  unsigned long duration = endTime - beginTime;
  if ((duration) < time) {
    delay(time - duration);
  }
}

void measureHumidity(String * msg){
  int values = 0;
  int samples = 10; // Het aantal samples wat gemeten wordt
  for(int i = 0; i < samples; i++){
    values = values + analogRead(humidityPin);
  }
  int reading = values / samples; 
  String valReading = String(reading);
  String valSensor = "humidity";
  String valSamples = String(samples);
  String valSource = "arduinoProductie";
  String vals[] = {valReading,valSensor,valSamples,valSource};
  String keys[] = {"reading","sensortype","samples","source"};
  generatePostMessage(msg,keys,vals,4);
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







