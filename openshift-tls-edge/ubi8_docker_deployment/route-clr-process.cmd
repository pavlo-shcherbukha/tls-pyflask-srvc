@echo on
call ..\login.cmd
oc project %APP_PROJ%
pause

set fltempl=pycrl-ubi8docker-route-temp.yaml
set fldepl=pycrl-ubi8docker-route-depl.yaml
 

echo %APP_PROJ% .....

echo %APP_DNS%   .....

set APP_SERVICE_NAME=pyedge-ubi8docker-srvc
set APP_NAME=py-tls
set ROUTENAME=pycrl-ubi8docker-srvc-%APP_PROJ%.%APP_DNS%
set SRVHOSTNAME=pycrl-1ubi8docker-srvc-%APP_PROJ%.%APP_DNS%
set PORTNUMBER=8080


echo APP_SERVICE_NAME=%APP_SERVICE_NAME%
echo APP_NAME=%APP_NAME%
echo ROUTENAME=%ROUTENAME%
echo SRVHOSTNAME=%SRVHOSTNAME%
echo PORTNUMBER=%PORTNUMBER%


pause



oc delete -f %fldepl%

pause
oc process -f %fltempl% --param=NAMESPACE=%APP_PROJ% --param=APP_SERVICE_NAME=%APP_SERVICE_NAME% --param=APP_NAME=%APP_NAME% --param=ROUTENAME=%ROUTENAME% --param=HOSTNAME=%SRVHOSTNAME% --param=PORTNUMBER=%PORTNUMBER% -o yaml > %fldepl% 
pause
oc create -f %fldepl%
pause
 
     
     
     
