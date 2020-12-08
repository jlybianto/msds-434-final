from google.cloud import automl
from google.oauth2 import service_account

def get_prediction(file_path):

    project_id = "msds-434-final"
    model_id = "ICN7344581542892535808"
    # file_path = "uploads/city.png" ## for local image testing

    credentials = service_account.Credentials.from_service_account_file("/home/jesse_lybianto/msds-434-final/msds-434-final-db35f3a74a12.json")
    prediction_client = automl.PredictionServiceClient(credentials=credentials)

    # Get the full path of the model.
    model_full_id = automl.AutoMlClient.model_path(
        project_id, "us-central1", model_id
    )

    # Read the file.
    with open(file_path, "rb") as content_file:
        content = content_file.read()

    image = automl.Image(image_bytes=content)
    payload = automl.ExamplePayload(image=image)

    # params is additional domain-specific parameters.
    # score_threshold is used to filter the result
    # https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#predictrequest
    params = {"score_threshold": "0.0"}

    request = automl.PredictRequest(
        name=model_full_id,
        payload=payload,
        params=params
    )
    response = prediction_client.predict(request=request)
    print(response.payload)
    return response.payload

    # For non-modular console output
    # print("Prediction results:")
    # for result in response.payload:
    #     print("Predicted class name: {}".format(result.display_name))
    #     print("Predicted class score: {}".format(result.classification.score))