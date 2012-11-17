#include <SPI.h>
#include <Ethernet.h>
#include <Genibus.h>
#include <Types.h>
#include <Pdu.h>
#include <Crc.h>

#define GB_MASTER_ADDRESS  0x01

byte macAddress[] = { 0xde, 0xad, 0xaf, 0xfe, 0xaa, 0x55  };
IPAddress subnet = (255, 255, 255, 0);
#define LOCAL_PORT  6734

/* TODO: The IP-configuration has to be adjusted to your needs!!! */
IPAddress myIP(192, 168, 100, 20);
IPAddress serverIP(192, 168, 100, 10);
IPAddress gateway = (192, 168, 100, 1);

#define LED_PIN  9  /* Pin 13 has an LED connected on most Arduino boards, otherwise this should be changed. */
                    /* Pin 9: led connected on Arduino Ethernet board*/

EthernetClient client;

void setup(void)
{
  SPI.begin();
  Ethernet.begin(macAddress, myIP);
  //server.begin();

  delay(1000); // give the Ethernet shield a second to initialize:.
  
  if (client.connect(serverIP, LOCAL_PORT)) {
  } else {
  }
  
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.begin(9600);
}

typedef enum tagRcv_State {
    RCV_IDLE,
    RCV_COUNTING
} Rcv_State;

static byte Buffer[0xff];

void loop(void)
{
  byte receivedByte;
  byte byteCount;
  byte idx;
  Rcv_State state = RCV_IDLE;
  
  connectRequest(GB_MASTER_ADDRESS);
  while (Serial.available() == 0) {
  }
  digitalWrite(LED_PIN, HIGH);

  idx = 0;
  while (Serial.available() > 0) { 
    receivedByte = Serial.read();
    Buffer[idx] = receivedByte;
    if (idx == 1) { /* Length byte? */
      byteCount =  receivedByte + 2;
      state = RCV_COUNTING;
    }
    if (state == RCV_COUNTING) {
      	if (--byteCount == 0) {
                writeToServer(Buffer, byteCount + 6);
		break; /* We're done. */
	}
    }
    ++idx;
  }
  digitalWrite(LED_PIN, LOW);
  delay(2000);
}

void writeToServer(byte const * data, byte len)
{   
    if (client.connected()) {
      client.write(data, len); 
      client.println();
    }
}

