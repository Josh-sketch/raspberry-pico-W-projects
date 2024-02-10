
from machine import Pin
import utime
import machine
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Create a map between keypad buttons and characters
matrix_keys = [['1', '2', '3', 'A'],
               ['4', '5', '6', 'B'],
               ['7', '8', '9', 'C'],
               ['*', '0', '#', 'D']]

# PINs according to schematic - Change the pins to match with your connections
keypad_rows = [2,3,4,5]
keypad_columns = [6,7,8,9]

## the keys entered by the user
myPassword = ""
#our secret pin, shhh do not tell anyone
secret_pin = "2596AD"

# Create two empty lists to set up pins ( Rows output and columns input )
col_pins = []
row_pins = []

# Loop to assign GPIO pins and setup input and outputs
for x in range(0,4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)
    
##############################Scan keys ####################
    
print("Please enter your Password")
lcd.move_to(0,0)
lcd.putstr("Enter Password:")
    
def scankeys():  
    for row in range(4):
        for col in range(4):
            row_pins[row].high()
            key = None
            
            if col_pins[col].value() == 1:
                print("You have pressed:", matrix_keys[row][col])
                key_press = matrix_keys[row][col]
                
                global myPassword
                if key_press == "#":
                    lcd.move_to(0,1)
                    lcd.putstr("....checking....")
                    utime.sleep(0.3)
                    if(myPassword == secret_pin):
                        lcd.clear()
                        lcd.move_to(0,0)
                        lcd.putstr("Correct Password")
                        utime.sleep(0.3)
                        lcd.move_to(2,1)
                        lcd.putstr("Safe unlocks")
                        utime.sleep(0.5)
                        lcd.clear()
                        lcd.move_to(3,0)
                        lcd.putstr("Welcome")
                        lcd.move_to(3,1)
                        lcd.putstr("Mr. Josh")
                        utime.sleep(0.3)
                        lcd.clear()
                        lcd.backlight_off()
                    else:
                        lcd.clear()
                        lcd.move_to(0,0)
                        lcd.putstr("Incorrect")
                        lcd.move_to(0,1)
                        lcd.putstr("Password")
                        utime.sleep(3)
                        lcd.clear()
                        myPassword = ""
                        lcd.move_to(0,0)
                        lcd.putstr("Enter Password:")
                        #machine.reset()
                        
                
                elif key_press == "*":
                    myPassword = myPassword[:-1]
                    utime.sleep(0.3)
                    print(myPassword)
                    lcd.move_to(0,1)
                    lcd.putstr(" " * 16)
                    lcd.move_to(0,1)
                    lcd.putstr(myPassword)
                    utime.sleep(0.1)
                    passLength = len(myPassword)
                    lcd.move_to(0,1)
                    lcd.putstr(" " * 16)
                    lcd.move_to(0,1)
                    lcd.putstr("*" * passLength)
              
                else:
                    lcd.move_to(0,1)
                    lcd.putstr(" " * 16)
                    utime.sleep(0.3)
                    lcd.move_to(0,1)
                    lcd.putstr(key_press)
                    myPassword += key_press
                    print(myPassword)
                    lcd.move_to(0,1)
                    lcd.putstr(myPassword)
                    utime.sleep(0.1)
                    passLength = len(myPassword)
                    lcd.move_to(0,1)
                    lcd.putstr(" " * 16)
                    lcd.move_to(0,1)
                    lcd.putstr("*" * passLength)
                          
               
                                 
                    
        row_pins[row].low()

while True:
    scankeys()
