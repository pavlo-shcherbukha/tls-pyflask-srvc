@echo off

echo **************************************************************
echo * oc login --server%OC_URL% --token=%OC_TOKEN%
echo * oc login --server%OC_URL% -u %OC_USER% -p %OC_PSW%
echo * HOW TO GET API URL:
echo * oc config view --minify -o jsonpath='{.clusters[*].cluster.server}'
echo **************************************************************

  set OC_URL=https://api.<openhsift dns>.com:6443
  set OC_TOKEN=<token>


  set APP_DNS=apps.<openhsift dns>
  set APP_PROJ=<openshift project (namespace)>

if "%OC_URL%" == "" (
   echo ===========================================
   echo Undefined cluster URL
   echo set env variable OC_URL
   echo ===========================================
   pause
   goto l_exit
)   


if "%OC_TOKEN%" == "" (
   echo ===========================================
   echo Undefined opensshift login token
   echo set env variable OC_TOKEN
   echo ===========================================
   pause
   goto l_exit
)   


echo oc login --token=%OC_TOKEN% --server=%OC_URL%
oc login --token=%OC_TOKEN% --server=%OC_URL%


:l_exit  

