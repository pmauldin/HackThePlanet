/**
 * Read Contacts
 * by Aaron Zarraga - Sensel, Inc
 * 
 * This opens a Sensel sensor, reads contact data, and prints the data to the console.
 */

boolean sensel_sensor_opened = false;

int WINDOW_WIDTH_PX = 1150;
//We will scale the height such that we get the same aspect ratio as the sensor
int WINDOW_HEIGHT_PX;
SenselDevice sensel;

void setup() 
{
  DisposeHandler dh = new DisposeHandler(this);
  sensel = new SenselDevice(this);
  
  sensel_sensor_opened = sensel.openConnection();
  
  if(!sensel_sensor_opened)
  {
    println("Unable to open Sensel sensor!");
    exit();
    return; 
  }
  
  //Init window height so that display window aspect ratio matches sensor.
  //NOTE: This must be done AFTER senselInit() is called, because senselInit() initializes
  //  the sensor height/width fields. This dependency needs to be fixed in later revisions 
  WINDOW_HEIGHT_PX = (int) (sensel.getSensorHeightMM() / sensel.getSensorWidthMM() * WINDOW_WIDTH_PX);
  
  size(WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX);
  
  //Enable contact sending
  sensel.setFrameContentControl(SenselDevice.SENSEL_FRAME_CONTACTS_FLAG);
  
  //Enable scanning
  sensel.startScanning();
}

void draw() 
{
  if(!sensel_sensor_opened)
    return;
    
  background(0);
 
  SenselContact[] c = sensel.readContacts();
  
  if(c == null)
  {
    println("NULL CONTACTS");
    return;
  }
   
  for(int i = 0; i < c.length; i++)
  {
    int force = c[i].total_force;
    
    float sensor_x_mm = c[i].x_pos_mm;
    float sensor_y_mm = c[i].y_pos_mm;
    
    int screen_x = (int) (c[i].x_pos_mm / sensel.getSensorWidthMM()  * WINDOW_WIDTH_PX);
    int screen_y = (int) (c[i].y_pos_mm / sensel.getSensorHeightMM() * WINDOW_HEIGHT_PX);
    
    int id = c[i].id;
    int event_type = c[i].type;
    
    String event;
    switch (event_type)
    {
      case SenselDevice.SENSEL_EVENT_CONTACT_INVALID:
        event = "invalid"; 
        break;
      case SenselDevice.SENSEL_EVENT_CONTACT_START:
        event = "start";   
        break;
      case SenselDevice.SENSEL_EVENT_CONTACT_MOVE:
        event = "move";
        break;
      case SenselDevice.SENSEL_EVENT_CONTACT_END:
        event = "end";
        break;
      default:
        event = "error";
    }
    
    println("Contact ID " + id + ", event=" + event + ", mm coord: (" + sensor_x_mm + ", " + sensor_y_mm + "), force=" + force); 

    int size = force / 100;
    if(size < 10) size = 10;
    
    ellipse(screen_x, screen_y, size, size);
    
  }
  if(c.length > 0)
    println("****");
}

public class DisposeHandler 
{   
  DisposeHandler(PApplet pa)
  {
    pa.registerMethod("dispose", this);
  }  
  public void dispose()
  {      
    println("Closing sketch");
    if(sensel_sensor_opened)
    {
      sensel.stopScanning();
      sensel.closeConnection();
    }
  }
}
