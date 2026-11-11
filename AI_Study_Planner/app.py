import os
import json
import streamlit as st
from openai import OpenAI
from pydantic import BaseModel, Field

st.set_page_config(page_title='AI 智慧讀書計畫助手', page_icon='📚')
st.title('📚 AI 智慧讀書計畫助手')
st.write('輸入學習需求，讓 AI 幫你安排可執行的讀書計畫。')

class StudyTask(BaseModel):
    day: int = Field(description='第幾天，從 1 開始')
    topic: str = Field(description='當天學習主題')
    minutes: int = Field(description='當天預計學習分鐘數')
    action: str = Field(description='具體可執行的學習活動')

class StudyPlan(BaseModel):
    title: str
    goal: str
    tips: list[str]
    tasks: list[StudyTask]

subject = st.text_input('學習科目', placeholder='例如：英文')
goal = st.text_area('學習目標', placeholder='例如：熟悉 100 個常用單字')
days = st.slider('規劃天數', 1, 14, 7)
minutes = st.number_input('每天可用時間（分鐘）', min_value=10, max_value=300, value=60, step=10)

if st.button('✨ 產生讀書計畫', type='primary'):
    if not subject.strip() or not goal.strip():
        st.warning('請先填寫學習科目與學習目標。')
    elif len(subject) > 100 or len(goal) > 1000:
        st.warning('輸入內容過長，請縮短後再試。')
    else:
        api_key = st.secrets.get('OPENAI_API_KEY', os.getenv('OPENAI_API_KEY'))
        if not api_key:
            st.error('尚未設定 OPENAI_API_KEY，請先依 README 設定。')
        else:
            try:
                client = OpenAI(api_key=api_key)
                with st.spinner('AI 正在安排讀書計畫…'):
                    response = client.responses.parse(
                        model='gpt-4o-mini',
                        input=[
                            {'role': 'system', 'content': (
                                '你是專業且友善的繁體中文學習規劃助理。'
                                '根據科目、目標、天數及每日分鐘數，產生務實的每日學習計畫。'
                                '必須恰好列出指定天數的任務，day 從 1 連續編號，'
                                '每個任務 minutes 不得超過每日可用時間。'
                                '請勿要求使用者提供私人資料。')},
                            {'role': 'user', 'content': (
                                f'科目：{subject}\n目標：{goal}\n'
                                f'天數：{days}\n每天時間：{minutes} 分鐘')},
                        ],
                        text_format=StudyPlan,
                    )
                plan = response.output_parsed
                if plan is None:
                    st.error('AI 未回傳有效的結構化結果，請重試。')
                elif len(plan.tasks) != days or any(t.day != i or t.minutes < 1 or t.minutes > minutes for i, t in enumerate(plan.tasks, 1)):
                    st.error('AI 回傳的天數或時間不符合要求，請重新產生。')
                else:
                    st.success('讀書計畫產生成功！')
                    st.subheader(plan.title)
                    st.write('**學習目標：**', plan.goal)
                    for task in plan.tasks:
                        with st.expander(f'第 {task.day} 天｜{task.topic}（{task.minutes} 分鐘）', expanded=True):
                            st.write(task.action)
                    st.subheader('學習建議')
                    for tip in plan.tips:
                        st.write('•', tip)
                    st.download_button('下載 JSON 計畫', json.dumps(plan.model_dump(), ensure_ascii=False, indent=2), file_name='study_plan.json', mime='application/json')
            except Exception as e:
                st.error('API 呼叫失敗，請確認網路、API Key、模型權限與額度。')
                st.caption(f'錯誤類型：{type(e).__name__}')
