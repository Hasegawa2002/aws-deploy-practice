\# 🦁 AI Image Classifier (ResNet50)



画像認識AIアプリです。

ユーザーがアップロードした画像を、Dockerコンテナ上で稼働するResNet50（ImageNet学習済みモデル）が解析し、何が写っているかを即座に判定します。



!\[Demo App](demo.png)



\## 🛠 Tech Stack (使用技術)



\* \*\*Frontend:\*\* Streamlit

\* \*\*Backend:\*\* FastAPI

\* \*\*ML Model:\*\* PyTorch (ResNet50)

\* \*\*Container:\*\* Docker

\* \*\*Infrastructure:\*\* AWS EC2 (Planned) / Local



\## 🏗 Architecture



ユーザーが画像をアップロードしてから、AIが判定するまでの流れです。



```mermaid

graph TD

&nbsp;   User((User)) -->|Upload Image| FE\[Frontend (Streamlit)]

&nbsp;   FE -->|POST /predict| API\[Backend API (FastAPI)]

&nbsp;   

&nbsp;   subgraph Docker Container

&nbsp;       API -->|Transform| Pre\[Preprocess]

&nbsp;       Pre -->|Tensor| Model\[ResNet50 (PyTorch)]

&nbsp;       Model -->|Top 3 Results| API

&nbsp;   end

&nbsp;   

&nbsp;   API -->|JSON Response| FE

&nbsp;   FE -->|Display Result| User

