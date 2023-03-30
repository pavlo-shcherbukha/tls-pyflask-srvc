from sh_app.webapp import application as application
##from werkzeug import serving
#from flask_sslify import SSLify
import ssl

#if __name__ == "__main__":
#    application.run()
# "./sh_app/tlscert/server-crt.pem"
# "./sh_app/tlscert/server-key.pem"
# "./sh_app/tlscert/ca-crt.pem"
#if __name__ == "__main__":
#    from flask_talisman import Talisman
#    application.run(debug=True, ssl_context=('./tlscert/server-crt.pem', './tlscert/server-key.pem', './tlscert/ca-crt.pem'))

# TODO: https security
HTTPS_ENABLED = True
VERIFY_USER = True

API_HOST = "0.0.0.0"
API_PORT = 5000
API_CRT = "./sh_app/tlscert/server-crt.pem"
API_KEY = "./sh_app/tlscert/server-key.pem"
API_CA_T = "./sh_app/tlscert/server-crt.pem"
context=None
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
if(VERIFY_USER):
    context.verify_mode = ssl.CERT_OPTIONAL    #  ssl.CERT_REQUIRED
    context.load_verify_locations(API_CA_T)

    try:
        context.load_cert_chain(API_CRT, API_KEY)
    except Exception as e:
        print(e)

if __name__ == "__main__":

    application.run(debug=True, ssl_context=context, host='localhost', port=API_PORT)
