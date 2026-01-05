from fastapi import FastAPI, File, UploadFile
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import io
import json
import urllib.request

app = FastAPI()

# --- 1. モデルとラベルの準備（起動時に1回だけ実行） ---
print("モデルを読み込んでいます...")
# 学習済みのResNet50をロード (weights="DEFAULT"で最新の重みを使用)
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval() # 推論モードに設定

# 画像の前処理ルールを作成
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# ImageNetのクラス名（1000種類）をダウンロード
url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
class_labels = json.loads(urllib.request.urlopen(url).read())
print("準備完了！")

@app.get("/")
def read_root():
    return {"message": "AI Server is Ready!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # --- 2. 画像の読み込み ---
        # アップロードされたファイルをバイナリとして読み込む
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert('RGB')

        # --- 3. 前処理と推論 ---
        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0) # バッチ次元を追加 (1, 3, 224, 224)

        with torch.no_grad():
            output = model(input_batch)

        # --- 4. 結果の整形（トップ3を取得） ---
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top3_prob, top3_id = torch.topk(probabilities, 3)

        results = []
        for i in range(3):
            results.append({
                "rank": i + 1,
                "label": class_labels[top3_id[i]], # クラス名を取得
                "score": f"{top3_prob[i].item() * 100:.2f}%"
            })

        return {"prediction": results}

    except Exception as e:
        return {"error": str(e)}