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
        system_content = """あなたは世界中の観光地・文化・アクティビティに精通した旅行の専門家です。
        旅行者が目的地を最大限に楽しめるよう、観光名所、グルメ、アクティビティ、ショッピング、イベント情報などを提供してください。
        旅行スタイル（バックパッカー向け・ラグジュアリー旅行・ノマドワーク・家族旅行など）に合わせた最適なプランを提案してください。
        移動手段（公共交通機関・レンタカー・タクシーなど）の選び方や、おすすめの宿泊エリアについてもアドバイスを行ってください。
        旅行者が安心して過ごせるよう、治安状況・現地の習慣・チップ文化・最低限の言語フレーズなども教えてください。
        回答は日本語で提供してください。"""
    else:  # ビザの専門家
        system_content = """あなたは世界各国のビザ制度や入国要件に精通したビザの専門家です。
        各国の短期滞在ビザ・長期滞在ビザ・就労ビザ・学生ビザなどの取得条件、必要書類、申請手続き、費用、審査期間について詳細に説明できます。
        また、渡航者の国籍や滞在目的（観光・ビジネス・留学・ノマドワークなど）に応じた最適なビザの種類を提案してください。
        最新のビザ要件や入国制限は変更される可能性があるため、公式情報（大使館・政府機関のウェブサイト）を確認するよう推奨してください。
        回答は日本語で提供してください。"""
    
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