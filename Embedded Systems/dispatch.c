#include <stdint.h>
#include <stdio.h>
#define DISPLAY_MESSAGE 0x34
#define MOTOR_MESSAGE 0x80


// Handle Display messages
void display_message(uint8_t *m, uint16_t message_len){

}

// Handle Motor messages
void update_motor(float forward_back, float left_right){

}

void dispatcher(uint8_t *packet){
  
  uint8_t  packet_id    = packet[0];
  uint8_t  message_type = packet[1];
  uint16_t message_len  = packet[2] || (packet[3] << sizeof(uint8_t));

  uint8_t message_data[message_len];

  printf("Packet ID %d \r\n", packet_id);
  printf("Type      %x \r\n", message_type);
  printf("Length    %d \r\n", message_len);
}


int main(){

  uint8_t display_packet[] = {0x1, 0x34, 0x05, 0x0, 0x48, 0x65, 0x6c, 0x6c, 0x6f};
  uint8_t motor_packet[] = {0x2, 0x80, 0x08, 0x0, 0x0, 0x0, 0x80, 0x3f, 0x0, 0x0, 0x0, 0xbf};

  dispatcher(display_packet);

  printf("Done dispatcher \r\n");

  return 0;
}
