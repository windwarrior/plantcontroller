
#include <Ethernet.h>
#include <SPI.h>
#include <Servo.h> 

Servo servo;//De servo die water moet geven
byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x00, 0x0D };//MAC adres van het ethernet shield
IPAddress server(130,89,162,163);//IP adres van de server
int port = 8000;//De poort waar de server op luistert
int humidityPin = A0;//De pin waar de humiditymeter op zit
unsigned long time = 60000;//De tijd die tussen twee loops zit
unsigned long timeToWater;//Tijd die het duurt totdat de plant water gegeven moet worden
int limitToWater;//Limiet waaronder de plant water moet krijgen, indien 0 is er geen limiet.


EthernetClient client;

void setup(){
    servo.attach(9);
    servo.write(10);
    timeToWater = 4,294,967,295; //Wordt hier op de maximale waarde van een unsigned long geinitialiseerd
    limitToWater = 0;
    Serial.begin(9600);
    Serial.println("connecting..");
    Ethernet.begin(mac);
}

void loop(){
  unsigned long beginTime = millis();
  connectToServer();
  String humidityMsg = "";
  measureHumidity(&humidityMsg);
  if(client.connected()){
    Serial.println(humidityMsg.length());
    Serial.println(humidityMsg);
    client.println("POST /plantcontroller/api/add/ HTTP/1.1");
    client.println("Host: 130.89.165.27");
    client.println("Connection: close");
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.println("Content-Length: " + String(humidityMsg.length()));
    client.println();
    client.println(humidityMsg);
    while (!client.available()){
    ;//Loop om te wachten totdat er een bericht binnenkomt
    }
    boolean reading = true;
    char prev = ' ';
    String inMsg = ""; 
    while (reading) {
      if (client.available()){
        char c = client.read();
        Serial.print(c);
        if (prev == c && c == '\n'){
          while(client.available()){
            inMsg += char(client.read());            
          }
          Serial.println(inMsg);
          reading = false;
        }
        if (!(c == '\r' && prev == '\n')){
          prev = c;
        }
      }
    }
    if (inMsg.startsWith("W")){
      if (inMsg.indexOf("<") != -1){
        int split = inMsg.indexOf("<");
        timeToWater = stringToInt(inMsg.substring(2,split));
        limitToWater = stringToInt(inMsg.substring(split+1));
      } else {
        timeToWater = stringToInt(inMsg.substring(2));
        limitToWater = 0;
      }
    } 
    if (inMsg.startsWith("E")){
      Serial.println(inMsg);
    }
  }//endif (client.connected())
  timeToWater = timeToWater - time;
  if (timeToWater <= 0){
    if (limitToWater == 0){
      servo.write(100);
      delay(10000);
      servo.write(10);
    } else {
      if(humidityReading(10) < limitToWater){
        servo.write(100);
        delay(10000);
        servo.write(10);
      }
    }
  }
  client.stop();
  //Zorgt ervoor dat de loop elke time milliseconden wordt uitgevoerd. Moet altijd onderin de loop staan
  unsigned long endTime = millis();
  unsigned long duration = endTime - beginTime;
  if ((duration) < time) {
    delay(time - duration);
  }
}
//Meet de humidity en maakt er een postmessage van
void measureHumidity(String * msg){
  int samples = 10; // Het aantal samples wat gemeten wordt
  int reading = humidityReading(samples);
  String valReading = String(reading);
  String valSensor = "humidity";
  String valSamples = String(samples);
  String valSource = "arduinoProductie";
  String vals[] = {valReading,valSensor,valSamples,valSource};
  String keys[] = {"reading","sensortype","samples","source"};
  generatePostMessage(msg,keys,vals,4);
}
//Meet de humidity met het gegeven aantal samples
int humidityReading(int samples){
  int values = 0;
  for(int i = 0; i < samples; i++){
    values = values + analogRead(humidityPin);
  }
  int reading = values / samples;
  return reading;
} 
  

void generatePostMessage(String * msg, String keys[], String vals[], int len){
  for(int i =0; i<len; i++){
    String key_repl = keys[i];
    key_repl.replace(' ', '+');
    String val_repl = vals[i];
    val_repl.replace(' ', '+');
    *msg = *msg + key_repl + '=' + val_repl;
    if(i < len - 1){
      *msg = *msg  + '&';
    }
  }
}
//Verbindt met de server
void connectToServer(){  
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
//Zet een string om naar een integer
int stringToInt(String msg){
  int result = 0;
  while (msg.length() != 0){
    result = result * 10;
    if (msg.charAt(0) == '0'){
      result += 0;
    }
    if (msg.charAt(0) == '1'){
      result += 1;
    }
    if (msg.charAt(0) == '2'){
      result += 2;
    }
    if (msg.charAt(0) == '3'){
      result += 3;
    }
    if (msg.charAt(0) == '4'){
      result += 4;
    }
    if (msg.charAt(0) == '5'){
      result += 5;
    }
    if (msg.charAt(0) == '6'){
      result += 6;
    }
    if (msg.charAt(0) == '7'){
      result += 7;
    }
    if (msg.charAt(0) == '8'){
      result += 8;
    }
    if (msg.charAt(0) == '9'){
      result += 9;
    }
    msg = msg.substring(1);
  }
  return result;

}





