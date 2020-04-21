::Resets the volume mixer settings and services. Nice on Win 7 PCs with driver issues

@ECHO OFF

ECHO Reset Volume Mixer Settings...

NET STOP Audiosrv
NET STOP AudioEndpointBuilder

REG DELETE "HKCU\Software\Microsoft\Internet Explorer\LowRegistry\Audio\PolicyConfig\PropertyStore" /F
REG ADD "HKCU\Software\Microsoft\Internet Explorer\LowRegistry\Audio\PolicyConfig\PropertyStore"

NET START Audiosrv