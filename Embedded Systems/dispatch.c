#include <stdint.h>
#include <stdio.h>
#define DISPLAY_MESSAGE 0x34
#define MOTOR_MESSAGE 0x80


// Handle Display messages
void display_message(uint8_t *m, uint16_t message_len){

    for(int i = 0; i < message_len; ++i)
      printf("%c ", m[i]);

    printf("\r\n");
}

// Handle Motor messages
void update_motor(float forward_back, float left_right){

  printf("Forward Back %d \r\n", forward_back);
  printf("Left Right   %d \r\n", left_right);

}

void dispatcher(uint8_t *packet){
  
  uint8_t  packet_id    = packet[0];
  uint8_t  message_type = packet[1];
  uint16_t message_len  = packet[2] || (packet[3] << sizeof(uint8_t));


  printf("Packet ID %d \r\n", packet_id);
  printf("Type      %x \r\n", message_type);
  printf("Length    %d \r\n", message_len);

  if(message_type == DISPLAY_MESSAGE){
    uint8_t message[message_len];
    for(int i = 0; i < message_len; ++i)
      message[i] = packet[4 + i];

    display_message(message, message_len);

  } else {
    float forward_back = (float) packet[4];
    float left_right   = (float) packet[8];

    for(int i = 1; i < 4; ++i){
      forward_back |= (float) (packet[4 + i] << sizeof(uint8_t) * i);
      left_right   |= (float) (packet[8 + i] << sizeof(uint8_t) * i);
    }

    update_motor(forward_back, left_right); 
    
  }
}


int main(){

  uint8_t display_packet[] = {0x1, 0x34, 0x05, 0x0, 0x48, 0x65, 0x6c, 0x6c, 0x6f};
  uint8_t motor_packet[] = {0x2, 0x80, 0x08, 0x0, 0x0, 0x0, 0x80, 0x3f, 0x0, 0x0, 0x0, 0xbf};

  dispatcher(display_packet);

  printf("Done dispatcher \r\n");

  return 0;
}
