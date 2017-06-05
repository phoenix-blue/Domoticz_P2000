Info:
This script is build to import P2000 messgaes (only used in the Netherlands) that will only check if there is an active "GRIP" messages.
After import it will compare the location with the GPS location that is set into the script.

When the result is positive it will send the info to Domoticz to control for example the home ventilation system.

Setup:
First create an virtual Alert device into domoticz to push the info to and setup inside this script the following info:

domoticz_server = "http://localhost"
domoticz_port = 8080
domoticz_device = 1
alert_range = 25  # in km
llatHome = xx.xxxxx
lngHome = xx.xxxx

Note: The script is also able to check the GPS location from Domoticz.

Finish:
Made an cronejob to run this script every x time to check the P2000 server.
For test you can set the random_debug to 1 to send GRIP alerts to domotics when needed.


Things to do:
- Insert an option to send messages 1 time so there are no double messages in the system.
- Dubug the default level to green when there is no actual message.
