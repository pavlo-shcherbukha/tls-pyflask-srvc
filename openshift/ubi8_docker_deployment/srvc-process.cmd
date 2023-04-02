@echo off
call ..\login.cmd
oc project %APP_PROJ%
pause

set fltempl=py-ubi8docker-srvc-templ.yaml
set fldepl=py-ubi8docker-srvc-depl.yaml 
oc delete -f %fldepl%
set APP_SERVICE_NAME=pytls-ubi8docker-srvc
set APP_NAME=py-tls
set GIT_BRANCH=tz-000001-init
set GIT_URL=https://github.com/pavlo-shcherbukha/tls-pyflask-srvc.git
set DOCKER_PTH=./openshift/ubi8_docker_deployment/Dockerfile

oc delete -f %fldepl%
pause
oc process -f %fltempl%  --param=NAMESPACE=%APP_PROJ% --param=APP_SERVICE_NAME=%APP_SERVICE_NAME% --param=APP_NAME=%APP_NAME% --param=GIT_BRANCH=%GIT_BRANCH% --param=GIT_URL=%GIT_URL% --param=DOCKER_PTH=%DOCKER_PTH% -o yaml > %fldepl% 
pause
oc create -f %fldepl%
pause

 