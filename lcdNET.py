#import
import RPi.GPIO as GPIO
import time
import commands

# Define GPIO to LCD mapping
LCD_RS = 18
LCD_E  = 23
LCD_D4 = 12 
LCD_D5 = 16
LCD_D6 = 20
LCD_D7 = 21
 
# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94
LCD_LINE_4 = 0xD4 
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
 
def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
 
  # Initialise display
  lcd_init()
 
  while True:
    print ifwifi()
    print ifcard()
    # Send some test
    lcd_string("Raspberry Pi",LCD_LINE_1)
    lcd_string("20x4 LCD Test",LCD_LINE_2)
    lcd_string("Silverlink RB",LCD_LINE_3)
    lcd_string("YULUN & Evan GOGO",LCD_LINE_4)
    time.sleep(5) # 5 second delay
		
    # Send some text
    lcd_string(get_date_now(),LCD_LINE_1)
    lcd_string(' '+get_time_now(),LCD_LINE_2)
    lcd_string("",LCD_LINE_3)
    lcd_string('ip:'+getip(),LCD_LINE_4)
    time.sleep(5) # 5 second delay

    # Send some text
    lcd_string("mobile internet("+ifnet()+")",LCD_LINE_1)
    lcd_string("sensor status:",LCD_LINE_2)
    lcd_string("  1   2   3   4   5",LCD_LINE_3)
    lcd_string(" (X) (O) (O) (X) (O)",LCD_LINE_4)
    time.sleep(5) # 5 second delay

 
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
    
    
def get_ip_info():
    return commands.getoutput('ifconfig wlan0|grep inet|awk -Faddr: \'{print $2}\'|awk \'{print $1}\'')
def get_ip2_info():
	return commands.getoutput('ifconfig ppp0|grep inet|awk -Faddr: \'{print $2}\'|awk \'{print $1}\'')
def ifwifi():
	wifi=get_ip_info()
	if(wifi==''):
		return False
	elif(wifi[0].isdigit()==False):
		return False
	else:
		i=0
		while (wifi[i].isdigit() or wifi[i]=='.'):
			i+=1
		wifi=wifi[0:i]
		return wifi
def ifcard():
	card=get_ip2_info()
	if(card==''):
		return False
	elif(card[0].isdigit()==False):
		return False
	else:
		return card
def ifnet():
	if ifwifi()!=False:
		return '1'
	elif ifcard()!=False:
		return '2'
	else:
		return 'X'
def getip():
	if ifnet()=='X':
		return 'no internet'
	elif ifnet()=='1':
		return ifwifi()
	elif ifnet()=='2':
		return ifcard()
def get_time_now():
    return time.strftime('    %H:%M:%S')
def get_date_now():
    return time.strftime('    %Y-%m-%d')
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
