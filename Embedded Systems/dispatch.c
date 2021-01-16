#define DISPLAY_MESSAGE 0x34
#define MOTOR_MESSAGE 0x80


// Handle Display messages
int display_message(Message m){

  return 1;
}

// Handle Motor messages
int update_motor(Message m){

  return 1;
}

int dispatcher(int packet){
  
  char packet_id;
  char message_type;
  short message_length;

  char message_data[message_length];


  return 0;
}
