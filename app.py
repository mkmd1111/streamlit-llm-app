import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# アプリのタイトル設定
st.title("Expert AI Navigator\U0001F30D")

# アプリの説明
st.markdown("""
### アプリケーションの概要
このAIアシスタントは、あなたの疑問に専門家の視点で答えてくれるアプリです。\n
**「旅行」** と **「ビザ」** の2つの分野から選んで質問を入力するだけで、AIがプロの知識をもとに分かりやすく回答します！

### 使い方
1. 下のラジオボタンから専門分野を選択する（旅行\u2708\ufe0fまたはビザ\U0001F6C2）
2. 質問を入力する
3. 「送信」ボタンをクリックすると、AIがプロの視点で回答\u2728
""")

# 区切り線
st.divider()

# 専門家の種類を選択するラジオボタン
expert_type = st.radio(
    "専門家の種類を選択してください",
    ["旅行の専門家", "ビザ・移住の専門家"],
    index=0
)

# テキスト入力フォーム
user_input = st.text_area("質問を入力してください", height=150)

# LLMからの回答を取得する関数
def get_llm_response(input_text, expert_type):
    # システムメッセージの設定（専門家の種類に応じて変更）
    if expert_type == "旅行の専門家":
        system_content = """あなたは世界各地の旅行に精通した旅行の専門家です。
        目的地のおすすめスポット、グルメ、文化、治安、持ち物リスト、現地の習慣、言語のヒントなどを提供できます。
        旅行者のニーズ（バックパッカー向け・ラグジュアリー旅行・ノマドワーク向けなど）に合わせて、最適なアドバイスを心がけてください。
        ただし、最新の入国制限やビザ情報については変動があるため、公式情報を確認するよう推奨してください。
        回答は日本語で提供してください"""
    else:  # ビザの専門家
        system_content = """あなたは世界各地の旅行に精通した旅行の専門家です。
        目的地のおすすめスポット、グルメ、文化、治安、持ち物リスト、現地の習慣、言語のヒントなどを提供できます。
        旅行者のニーズ（バックパッカー向け・ラグジュアリー旅行・ノマドワーク向けなど）に合わせて、最適なアドバイスを心がけてください。
        ただし、最新の入国制限やビザ情報については変動があるため、公式情報を確認するよう推奨してください。
        回答は日本語で提供してください"""
    
    # LLMの初期化
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    # メッセージの作成
    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=input_text)
    ]
    
    # LLMからの回答を取得
    try:
        result = llm(messages)
        return result.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# 送信ボタン
if st.button("送信"):
    if user_input:
        # 処理中の表示
        with st.spinner('AIが回答を生成中です...'):
            # LLMからの回答を取得
            response = get_llm_response(user_input, expert_type)
            
            # 回答を表示
            st.subheader("AIからの回答:")
            st.markdown(response)
    else:
        st.error("質問を入力してください。")

# フッター
st.divider()
st.caption("© 2025 専門家AI アシスタント | Powered by LangChain & Streamlit")