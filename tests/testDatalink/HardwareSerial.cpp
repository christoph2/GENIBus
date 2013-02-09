
/*!
 * Mock implementation.
 */

#include "HardwareSerial.h"
#include <stdio.h>

HardwareSerial::HardwareSerial()
{

}

void HardwareSerial::begin(long speed)
{

}

void HardwareSerial::setTelegram(uint8_t const * telegram, uint8_t len)
{
    _telegram = telegram;
    _pos = 0;
    _len = len;
}

uint8_t HardwareSerial::getLen(void)
{
    return _len;
}

uint8_t HardwareSerial::write(uint8_t const * buf, size_t len)
{
  return len;
}


uint8_t HardwareSerial::write(uint8_t val)
{
  return 1;
}


size_t HardwareSerial::available(void)
{
    if (_pos < _len) {
        return 1;
    } else {
      return 0;
    }
}


int16_t HardwareSerial::read(void)
{
    int16_t sym = _telegram[_pos++];

    //printf("%#X ", sym);
    return sym;
//  return -1;
}


