# Inmarsat IDP Plug-N-Play Dongle

The Plug-N-Play dongle is a small programmable single board computer in a
black box intended to be able to quickly demonstrate and prototype 
Internet-of-Things use cases enabled by satellite messaging connectivity.

The dongle connects directly to an **ST2100** satellite modem manufactured by
[ORBCOMM](www.orbcomm.com) and provides access to:

  * Serial communications using **AT commands**
  * Modem **event notification** via discrete output pin
  * Reset via external **reset** pin
  * 1 pulse-per-second (**PPS**) from GNSS timing via discrete output pin

The dongle can be configured to:

1. Pass through serial commands to a separate third party microcontroller
(default hardware configuration)
2. Act as the application microcontroller *(default when using this Python 
module)*
3. Act as a proxy intercepting communications from the modem to a third 
party microcontroller

