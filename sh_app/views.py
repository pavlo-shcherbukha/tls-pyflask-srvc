from datetime import datetime
from operator import truediv
from flask import Flask, render_template, request, jsonify, Response
#from flask_talisman import Talisman, ALLOW_FROM
import json
import logging
import datetime
import sys
import os
import traceback

if os.environ.get("APP_DEBUG") == 'DEBUG_BRK':
    import debugpy
    print("===========1-DEBUG-BREAK======")
    breakpoint() 
    print("===========2-DEBUG-BREAK======")

application = Flask(__name__)
#Talisman(application)




class InvalidAPIUsageR(Exception):
    status_code = 400

    def __init__(self, code, message, target=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if code is not None:
            self.code = code 
        if target is not None:
            self.target = target
        else:
            self.target = ""
        self.payload = payload

    def to_dict(self):
        errdsc = {}
        errdsc["code"] = self.code
        errdsc["description"] = self.message
        errdsc["target"] = self.target
        rv={}
        rv["Error"]=errdsc
        rv["Error"]["Inner"]=dict(self.payload or ())
        return rv


@application.errorhandler(InvalidAPIUsageR)
def invalid_api_usager(e):
    r=e.to_dict()
    return json.dumps(r), e.status_code, {'Content-Type':'application/json'}





logging.basicConfig(filename='myapp.log', level=logging.DEBUG)

#===================================================
# Функція внутрішнього логера
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#===================================================
def log( a_msg='NoMessage', a_label='logger' ):
	dttm = datetime.datetime.now()
	ls_dttm = dttm.strftime('%d-%m-%y %I:%M:%S %p')
	logging.info(' ['+ls_dttm+'] '+ a_label + ': '+ a_msg)
	print(' ['+ls_dttm+'] '+ a_label + ': '+ a_msg)




#=================================================
# Головна сторінка
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================
@application.route("/")
def home():
    log("render home.html" )
    return render_template("home.html")


#=================================================
# Про програму
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================
@application.route("/about/")
def about():
    return render_template("about.html")

@application.route("/todo/")
def todo():
    return render_template("todo.html")

@application.route("/todocrt/", methods=["POST"])
def todo_create():
    body={}
    mimetype = request.mimetype
    print("mimetype = mimetype")
    label="todo_create"
    if mimetype == 'application/x-www-form-urlencoded':
        iterator=iter(request.form.keys())
        for x in iterator:
            body[x]=request.form[x]            
    elif mimetype == 'application/json':
        body = request.get_json()
    else:
        orm = request.data.decode()

    log('Body request' + json.dumps(  body ), label)
    res={}
    res["todo_id"]=body["todo_id"]
    res["todo_header"]=body["todo_header"]
    res["todo_owner"]=body["todo_owner"]
    log('Render result ' )
    return render_template("todo_res.html", data=res)   


#===========================================================================
#    *********** Сервісні  АПІ ******************************
#===========================================================================

# =================================================================================
# Метод health check
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Повертає {'success':True} якщо контейнер працює
# =================================================================================
@application.route("/api/health", methods=["GET"])
def health():
    title="Remote debug demo"
    label="health"
    result={}
    log('Health check', label)
    try:
        log('Health check' , 'health')
        result= {}
        result["message"]= title
        result["ok"]=True
        return json.dumps( result ), 200, {'Content-Type':'application/json'}
    except Exception as e: 
            ex_type, ex_value, ex_traceback = sys.exc_info()
            trace_back = traceback.extract_tb(ex_traceback)
            stack_trace = list()
            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
            #ex_code=e.code
            ex_name=ex_type.__name__
            ex_dsc=ex_value.args[0]

            result["ok"]=False
            result["message"]= title
            result["error"]=ex_dsc
            result["errorCode"]=ex_name
            result["trace"]=stack_trace 
            return json.dumps( result ), 422, {'Content-Type':'application/json'}



@application.route("/api/srvci", methods=["GET"])
def srvci():

    label="srvci"
    result={}
    result["DB_HOST"]=os.environ.get("DB_HOST")
    result["DB_PORT"]=os.environ.get("DB_PORT")
    result["DB_NAME"]=os.environ.get("DB_NAME")
    if result["DB_HOST"]==None:
        raise InvalidAPIUsageR( "InvalidAPIRequestParams",  "No  ENV [DB_HOST!]", target=label,status_code=422, payload = {"code": "NoDefined ENV", "description": "Not defined env variable DB_HOST" } )
    if result["DB_PORT"]==None:
        raise InvalidAPIUsageR( "InvalidAPIRequestParams",  "No  ENV [DB_PORT!]", target=label,status_code=422, payload = {"code": "NoDefined ENV", "description": "Not defined env variable DB_PORT" } )
    if result["DB_NAME"]==None:
        raise InvalidAPIUsageR( "InvalidAPIRequestParams",  "No  ENV [DB_NAME!]", target=label,status_code=422, payload = {"code": "NoDefined ENV", "description": "Not defined env variable DB_NAME" } )

    log('Відправляю результат: ', label)
    return json.dumps( result ), 200, {'Content-Type':'application/json'}
    


@application.route("/api/data", methods=["POST"])
def postdata():

    label="postdata"
    """
        Test http post
        request: { "typemsg": "warning|error|info", "textmsg": "this is message text"}
    """
    
    l_label='signreport';
    l_step='start'

    log(l_step, l_label)
    l_label=l_label + '_' + request.method

    l_req_body_dict={}
    l_types_of_msg = ( "warning", "error", "info" )
    res_body_dic={}

 
    l_step='getting request body'
    log(l_step, l_label)
    body = request.get_json()
    l_step='Request bidy: ' + json.dumps(  body )
    log(l_step, l_label)
    body_dict = dict(body)

    l_step='Check existanse key [typemsg]'
    log(l_step, l_label)
    if not 'typemsg' in body_dict:
        raise InvalidAPIUsageR( "InvalidAPIRequestParams",  "No key [typemsg]", target=l_label,status_code=422, payload = {"code": "NoKey", "description": l_step } )
    
    l_step='Check existanse key [textmsg]'
    if not 'textmsg' in body_dict:
        raise InvalidAPIUsageR( "InvalidAPIRequestParams",  "No key [textmsg]", target=l_label,status_code=422, payload = {"code": "NoKey", "description": l_step } )
    
    l_step='Check  apropreate values in [typemsg]'
    if not any( body_dict["typemsg"] in  typemsg for typemsg in l_types_of_msg ):
        raise InvalidAPIUsageR( "InvalidAPIRequestParams",  "No key [typemsg]", target=l_label,status_code=422, payload = {"code": "UnApropreateValue", "description": " must be  only (warning, error, info) " } )
   
    l_step="Prepare response OK"
    log(l_step, l_label)

    res={}
    res["ok"]=True
    res["message"]="Request processed"
    res["origreq"]=body_dict

    l_step="Send response OK: " + json.dumps(  res )
    log(l_step, l_label)

    return json.dumps(  res ), 200, {'Content-Type':'application/json'}
