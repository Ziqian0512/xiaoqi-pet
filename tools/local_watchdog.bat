@echo off
rem Local watchdog: every 120s check SnowLuma (:3001) and pet_agent (:8790); restart if missing.
rem ASCII only on purpose: cmd decodes .bat as GBK, Chinese comments break it.
set "LOG=E:\dsh-pet-projects\logs\local-watchdog.log"
if not exist "E:\dsh-pet-projects\logs" mkdir "E:\dsh-pet-projects\logs"

:loop
netstat -ano | findstr /R /C:":3001 .*LISTENING" >nul 2>&1
if errorlevel 1 (
  echo [%date% %time%] SnowLuma down, restarting >> "%LOG%"
  start "" /min "E:\dsh-pet-projects\tools\start_agents.bat"
)

netstat -ano | findstr /R /C:":8790 .*LISTENING" >nul 2>&1
if errorlevel 1 (
  echo [%date% %time%] pet_agent down, restarting >> "%LOG%"
  start "" /min "E:\dsh-pet-projects\tools\start_agents.bat"
)

rem ping instead of timeout: timeout fails when stdin is redirected
ping -n 121 127.0.0.1 >nul
goto loop
