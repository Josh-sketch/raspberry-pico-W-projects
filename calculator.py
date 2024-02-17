# NerdCave - https://www.youtube.com/channel/UCxxs1zIA4cDEBZAHIJ80NVg - Subscribe if you found this helpful.
# Github - https://github.com/Guitarman9119

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
matrix_keys = [['1', '2', '3', '+'],
               ['4', '5', '6', '-'],
               ['7', '8', '9', '*'],
               ['del', '0', '=', '/']]

# PINs according to schematic - Change the pins to match with your connections
keypad_rows = [2,3,4,5]
keypad_columns = [6,7,8,9]

myExpression = ""
operand1 = ""
operand2 = ""
operand3 = ""
operator1 = ""
operator2 = ""

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
    
##print("Please enter your Password")
lcd.move_to(5,0)
lcd.putstr("JOSH")
lcd.move_to(3,1)
lcd.putstr("CALCULATOR")
utime.sleep(1.0)
lcd.clear()

def assignprecedent(operator):
    if operator == "-":
        return 1
    elif operator == "+":
        return 2
    elif operator == "*":
        return 3
    elif operator == "/":
        return 4
    else:
        return 0

def applyoperator(a, b, operator):
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "/":
        return a / b
    elif operator == "*":
        return a * b

        
    
                       

def scankeys():  
    for row in range(4):
        for col in range(4):
            row_pins[row].high()
            key = None
            
            if col_pins[col].value() == 1:
                #print("You have pressed:", matrix_keys[row][col])
                key_press = matrix_keys[row][col]
                
                global myExpression
                global operand1
                global operand2
                global operand3
                global operator1
                global operator2
                if key_press == "=":
                    utime.sleep(0.3)
                    i = 0
                    while i < len(myExpression):
                        if myExpression[i].isdigit():
                            val = 0
                            while i < len(myExpression) and myExpression[i].isdigit():
                                 print("That means the operand has more digits")
                                 val = (val * 10) + int(myExpression[i])
                                 print(val)
                                 i += 1
                            if operand1 == "":
                                operand1 = val
                            elif operand1 != "" and operand2 == "":
                                operand2 = val
                            elif operand1 != "" and operand2 != "":
                                operand3 = val
                            
                        else:
                            print("it's an operator")
                            if operator1 == "":
                                operator1 = myExpression[i]
                            else:
                                operator2 = myExpression[i]
                            i += 1
                    print("Operand1: ", operand1)
                    print("Operator1: ", operator1, "Precedence: ", assignprecedent(operator1))
                    print("Operand2: ", operand2)
                    print("Operator2: ", operator2, "Precedence: ", assignprecedent(operator2))
                    print("Operand3: ", operand3)
                    
                        
                    if assignprecedent(operator1) > assignprecedent(operator2) and operand2 != "":
                        if assignprecedent(operator2) == 0:
                            result = applyoperator(operand1, operand2, operator1)
                        else:
                            firstStep = applyoperator(operand1, operand2, operator1)
                            result = applyoperator(firstStep, operand3, operator2)
                    elif assignprecedent(operator2) > assignprecedent(operator1) and operand2 != "":
                        firstStep = applyoperator(operand2, operand3, operator2)
                        result = applyoperator(operand1, firstStep, operator1)
                    else:
                        result = "math error"
                        
                            
                    print("Final answer: ", result)
                    final = str(result)
                    lcd.clear()
                    utime.sleep(0.1)
                    lcd.move_to(0,1)
                    lcd.putstr(final)
                    
                            
                elif key_press == "del":
                    myExpression = myExpression[:-1]
                    utime.sleep(0.1)
                    print(myExpression)
                    lcd.move_to(0,0)
                    lcd.putstr(" " * 16)
                    lcd.move_to(0,0)
                    lcd.putstr(myExpression)
                elif key_press == "=" and key_press == "del":
                    lcd.clear()
                    myExpression = ""
                    operand1 = ""
                    operand2 = ""
                    operand3 = ""
                    operator1 = ""
                    operator2 = ""
                else:
                    lcd.move_to(0,0)
                    lcd.putstr(" " * 16)
                    utime.sleep(0.2)
                    lcd.move_to(0,0)
                    lcd.putstr(key_press)
                    myExpression += key_press
                    print(myExpression)
                    lcd.move_to(0,0)
                    lcd.putstr(myExpression)
                    
                          
                    
                    
        row_pins[row].low()

while True:
    scankeys()
    