import os
from flask import Flask, request, render_template
from azure.appconfiguration.provider import load, SettingSelector
from azure.identity import DefaultAzureCredential


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


credential = DefaultAzureCredential()

### Azure App Configuration ###
from azure.appconfiguration import AzureAppConfigurationClient
AppConfigUrl = "https://appcs-demo.azconfig.io"
azure_app_config = load(
                        endpoint=AppConfigUrl,
                        keyvault_credential=credential,
                        credential=credential
                   )


### App Insights ###
AzureAppInsights_ConnectionString=''
AzureAppInsights_ConnectionString = azure_app_config.get_configuration_setting(key="appinsight")
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

    return render_template('index.html', request=get_request, azure_app_config="")

@app.route('/appconfig')
def appconfig():
    return render_template('index.html', azure_app_config=azure_app_config)
