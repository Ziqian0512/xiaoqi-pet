@echo off
rem Local resident services: SnowLuma (QQ alt account bridge) + pet_agent
rem ASCII only on purpose: cmd decodes .bat as GBK, Chinese comments break it.

set "SNOW=E:\snowluma"
set "PETAGENT=E:\dsh-pet-projects\dspet-main\deploy\pet_agent\pet_agent.py"
set "PYW=C:\Users\10943\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\pythonw.exe"

netstat -ano | findstr /R /C:":3001 .*LISTENING" >nul 2>&1
if errorlevel 1 (
  echo [start_agents] starting SnowLuma
  start "" /min "%SNOW%\launcher.bat"
) else (
  echo [start_agents] SnowLuma already running
)

netstat -ano | findstr /R /C:":8790 .*LISTENING" >nul 2>&1
if errorlevel 1 (
  if exist "%PETAGENT%" (
    echo [start_agents] starting pet_agent
    start "" /min "%PYW%" "%PETAGENT%"
  ) else (
    echo [start_agents] pet_agent.py not found, skip
  )
) else (
  echo [start_agents] pet_agent already running
)
