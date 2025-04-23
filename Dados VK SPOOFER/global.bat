@echo off
reg delete "HKLM\SOFTWARE\Microsoft\Cryptography" /v MachineGuid /f
rd /s /q "%LocalAppData%\DigitalEntitlements"
echo Sucesso!
pause
