from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="DMETE8WfmmDIeq9PA6Sf"
)


img = "../dataset/01.png"

result = CLIENT.infer(img, model_id="forest-analysis/22")

print(result)