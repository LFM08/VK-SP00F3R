@echo off
:menu
cls
echo ====================================
echo          Painel de Acesso
echo ====================================
echo [1] Login
echo [2] Registrar
echo [3] Sair
echo ====================================
set /p opcao=Escolha uma opcao: 

if "%opcao%"=="1" goto login
if "%opcao%"=="2" goto registrar
if "%opcao%"=="3" exit

:login
cls
echo ====================================
echo               Login
echo ====================================
set /p nome=Digite seu nome: 
set /p senha=Digite sua senha: 

:: Obtém o IP público do usuário
set ip=
for /f "delims=" %%i in ('powershell -Command "Invoke-RestMethod http://api.ipify.org"') do set ip=%%i

:: Verifica se o IP foi obtido corretamente
if "%ip%"=="" (
    echo Falha ao obter o IP publico.
    pause
    goto menu
)

:: Chama o script Python para verificar o login e validar o IP
python database.py login "%nome%" "%senha%" "%ip%"
if %errorlevel% neq 0 (
    echo Nome ou senha invalidos, ou IP nao autorizado.
    pause
    goto menu
)

echo Login bem-sucedido!
pause
goto spoofer_global

:registrar
cls
echo ====================================
echo             Registrar
echo ====================================
set /p nome=Digite seu nome: 
set /p senha=Digite sua senha: 
set /p chave=Digite sua chave de acesso: 

:: Obtém o IP público do usuário
set ip=
for /f "delims=" %%i in ('powershell -Command "Invoke-RestMethod http://api.ipify.org"') do set ip=%%i

:: Verifica se o IP foi obtido corretamente
if "%ip%"=="" (
    echo Falha ao obter o IP publico.
    pause
    goto menu
)

:: Chama o script Python para registrar o usuario e validar a chave
python database.py registrar "%nome%" "%senha%" "%chave%" "%ip%"
if %errorlevel% neq 0 (
    echo Chave invalida ou ja usada. Tente novamente.
    pause
    goto menu
)

echo Registro bem-sucedido!
pause
goto menu

:spoofer_global
cls
echo ====================================
echo          Spoofer Global
echo ====================================
echo [1] Executar Spoofer
echo [2] Consultar tempo de key
echo [3] Voltar ao Menu Principal
echo ====================================
set /p opcao_spoofer=Escolha uma opcao: 

if "%opcao_spoofer%"=="1" goto executar_spoofer
if "%opcao_spoofer%"=="2" goto consultar_tempo_key
if "%opcao_spoofer%"=="3" goto menu

:executar_spoofer
cls
echo ====================================
echo           Executando Spoofer
echo ====================================
echo Spoofando...

:: Removendo MachineGuid do registro
echo Removendo MachineGuid do registro...
reg delete "HKLM\SOFTWARE\Microsoft\Cryptography" /v MachineGuid /f >nul 2>&1
if %errorlevel% neq 0 (
    echo Falha ao remover MachineGuid.
    pause
    goto spoofer_global
)

:: Removendo pasta DigitalEntitlements
echo Removendo pasta DigitalEntitlements...
rd /s /q "%LocalAppData%\DigitalEntitlements" >nul 2>&1
if %errorlevel% neq 0 (
    echo Falha ao remover a pasta DigitalEntitlements.
    pause
    goto spoofer_global
)

:: Mensagem de sucesso
echo Sucesso!
pause
goto spoofer_global

:consultar_tempo_key
cls
echo ====================================
echo        Consultar Tempo de Key
echo ====================================
python database.py consultar_tempo_key "%nome%"
if %errorlevel% neq 0 (
    echo Erro ao consultar o tempo da chave.
    pause
    goto spoofer_global
)
pause
goto spoofer_global