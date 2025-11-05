import azure.functions as func
import logging

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="test-hub",
                               connection="d2t012eventhub_RootManageSharedAccessKey_EVENTHUB") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))


# This example uses SDK types to directly access the underlying EventData object provided by the Event Hubs trigger.
# To use, uncomment the section below and add azurefunctions-extensions-bindings-eventhub to your requirements.txt file
# Ref: aka.ms/functions-sdk-eventhub-python
#
# import azurefunctions.extensions.bindings.eventhub as eh
# @app.event_hub_message_trigger(
#     arg_name="event", event_hub_name="test-hub", connection="d2t012eventhub_RootManageSharedAccessKey_EVENTHUB"
# )
# def eventhub_trigger(event: eh.EventData):
#     logging.info(
#         "Python EventHub trigger processed an event %s",
#         event.body_as_str()
#     )

@app.function_name(name="eventhub_output")
@app.route(route="eventhub_output", methods=["POST"])
# test-hub3와 el31eventhub_RootMangeSharedAccessKey~~ 부분은 본인이 생성한 환경과 동일하게 설정하세요.
@app.event_hub_output(arg_name="event", event_hub_name="test-hub", connection="d2t012eventhub_RootManageSharedAccessKey_EVENTHUB")
def eventhub_output(req: func.HttpRequest, event: func.Out[str]) -> func.HttpResponse:
    req_body = req.get_body().decode('utf-8')

    logging.info("HTTP trigger function received a request: %s", req_body)

    event.set(req_body)

    return func.HttpResponse("Event Hub output function executed successfully.", status_code=200)