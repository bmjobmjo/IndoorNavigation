#include <Wire.h>
#include <LSM303.h>
#define  degtol 10
LSM303 compass;
const int trigPin = 13; // 10 microsecond high pulse causes chirp , wait 50 us
const int echoPin = 12; // Width of high pulse indicates distance
// Servo motor that aims ultrasonic sensor .
const int servoPin = 11; // PWM output for hobby servo
// Motor control pins : L298N H bridge
const int enAPin = 6; // Left motor PWM speed control
const int in1Pin = 7; // Left motor Direction 1
const int in2Pin = 8; // Left motor Direction 2
const int in3Pin = 9; // Right motor Direction 1
const int in4Pin = 2; // Right motor Direction 2
const int enBPin = 3; // Right motor PWM speed control
String b;
const unsigned int MAX_MESSAGE_LENGTH = 11;
static unsigned int message_pos = 0;
char directions;
int speeds;
int delays;
float heading;

enum Motor { LEFT, RIGHT , FWD, BKWD};
// Set motor speed: 255 full ahead, −255 full reverse , 0 stop
void reset()
{
  delays = NULL;
  speeds = 0;
  directions = 0;
  message_pos = 0;

}
void stops()
{
  analogWrite(enAPin, 0);
  analogWrite(enBPin, 0);

}

void compasRead()
{
  compass.read();


    heading =compass.heading((LSM303::vector<int>){0, 0, 1});
  //Serial.print("heading");
 // Serial.println(heading);
  delay(100);

}

int rotateDeg(int deg)
{ float maxdeg = deg + degtol;
  float mindeg = deg - degtol;
  compasRead();
  Serial.println("in reate ");
  Serial.println(heading);
  Serial.println(mindeg);
  Serial.println(maxdeg);
  int counter=0;
  while (1) {
  /*  if ((heading >= maxdeg) || (heading <= mindeg))
    { go(LEFT, 180);
      Serial.println("in reate  if ");
      delay(100);
    }*/
    go(LEFT,180);
    delay(100);
    stops();
    if ((heading <= maxdeg) && (heading >= mindeg))
    { return 0;
    }
    ++counter;
    Serial.print("Head :");
    Serial.print(heading);
    Serial.print("Min :");
    Serial.print(mindeg);
    Serial.print("Man :");
    Serial.println(maxdeg);
   // Serial.println(counter);
    if(counter>400) {return -1;stops();}
    compasRead();
    //Serial.println("in sdjust loop ");
    //Serial.println(heading);
    //Serial.println(mindeg);
    //Serial.println(maxdeg);
  }//
}

void go( enum Motor m, int speed)
{
  if (m == LEFT)
  { analogWrite(enAPin, 0);
    analogWrite(enBPin, speed);
    digitalWrite(in1Pin, HIGH);
    digitalWrite(in2Pin, LOW);
    digitalWrite(in3Pin, HIGH);
    digitalWrite(in4Pin, LOW);
   // Serial.println(" in Left ");

  }
  else if (m == RIGHT)
  { analogWrite(enBPin, 0);
    analogWrite(enAPin, speed);
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, HIGH);
    digitalWrite(in3Pin, LOW);
    digitalWrite(in4Pin, HIGH);
    //Serial.println(" in Right ");
  }
  else if (m == BKWD)
  { analogWrite(enAPin, speed);
    analogWrite(enBPin, speed);
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, HIGH);
    digitalWrite(in3Pin, HIGH);
    digitalWrite(in4Pin, LOW);
    //Serial.println(" in bkwd");
  }
  else if (m == FWD)
  { analogWrite(enAPin, speed);
    analogWrite(enBPin, speed);
    digitalWrite(in1Pin, HIGH);
    digitalWrite(in2Pin, LOW);
    digitalWrite(in3Pin, LOW);
    //Serial.println(" in fwd ");
    digitalWrite(in4Pin, HIGH);
  }

}


void testMotors ()
{
  static int speed[8] = { 128, 255, 128, 0 , -128, -255, -128, 0};
  go(RIGHT, 0);
  for (unsigned char i = 0 ; i < 8 ; i++)
    go(LEFT, speed[i ]), delay (200);
  for (unsigned char i = 0 ; i < 8 ; i++)
    go(RIGHT, speed[i ]), delay (200);
}




void setup () {
  
  Serial.begin(9600);

  Wire.begin();
  compass.init();
  compass.enableDefault();

 compass.m_min = (LSM303::vector<int16_t>){-392, -137, -4};
  compass.m_max = (LSM303::vector<int16_t>){+339, +976, +3};

  pinMode(trigPin , OUTPUT);
  pinMode(echoPin, INPUT);
  digitalWrite ( trigPin , LOW);
  pinMode(enAPin, OUTPUT);
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(in3Pin, OUTPUT);
  pinMode(in4Pin, OUTPUT);
  pinMode(enBPin, OUTPUT);

  go(LEFT, 0);
  go(RIGHT, 0);
  //testMotors ();
  // Scan the surroundings before starting

  delay (200);
//rotateDeg(180);
}


void loop() {

  /* go(LEFT, 225);

    delay(1000);
    go(RIGHT,225);
    delay(1000);*/

  while (Serial.available() > 0)
  {
    //Create a place to hold the incoming message
    static char message[MAX_MESSAGE_LENGTH];


    //Read the next available byte in the serial receive buffer
    char inByte = Serial.read();
   // Serial.println("Char recived->");
   // Serial.println(inByte);
    //Message coming in (check not terminating character) and guard for over message size
    if ( inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) )
    {
      //Add the incoming byte to our message
      message[message_pos] = inByte;
      message_pos++;
      //Serial.print("message pos :");
      //Serial.println(message_pos);
    }
    //Full message received...
    else
    {
      //Serial.println("command received");
      //Add null character to string
      message[message_pos] = '\0';

      //Print the message (or do other things)
      Serial.println(message);

      int num = 0, ten = 1;
      char *token;

      /* get the first token */
      token = strtok(message, " ");

      /* walk through other tokens */
      while ( token != NULL ) {
        Serial. println(  token );
        if (num == 0)directions = token[0];
        else if (num == 1) speeds = atoi(token);
        else if (num == 2) delays = atoi(token);
        num++;

        token = strtok(NULL, " ");
      }
    //  Serial. println(  directions );
    //  Serial. println(  speeds );
    //  Serial. println(  delays );

      if (directions == 'L')
      {
        go(LEFT, speeds);
        delay(delays);

      }

      if (directions == 'R')
      {
        go(RIGHT, speeds);
        delay(delays);

      }

      if (directions == 'F')
      {
         go(FWD, speeds/2);
        delay(delays/4);
        
        go(FWD, speeds);
        delay(delays/2);

         go(FWD, speeds/2);
        delay(delays/4);
      }

      if (directions == 'B')
      {
        go(BKWD, speeds/2);
        delay(delays/4);
        
        go(BKWD, speeds);
        delay(delays/2);
        
        go(BKWD, speeds/2);
        delay(delays/4);
      }
      if (directions == 'Z')
      { Serial.println("here");
        rotateDeg(speeds);

      }

      reset();

      stops();
      /*while(message_pos<5)
        { Serial.print(atoi(message[message_pos]));
        num+=ten* atoi(message[message_pos]);
        Serial.print(num);
        ten=ten*10;
        message_pos++;
        }
        Serial.print(num);
        //Reset for the next message
        message_pos = 0;*/
 }
  }


}

 
