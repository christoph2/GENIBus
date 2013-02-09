
#include "GB_Datalink.h"
#include <stdio.h>

const uint8_t CONNECT_RESP[] = {
    0x24,
    0x0e,
    0x01,
    0x20,

    0x00,
    0x02,
    0x46,
    0x0e,
    0x04,
    0x02,
    0x20,
    0xf7,
    0x02,
    0x02,
    0x03,
    0x01,

    0x00,
    0x04
};

const uint8_t DATA_RESP[] = {
    0x24,
    0x1E,
    0x04,
    0x20,

    0x02,
    0x1A,
    0x10,
    0x00,
    0x00,
    0x01,
    0xA5,
    0xFE,
    0xFE,
    0x94,
    0x7B,
    0x23,
    0xCD,
    0xB4,
    0x0B,
    0x80,
    0x22,
    0xE9,
    0x0C,
    0xE7,
    0xA5,
    0x0E,
    0x00,
    0x20,
    0x39,
    0x30,
    0x40,
    0x00,

    0xec,
    0x8b
};

const uint8_t INFO_RESP[] = {
    0x24,
    0x18,
    0x04,
    0x20,

    0x02,
    0x14,
    0x82,
    0x19,
    0x00,
    0x0C,
    0x82,
    0x17,
    0x00,
    0x20,
    0x82,
    0x09,
    0x00,
    0x28,
    0x82,
    0x13,
    0x00,
    0x24,
    0x82,
    0x2F,
    0x00,
    0xFE,

    0xD9,
    0xBF,
};


void frameReceived(uint8 * buffer, uint8 len)
{
    printf("Frame received: ");
    for (int idx = 0; idx < len; ++idx) {
        printf("%#X ", buffer[idx]);
    }
    printf("\n\n");
}

HardwareSerial hws = HardwareSerial();

GB_Datalink link(hws, frameReceived);


#define ARR_SIZE(a) ((sizeof((a))) / sizeof((a)[0]))

void runTest(uint8_t const * tel, uint8_t len)
{

    hws.setTelegram(tel, len);

    for (int idx=0; idx < hws.getLen(); ++idx) {
        link.feed();
    }
}

int main(void)
{

  runTest(CONNECT_RESP, ARR_SIZE(CONNECT_RESP));
  runTest(DATA_RESP, ARR_SIZE(DATA_RESP));
  runTest(INFO_RESP, ARR_SIZE(INFO_RESP));

  return 0;
}

