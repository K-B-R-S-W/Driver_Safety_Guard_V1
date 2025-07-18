#include <WiFi.h>
#include <WebServer.h>

// Replace with your network credentials
const char* ssid = "SLTFIBER";
const char* password = "Uchihamadara1";

WebServer server(80);

// Define the GPIO pins for the LEDs and the buzzer
const int greenLED = 5;      // GPIO pin connected to the Green LED
const int redLED = 18;       // GPIO pin connected to the Red LED
const int orangeLED = 19;    // GPIO pin connected to the Orange LED
const int blueLED = 17;      // GPIO pin connected to the Blue LED
const int buzzer = 16;       // GPIO pin connected to the Buzzer

unsigned long timeoutDuration = 5000; // Timeout duration in milliseconds
unsigned long lastActivated = 0; // Last time an LED was activated

void playBuzzerTune() {
  int melody[] = {262, 294, 330, 349, 392, 440, 494, 523}; // Notes in the C major scale
  int noteDurations[] = {4, 4, 4, 4, 4, 4, 4, 4};         // Quarter note duration

  for (int thisNote = 0; thisNote < 8; thisNote++) {
    int noteDuration = 1000 / noteDurations[thisNote];
    tone(buzzer, melody[thisNote], noteDuration);
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    noTone(buzzer);
  }
}

void beepBuzzer(int duration) {
  tone(buzzer, 1000); // 1 kHz tone
  delay(duration);
  noTone(buzzer);
}

void setup() {
  Serial.begin(115200);
  Serial.println("Starting ESP32 setup...");

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // Set the GPIO pins as output
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(orangeLED, OUTPUT);
  pinMode(blueLED, OUTPUT);
  pinMode(buzzer, OUTPUT);

  playBuzzerTune();

  // Test LEDs and Buzzer
  Serial.println("Testing LEDs and Buzzer...");

  // Turn on Green LED
  digitalWrite(greenLED, HIGH);
  Serial.println("Green LED Test");
  delay(1000);
  digitalWrite(greenLED, LOW);

  // Turn on Red LED
  digitalWrite(redLED, HIGH);
  Serial.println("Red LED Test");
  delay(1000);
  digitalWrite(redLED, LOW);

  // Turn on Orange LED
  digitalWrite(orangeLED, HIGH);
  Serial.println("Orange LED Test");
  delay(1000);
  digitalWrite(orangeLED, LOW);

  // Turn on Blue LED
  digitalWrite(blueLED, HIGH);
  Serial.println("Blue LED test");
  delay(1000);
  digitalWrite(blueLED, LOW);

  // Test Buzzer
  beepBuzzer(1000); // 1 second beep
  Serial.println("Buzzer test");

  Serial.println("LEDs and Buzzer Test Complete");

  // Define server routes and their actions
  server.on("/distracted", HTTP_GET, [](){
    digitalWrite(greenLED, HIGH);
    beepBuzzer(1000); // 1 second beep
    lastActivated = millis();
    Serial.println("Distracted: Green LED On, Buzzer Beep");
    server.send(200, "text/plain", "Distracted: Green LED On with Buzzer Beep");
  });

  server.on("/drowsy", HTTP_GET, [](){
    digitalWrite(redLED, HIGH);
    beepBuzzer(1000); // 1 second beep
    lastActivated = millis();
    Serial.println("Drowsy: Red LED On, Buzzer Beep");
    server.send(200, "text/plain", "Drowsy: Red LED On with Buzzer Beep");
  });

  server.on("/mobileuse", HTTP_GET, [](){
    digitalWrite(orangeLED, HIGH);
    beepBuzzer(1000); // 1 second beep
    lastActivated = millis();
    Serial.println("Mobile Use: Orange LED On, Buzzer Beep");
    server.send(200, "text/plain", "Mobile Use: Orange LED On with Buzzer Beep");
  });

  server.on("/smoking", HTTP_GET, [](){
    digitalWrite(blueLED, HIGH);
    beepBuzzer(1000); // 1 second beep
    lastActivated = millis();
    Serial.println("Smoking: Blue LED On, Buzzer Beep");
    server.send(200, "text/plain", "Smoking: Blue LED On with Buzzer Beep");
  });

  server.on("/off", HTTP_GET, [](){
    digitalWrite(greenLED, LOW);
    digitalWrite(redLED, LOW);
    digitalWrite(orangeLED, LOW);
    digitalWrite(blueLED, LOW);
    noTone(buzzer);
    Serial.println("All LEDs and Buzzer Off");
    server.send(200, "text/plain", "All LEDs and Buzzer Off");
  });

  server.begin();
  Serial.println("Server started");
}

void loop() {
  server.handleClient();

  // Check if the timeout period has passed
  if (millis() - lastActivated >= timeoutDuration) {
    digitalWrite(greenLED, LOW);
    digitalWrite(redLED, LOW);
    digitalWrite(orangeLED, LOW);
    digitalWrite(blueLED, LOW);
    noTone(buzzer);
  }
}