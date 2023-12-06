import os
import json
from flask import (Flask, request, render_template)

### Managed Identity Credentials ###
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()

### Azure App Configuration ###
from azure.appconfiguration import AzureAppConfigurationClient
AppConfigUrl = "https://appcs-demo.azconfig.io"
AppConfigClient = AzureAppConfigurationClient(AppConfigUrl, credential)

### APP ###
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

### App Insights ###
AzureAppInsights_ConnectionString=''
#AzureAppInsights_ConnectionString = AppConfigClient.get_configuration_setting(key="appinsight")
if AzureAppInsights_ConnectionString:
    from opencensus.ext.azure.trace_exporter import AzureExporter
    from opencensus.ext.flask.flask_middleware import FlaskMiddleware
    from opencensus.trace.samplers import ProbabilitySampler
    # For website monitoring
    middleware = FlaskMiddleware(
        app,
        exporter=AzureExporter( connection_string=AzureAppInsights_ConnectionString ),
        sampler=ProbabilitySampler(rate=1.0),
    )

### Test Config ###
testconfig=''
testconfig = AppConfigClient.get_configuration_setting(key="test")

@app.route('/')
def index():
    args = request.args
    arg_search = args.get("search")

    get_request = {}
    if arg_search != '':
        get_request['search'] = arg_search

    return render_template('index.html', request=get_request, testconfig="")

@app.route('/appconfig')
def appconfig():
    return render_template('index.html', testconfig=testconfig)
