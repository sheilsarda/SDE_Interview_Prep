## Overview of communication protocols

### SPI

#### Overview

- Interface originally designed to control peripherals
- All the communication is always initiated by the master on the bus
- Full-duplex pin configuration (data can be transmitted in both directions on a signal carrier at the same time) and the synchronized clock, it may be much faster than asynchronous communication due to the better robustness to clock skews between the systems sharing the bus
- Multiple peripherals can share the same bus, as long as media access strategies are defined
- A common way for a master to control one peripheral at a time is by using separate GPIO lines to control the slave selection, although this does require an additional wire for each slave

#### Setup

A few predefined settings must be known in advance and shared between the master and all the slaves on the same bus:

- Clock polarity, indicating whether the clock tick corresponds to a raising or a falling edge of the clock
- Clock phase, indicating whether the clock idle position is high or low
- Length of the data packet, any value between 4 and 16 bits
- Bit order, indicating whether the data is transmitted starting from the most significant bit or the least significant bit

#### Operations

4-wire SPI devices have four signals:

![](imgs/SPI_Protocol.jpg)

| Wire | Signal |
|--|--|
| SPI CLK / SCLK | Clock |
| CS | Chip select |
| MOSI | main out, subnode in |
| MISO | main in, subnode out |

- To initiate the communication, the master must activate the clock, and may send a command sequence to the slave on the MOSI line. When the clock is detected, the slave can immediately start transferring bytes in the opposite direction using the MISO line.
- Even if the master has finished transmitting, it must comply with the protocol implemented by the slave and permit it to reply by keeping the clock alive for the duration of the transaction. The slave is given a predefined number of byte slots to communicate with the master.
- In order to keep the clock alive even when there is no data to transfer to the slave, the master can keep sending dummy bytes through the MOSI line, which are ignored by the slave. In the meantime, the slave is allowed to send data through the MISO line, as long as the master ensures that the clock keeps running. 

**Unlike UART** in the master-slave communication model implemented in the SPI, the slaves can never spontaneously initiate SPI communication, as the master is the only device on the bus allowed to transmit a clock. Each SPI transaction is self-contained, and at the end, the slave
is deselected by turning off the corresponding slave-select signal.

#### C Code

````c
uint8_t spi1_read(void) {
    volatile uint32_t reg;
    do {
        reg = SPI1_SR;
    } while ((reg & SPI_SR_RX_NOTEMPTY) == 0);
    return (uint8_t)SPI1_DR;
}
void spi1_write(const char byte) {
    int i;
    volatile uint32_t reg;
    SPI1_DR = byte;
    do {
        reg = SPI1_SR;
    } while ((reg & SPI_SR_TX_EMPTY) == 0);
}

int main () {
    slave_on();
    spi1_write(0x8F);
    b = spi1_read();
    spi1_write(0xFF);
    b = spi1_read();
    slave_off();
}
````

![](imgs/SPI_Transaction.jpg)

### I2C

### UART

### Other GPIO protocols
