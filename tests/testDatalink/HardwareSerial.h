
/*!
 * Mock implementation.
 */

#if !defined(HARDWARE_SERIAL_H)
#define HARDWARE_SERIAL_H

#include <stdint.h>
#include <stdlib.h>

class HardwareSerial {
public:
        HardwareSerial();
        void setTelegram(uint8_t const * telegram, uint8_t len);
        uint8_t getLen(void);
        void begin(long speed);
        uint8_t write(uint8_t const * buf, size_t len);
        uint8_t write(uint8_t val);
        size_t available(void);
        int16_t read(void);
private:
        uint8_t const * _telegram;
        uint8_t _len;
        uint8_t _pos;
};

#endif /* HARDWARE_SERIAL_H */

