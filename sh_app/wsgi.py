
from sh_app.webapp import application as application
##from webapp import application as application
##from werkzeug import serving
from flask_sslify import SSLify
import ssl

#if __name__ == "__main__":
#    application.run()

# "./tlscert/server-crt.pem"
# "./tlscert/server-key.pem"
# "./tlscert/ca-crt.pem"
#if __name__ == "__main__":

#    from flask_talisman import Talisman
#    application.run(debug=True, ssl_context=('./tlscert/server-crt.pem', './tlscert/server-key.pem', './tlscert/ca-crt.pem'))

context=None
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.load_default_certs(purpose=Purpose.SERVER_AUTH)
#context.load_cert_chain("./sh_app/tlscert/server-crt.pem", "./sh_app/tlscert/server-key.pem")
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
if __name__ == "__main__":
    ## application.run(debug=False, ssl_context=context)
    #application.run(debug=True, ssl_context=context)
    ##sslify = SSLify(application)
    application.run(ssl_context='adhoc')