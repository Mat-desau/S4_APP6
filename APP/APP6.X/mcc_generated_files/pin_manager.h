/**
  System Interrupts Generated Driver File

  @Company:
    Microchip Technology Inc.

  @File Name:
    pin_manager.h

  @Summary:
    This is the generated manager file for the MPLAB(c) Code Configurator device.  This manager
    configures the pins direction, initial state, analog setting.
    The peripheral pin select, PPS, configuration is also handled by this manager.

  @Description:
    This source file provides implementations for MPLAB(c) Code Configurator interrupts.
    Generation Information :
        Product Revision  :  MPLAB(c) Code Configurator - 4.85.0
        Device            :  PIC32MX370F512L
        Version           :  1.02
    The generated drivers are tested against the following:
        Compiler          :  XC32 1.42
        MPLAB             :  MPLAB X 3.55

    Copyright (c) 2013 - 2015 released Microchip Technology Inc.  All rights reserved.

    Microchip licenses to you the right to use, modify, copy and distribute
    Software only when embedded on a Microchip microcontroller or digital signal
    controller that is integrated into your product or third party product
    (pursuant to the sublicense terms in the accompanying license agreement).

    You should refer to the license agreement accompanying this Software for
    additional information regarding your rights and obligations.

    SOFTWARE AND DOCUMENTATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
    EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF
    MERCHANTABILITY, TITLE, NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.
    IN NO EVENT SHALL MICROCHIP OR ITS LICENSORS BE LIABLE OR OBLIGATED UNDER
    CONTRACT, NEGLIGENCE, STRICT LIABILITY, CONTRIBUTION, BREACH OF WARRANTY, OR
    OTHER LEGAL EQUITABLE THEORY ANY DIRECT OR INDIRECT DAMAGES OR EXPENSES
    INCLUDING BUT NOT LIMITED TO ANY INCIDENTAL, SPECIAL, INDIRECT, PUNITIVE OR
    CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, COST OF PROCUREMENT OF
    SUBSTITUTE GOODS, TECHNOLOGY, SERVICES, OR ANY CLAIMS BY THIRD PARTIES
    (INCLUDING BUT NOT LIMITED TO ANY DEFENSE THEREOF), OR OTHER SIMILAR COSTS.

*/

