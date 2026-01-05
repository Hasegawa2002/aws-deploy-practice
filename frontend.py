import streamlit as st
import requests

st.title("画像判定アプリ")
st.write("画像をアップロードすると判定します")

api_url = st.sidebar.text_input("API URL", "http://localhost:8000/predict")
uploaded_file = st.file_uploader("画像をドラッグ＆ドロップ", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="アップロードされた画像", use_column_width=True)

    if st.button('判定する'):
        try:
            files = {"file": uploaded_file.getvalue()}

            with st.spinner("処理中…"):
                response = requests.post(api_url, files=files)
            
            if response.status_code == 200:
                result = response.json()
                if "prediction" in result:
                    st.success("判定完了")
                    data = result["prediction"]

                    top_one = data[0]
                    st.metric(label=f"判定結果1位{top_one['label']}", value=top_one["score"])
                    st.write("詳細")
                    st.table(data)

                else:
                    st.warning("予期せぬデータが返ってきました")
                    st.json(result)
            else:
                st.error(f"サーバーエラー: {response.status_code}")
                st.write(response.text)
            
        except Exception as e:
            st.error(f"接続エラー: {e}")
            st.info("Dockerを確認してください")