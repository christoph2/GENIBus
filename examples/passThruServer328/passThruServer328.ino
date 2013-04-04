#include <EtherShield.h>
#include <GB_Datalink.h>
#include <Genibus.h>


#define GB_MASTER_ADDRESS  0x01

byte macAddress[] = { 0x90, 0xa2, 0xda, 0x00, 0x69, 0x4b  };

IPAddress subnet = (255, 255, 255, 0);
#define LOCAL_PORT  6734

/* TODO: The IP-configuration has to be adjusted to your needs!!! */
IPAddress myIP(192, 168, 1, 3);         // for Linux users: adjust the two first line on the file /etc/hosts:
IPAddress serverIP(192, 168, 1, 2);     // IP address of "localhost" must be the same as "IPAddress serverIP", for example "192.168.1.2  localhost"
//IPAddress gateway = (192,168, 1, 1);  // and, 2nd line, "192.168.1.2   'my computer name'"
int EN = 2;                             // RS485 has a enable/disable pin to transmit or receive data.
                                        // Arduino Digital Pin 2 = Rx/Tx 'Enable'; High to Transmit, Low to Receive
int LED_PIN = 9;                        /* Pin 13 has an LED connected on most Arduino boards, otherwise this should be changed. */
                                        /* Pin 9: led connected on Arduino Ethernet board*/

//EthernetServer server(LOCAL_PORT);
EtherShield es = EtherShield();
//EthernetClient client;

boolean alreadyConnected = false;

void setup(void)
{
    es.ES_enc28j60SpiInit();

    delay(1000); // give the Ethernet shield a second to initialize:.

    Serial.begin(9600);

    pinMode(EN, OUTPUT);
    pinMode(LED_PIN, OUTPUT);
    setTxMode();
}

void frameReceived(uint8 * buffer, uint8 len)
{
    setTxMode();    // Switch back to TX mode.
    delay(500);
    digitalWrite(LED_PIN, LOW);

    client.write(buffer, len);
    client.stop();
}

void errorCallout(Gb_Error error, uint8 * buffer, uint8 len)  //  Needs latest software version to compile!!!
{
    //Serial.print("CRC-Error\n\r"); // Only a single cause of error right now.
    setTxMode();    // Switch back to TX mode.
    delay(500);
    digitalWrite(LED_PIN, LOW);

    client.write(buffer, len);
    client.stop();
}

GB_Datalink link(Serial, frameReceived, errorCallout);

byte header[4];
byte apdus[0xff];

void loop(void)
{
    client = server.available();

    if (client) {
        setTxMode();    // We need to be able to write the received telegram later on.
        digitalWrite(LED_PIN, HIGH);    // Toggle LED before receiving.
        //Serial.print(" server available ");
        //Serial.print("\n\r");
        //delay(500);

        // TAP#1 - Indicates basic TCP/IP connectivity.
        readRequest(client);
    }
    delay(50);
}


void serialEvent(void)
{
    // receive data
    //digitalWrite(LED_PIN, LOW);
    // TAP#3 - Pump received a correct request and is now answering.
    link.feed();
}


void writeToClient(EthernetClient client, byte const * data, byte len)
{
    client.write(data, len);
    client.stop();
}


void readRequest(EthernetClient client)
{
    byte totalLength = 0;
    byte remainingBytes;
    char ch;

    while (client.connected()) {
        if (client.available()) {
            ch = client.read();
            link.write(ch);

            if (totalLength == 0x01) {  // Length byte.
                remainingBytes = (byte)ch + 2;

            } else if (totalLength > 1) {
                remainingBytes -= 1;

                if (remainingBytes == 0) {

                    //Serial.print("TCP frame completed");
                    //Serial.print("\n\r");
                    link.reset();
		    delay(2); 	    // !!!
                    setRxMode();    // TCP frame completely received and written to RS485, now receiving response.
                    return;
                }
            }
            totalLength += 1;
        }
    }
}

void setRxMode(void)
{
    digitalWrite(EN, LOW);//Enable RS485 Receiving Data
    digitalWrite(LED_PIN, LOW);
}

void setTxMode(void)
{
    digitalWrite(EN, HIGH);//Enable RS485 Receiving Data
    digitalWrite(LED_PIN, LOW);
}