#ifndef _PIN_MANAGER_H
#define _PIN_MANAGER_H
/**
    Section: Includes
*/
#include <xc.h>
/**
    Section: Device Pin Macros
*/
/**
  @Summary
    Sets the GPIO pin, RB7, high using LATBbits.LATB7.

  @Description
    Sets the GPIO pin, RB7, high using LATBbits.LATB7.

  @Preconditions
    The RB7 must be set to an output.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    // Set RB7 high (1)
    channel_AN7_SetHigh();
    </code>

*/
#define channel_AN7_SetHigh()          LATBbits.LATB7 = 1
/**
  @Summary
    Sets the GPIO pin, RB7, low using LATBbits.LATB7.

  @Description
    Sets the GPIO pin, RB7, low using LATBbits.LATB7.

  @Preconditions
    The RB7 must be set to an output.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    // Set RB7 low (0)
    channel_AN7_SetLow();
    </code>

*/
#define channel_AN7_SetLow()           LATBbits.LATB7 = 0
/**
  @Summary
    Toggles the GPIO pin, RB7, using LATBbits.LATB7.

  @Description
    Toggles the GPIO pin, RB7, using LATBbits.LATB7.

  @Preconditions
    The RB7 must be set to an output.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    // Toggle RB7
    channel_AN7_Toggle();
    </code>

*/
#define channel_AN7_Toggle()           LATBbits.LATB7 ^= 1
/**
  @Summary
    Reads the value of the GPIO pin, RB7.

  @Description
    Reads the value of the GPIO pin, RB7.

  @Preconditions
    None.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    uint16_t portValue;

    // Read RB7
    postValue = channel_AN7_GetValue();
    </code>

*/
#define channel_AN7_GetValue()         PORTBbits.RB7
/**
  @Summary
    Configures the GPIO pin, RB7, as an input.

  @Description
    Configures the GPIO pin, RB7, as an input.

  @Preconditions
    None.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    // Sets the RB7 as an input
    channel_AN7_SetDigitalInput();
    </code>

*/
#define channel_AN7_SetDigitalInput()  TRISBbits.TRISB7 = 1
/**
  @Summary
    Configures the GPIO pin, RB7, as an output.

  @Description
    Configures the GPIO pin, RB7, as an output.

  @Preconditions
    None.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    // Sets the RB7 as an output
    channel_AN7_SetDigitalOutput();
    </code>

*/
#define channel_AN7_SetDigitalOutput() TRISBbits.TRISB7 = 0
/**
  @Summary
    Sets the GPIO pin, RG7, high using LATGbits.LATG7.

  @Description
    Sets the GPIO pin, RG7, high using LATGbits.LATG7.

  @Preconditions
    The RG7 must be set to an output.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    // Set RG7 high (1)
    channel_AN17_SetHigh();
    </code>

*/
#define channel_AN17_SetHigh()          LATGbits.LATG7 = 1
/**
  @Summary
    Sets the GPIO pin, RG7, low using LATGbits.LATG7.

  @Description
    Sets the GPIO pin, RG7, low using LATGbits.LATG7.

  @Preconditions
    The RG7 must be set to an output.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    // Set RG7 low (0)
    channel_AN17_SetLow();
    </code>

*/
#define channel_AN17_SetLow()           LATGbits.LATG7 = 0
/**
  @Summary
    Toggles the GPIO pin, RG7, using LATGbits.LATG7.

  @Description
    Toggles the GPIO pin, RG7, using LATGbits.LATG7.

  @Preconditions
    The RG7 must be set to an output.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    // Toggle RG7
    channel_AN17_Toggle();
    </code>

*/
#define channel_AN17_Toggle()           LATGbits.LATG7 ^= 1
/**
  @Summary
    Reads the value of the GPIO pin, RG7.

  @Description
    Reads the value of the GPIO pin, RG7.

  @Preconditions
    None.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    uint16_t portValue;

    // Read RG7
    postValue = channel_AN17_GetValue();
    </code>

*/
#define channel_AN17_GetValue()         PORTGbits.RG7
/**
  @Summary
    Configures the GPIO pin, RG7, as an input.

  @Description
    Configures the GPIO pin, RG7, as an input.

  @Preconditions
    None.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    // Sets the RG7 as an input
    channel_AN17_SetDigitalInput();
    </code>

*/
#define channel_AN17_SetDigitalInput()  TRISGbits.TRISG7 = 1
/**
  @Summary
    Configures the GPIO pin, RG7, as an output.

  @Description
    Configures the GPIO pin, RG7, as an output.

  @Preconditions
    None.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    // Sets the RG7 as an output
    channel_AN17_SetDigitalOutput();
    </code>

*/
#define channel_AN17_SetDigitalOutput() TRISGbits.TRISG7 = 0

/**
    Section: Function Prototypes
*/
/**
  @Summary
    Configures the pin settings of the PIC32MX370F512L
    The peripheral pin select, PPS, configuration is also handled by this manager.

  @Description
    This is the generated manager file for the MPLAB(c) Code Configurator device.  This manager
    configures the pins direction, initial state, analog setting.
    The peripheral pin select, PPS, configuration is also handled by this manager.

  @Preconditions
    None.

  @Returns
    None.

  @Param
    None.

  @Example
    <code>
    void SYSTEM_Initialize(void)
    {
        // Other initializers are called from this function
        PIN_MANAGER_Initialize();
    }
    </code>

*/
void PIN_MANAGER_Initialize(void);

#endif
