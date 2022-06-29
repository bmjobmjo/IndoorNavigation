#include <WiFi.h>
#include <WebServer.h>

/* Put your SSID & Password */
const char* ssid = "BIGB";  // Enter SSID here
const char* password = "123456789";  //Enter Password here

/* Put IP Address details */

WiFiClient client;
WebServer server(80);
void setup()
{
  Serial.begin(9600);
  WiFi.begin("BIGB", "123456789");
  while(WiFi.status() != WL_CONNECTED)
  {
    delay(200);
    Serial.print("..");
  }
  Serial.println();
  Serial.println("NodeMCU is connected!");
  Serial.println(WiFi.localIP());
  server.on("/", handle_OnConnect);
  server.on("/L", handle_left);
  server.on("/R", handle_right);

 server.on("/F", handle_frwd);
  server.on("/B", handle_back);
  server.on("/FF", handle_frwd_f);
  server.on("/BB", handle_back_b);
    server.on("/FFF", handle_frwd_ff);
  server.on("/BBB", handle_back_bb);
  
  server.onNotFound(handle_OnConnect);
  server.begin();
}

void loop() 
{
  server.handleClient();
}




void handle_OnConnect() {
  //Serial.println("L 200 100");
  server.send(200, "text/html", "Nop"); 
}

void handle_left() {
  Serial.println("L 200 100");
  server.send(200, "text/html", "Left"); 
}

void handle_right() {
 Serial.println("R 200 100");
  server.send(200, "text/html", "Right"); 
}


void handle_frwd() {
 Serial.println("F 200 100");
  server.send(200, "text/html", "Forward"); 
}

void handle_frwd_f() {
 Serial.println("F 200 200");
  server.send(200, "text/html", "Forward"); 
}

void handle_frwd_ff() {
 Serial.println("F 200 500");
  server.send(200, "text/html", "Forward"); 
}
void handle_back() {
 Serial.println("B 200 100");
  server.send(200, "text/html", "Back"); 
}

void handle_back_b() {
 Serial.println("B 200 200");
  server.send(200, "text/html", "Back"); 
}

void handle_back_bb() {
 Serial.println("B 200 500");
  server.send(200, "text/html", "Back"); 
}

  
