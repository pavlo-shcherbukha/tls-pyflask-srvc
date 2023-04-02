# tls-pyflask-srvc Запуск Python-Flask application за https.

## Постановка проблеми

В рамках OpenShift  портібно забезепечити коммунікацію з python flask  додатками, використовуючи захищений транспртний рівеь (tls), а простіше по https://. В деяких випадках tls  можна дотягти тільки до роутера openshift.  А в деяких  - потрібно тягти tls  до самого додатку. 
В цьому репозиторіх показно як запустити в продуктивному середовищі python flask  сервіси, використовуючи tls. 

Це правда, не дає відповіді, як запустити за tls Python service в режимі розробки чи remote debug.  Я проце поки тільки думаю. Ще не тестував.

## Орис простого Python flask сервісу та запуск його локально.

Для тестування розроблено простий Python Flask  сервіс, що має кілька html сторінок серверного рендеригу, включно з HTTP-POST  формою, та кілька rest методів.

### розгортання додатку локально

- Склонувати git repo

```bash
git clone https://github.com/pavlo-shcherbukha/tls-pyflask-srvc.git -b main
```

- створити virtual env  для запуску python [Python - flask start. Створення віртуального середовища ](https://pavlo-shcherbukha.github.io/posts/2022-09-02/python-flask-1/#p-3.2)

```bash
py -m venv env
.\env\Scripts\activate.ps1 
```

- встановити необхідні залежності [Python - flask start. Установка необхідних бібіліотек ](https://pavlo-shcherbukha.github.io/posts/2022-09-02/python-flask-1/#p-3.2)

```bash
py -m pip install -r requirements.txt
```

- запустити додаток в режимі локального debug

Додатко доступний по url: **http://localhost:5010**

Як запустити в режимі debug локально  з Vsc показанона [pic-01](#pic-01).

<kbd><img src="doc/pic-01.png" /></kbd>
<p style="text-align: center;"><a name="pic-01">pic-01</a></p>


### Опис  функціональності додатку

####   Http-GET /api/health Метод перевірки працездатності 

Метод повертає простий JSON  з фіксованими параметрами

```json

{
  "message": "For TLS demo",
  "ok": true
}

```

####   Http-GET /api/srvci Метод що повертає значення env  змінних, або помилку, якщо якихось змінних не вситачає


- Response-OK

```json
{
  "DB_HOST": "pfu-couchdb",
  "DB_PORT": "80",
  "DB_NAME": "shdb"
}
```

- Response-Err

```json
{
  "Error": {
    "code": "InvalidAPIRequestParams",
    "description": "No  ENV [DB_HOST!]",
    "target": "srvci",
    "Inner": {
      "code": "NoDefined ENV",
      "description": "Not defined env variable DB_HOST"
    }
  }
}

```

### Опис UI

Приклад UI показано на [pic-02](#pic-02).

<kbd><img src="doc/pic-02.png" /></kbd>
<p style="text-align: center;"><a name="pic-02">pic-02</a></p>

Тобто UI має кільа html get  та одну форму ввода з html post меню: "todo". В форму можна ввести todo,  а потім отримати відповідь, з  введеними данними.


## Розгортання в openshfit
### Підготовка середовища виконання

- Створиnи собі openshift sandbox як поисано за лінком [create openshift sendbox](https://github.com/pavlo-shcherbukha/google-sheet-to-db#create-openshift-sendbox). 

- Розгорнути openshift crc platform [ A minimal OpenShift Container Platform 4 cluster and Podman container runtime to your local computer](https://crc.dev/crc/).

- Використати існуючий корпоративний openshift, якщо це  допустимо.

Особисто я віддаю перевагу використанню openshift sandbox.

В проекті існує 2 приклади deployment:

- **\openshift\ubi8_docker_deployment**  TLS  доходить до Flask application

- **\openshift-tls-edge\ubi8_docker_deployment** TSL  доходить тількт до route openshift,  а далі трафік уже не захищений.

В варіанті **\openshift\ubi8_docker_deployment** python запускається за gunicorn, тому ніяких змін в python код вносити не потрібно. Потрібно зробити 2 кроки, а саме:

- всі кореневі  (CA) сертифікати, що є в ланцюжку потрібно покласти в трастове сховище Linux. Це робиться при зборці docke image і описується Dockerfile.

Ось цитата з Dockerfile, для Redhat Ubi8-python базового образу

```bash
# Put self signed CA into trust store
RUN cp /tmp/src/sh_app/tlscert/ca-crt.pem /usr/share/pki/ca-trust-source/anchors/
RUN ls /usr/share/pki/ca-trust-source/anchors/
RUN update-ca-trust

```

- Серврений ключ та серверний сертифікат вносяться в спеціальні ключі командного рядку при запуску gunicorn: --keyfile --certfile 

```yaml
        spec:
          containers:
          - env:
            - name: GUNICORN_CMD_ARGS
              value: --workers=1 --worker-connections=2000  --bind=0.0.0.0:8080 --access-logfile=---keyfile /opt/app-root/src/sh_app/tlscert/server-key.pem --certfile /opt/app-root/src/sh_app/tlscert/server-crt.pem


```
Ну і далі в програмному коді нічго міняти не портібно в Deploymentconfig  також ні, окрім роутера. В роутері додається додатковий ключ **tls** із значеннмя termination: passthrough 

```yaml
    spec:
      host: "${HOSTNAME}"
      port:
        targetPort: ${{PORTNUMBER}}
      # новий розділ start  
      tls:
        termination: passthrough
      # новий розділ stop  
      to:
        kind: "Service"
        name: ${APP_SERVICE_NAME}
        weight: null


```


- В варіанті **\openshift-tls-edge\ubi8_docker_deployment**  запуск самого додатку взагалі ніяк не відрізняється від запуску в режимі без захисту. Але основні зміни виконуються в роутері. Створюється так званий edg- роутер, куди додаються зненеровані CA та серврені ключ та сертифікат.

В роутері з`являється ноий блок **tls**, куди  вносяться сертифікати та ключі

```yaml
    spec:
      host: "${HOSTNAME}"
      port:
        targetPort: ${{PORTNUMBER}}
      # новий розділ start  
      tls:
        termination: edge
        certificate: |
          -----BEGIN CERTIFICATE-----
          # 
          -----END CERTIFICATE-----
        key: |
          -----BEGIN PRIVATE KEY-----

          -----END PRIVATE KEY-----
        caCertificate: |
          -----BEGIN CERTIFICATE-----
   
          -----END CERTIFICATE-----
        insecureEdgeTerminationPolicy: Allow
      wildcardPolicy: None
      # новий розділ stop
      to:
        kind: "Service"

```


### Генерація сертифікатів TLS

Принципи та послідовність короків для генераціх сертифікатів  описана за [tls-self-sign-certs Набрі кроків для генерації самопідписних TLS сертифікатів](https://github.com/pavlo-shcherbukha/tls-self-sign-certs#readme). 

- Для варіанту **\openshift\ubi8_docker_deployment** достатньо поміняти тільки свої реквізити в конфігураційних файлах openssl в розділі req_distinguished_name, залишивши localhost в CN  для серверного сертифікату.

Для варіанту **\openshift-tls-edge\ubi8_docker_deployment** в сертифікатах в реквізиті CN  вказував маску URL в ca.cnf  та в server.cnf 

```text
CN                     = *.apps.sandbox-myowndomain.openshiftapps.com
```

Використовується серверна аутентифікація. Тому у відповідності з посиланням- сертифікати генеруються в 4 кроки.


### Deployment в openshift **\openshift\ubi8_docker_deployment**
- Налаштувати **login.cmd**, вказавши  логін токен, DNS openshift, назву namespace
- Налаштувати secret github у файлі login.cmd secret-github-basicauth.yaml  та створити secret командою 

```bash
oc create -f secret-github-basicauth.yaml 

```

- Перевірити на налаштувати, якщо порібно параметри deployment в файлі **srvc-process.cmd**.  

- Запустити  **srvc-process.cmd** потім зайти в openshift і  натиснути build. В даному випадку створиться і запуститься сам доадток

- Запустити  **route-process.cmd**. В даному випдку запутиться роутер.

Якщо все зролено правильно то зайшовши по створеному роутеру у вас додаток повинен працювати так, я к і на laptop локально.


#### Deployment в openshift  **\openshift-tls-edge\ubi8_docker_deployment**

- Налаштувати **login.cmd**, вказавши  логін токен, DNS openshift, назву namespace
- Налаштувати secret github у файлі login.cmd secret-github-basicauth.yaml  та створити secret командою 

```bash
oc create -f secret-github-basicauth.yaml 

```

- Перевірити на налаштувати, якщо порібно параметри deployment в файлі **srvc-process.cmd**.  

- Запустити  **srvc-process.cmd** потім зайти в openshift і  натиснути build. В даному випадку створиться і запуститься сам доадток

- Запустити  **route-edge-process.cmd **. В даному випадку створиться роутер доступний по https.
- Запустити  **route-clr-process.cmd **. В даному випадку створиться роутер доступний по http.


Якщо все зролено правильно то зайшовши по створенbv роутерам у вас додаток повинен працювати так, я к і на laptop локально.



