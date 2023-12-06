import os
import json
from flask import (Flask, request, render_template)

appinsight=''
config_settings=''

### Managed Identity Credentials ###
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()

### Azure App Configuration ###
from azure.appconfiguration import AzureAppConfigurationClient
AppConfigUrl = "https://appcs-demo.azconfig.io"
AppConfigClient = AzureAppConfigurationClient(AppConfigUrl, credential)

AppConfig_test = AppConfigClient.get_configuration_setting(key="test")



### APP ###

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

if appinsight:
    from opencensus.ext.azure.trace_exporter import AzureExporter
    from opencensus.ext.flask.flask_middleware import FlaskMiddleware
    from opencensus.trace.samplers import ProbabilitySampler
    # For website monitoring
    AzureAppInsights_ConnectionString = 'InstrumentationKey=3712782d-691c-47d4-bef1-52ae3c0f7dc1;IngestionEndpoint=https://northeurope-2.in.applicationinsights.azure.com/;LiveEndpoint=https://northeurope.livediagnostics.monitor.azure.com/'

    if AzureAppInsights_ConnectionString:
        middleware = FlaskMiddleware(
            app,
            exporter=AzureExporter( connection_string=AzureAppInsights_ConnectionString ),
            sampler=ProbabilitySampler(rate=1.0),
        )

@app.route('/')
def index():
    args = request.args
    arg_search = args.get("search")

    get_request = {}
    if arg_search != '':
        get_request['search'] = arg_search

    return render_template('index.html', request=get_request, config_settings="")

@app.route('/appconfig')
def appconfig():
    return render_template('index.html', config_settings=config_settings)
