/*
* implement tree view to browse devices
* devices
*   device-1
*       one wire ifcs
*           ifc-1
*           ifc-2
*       relays
*           relay-1
*           relay-21
*   device-2
*       one wire ifcs
*           ifc-1
*       relays
*           relay-1
*           relay-2
*           relay-3
* */

function Device(name, device_div, url) {
    this.name = name;
    this.url = url;
}



