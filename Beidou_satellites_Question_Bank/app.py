import streamlit as st
import pandas as pd
import random
import os
import streamlit as st
# st.write("當前目錄下所有檔案：", os.listdir('.'))

data = pd.read_excel('Beidou_satellites_Question_Bank/Beidou_satellites_Question_Bank.xlsx')

if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_ids' not in st.session_state:
    st.session_state.question_ids = []
if 'wrong_ids' not in st.session_state:
    st.session_state.wrong_ids = []
if 'current_question_idx' not in st.session_state:
    unused_ids = [i for i in range(len(data)) if i not in st.session_state.question_ids]
    st.session_state.current_question_idx = random.choice(unused_ids) if unused_ids else None
if 'answered' not in st.session_state:
    st.session_state.answered = False

total_questions = len(data)
answered_questions = len(st.session_state.question_ids)
percent_score = (st.session_state.score / answered_questions * 100) if answered_questions else 0

def pick_random_unanswered():
    unused_ids = [i for i in range(len(data)) if i not in st.session_state.question_ids]
    if unused_ids:
        st.session_state.current_question_idx = random.choice(unused_ids)
        st.session_state.answered = False
        st.rerun()

def pick_random_wrong():
    if st.session_state.wrong_ids:
        st.session_state.current_question_idx = random.choice(st.session_state.wrong_ids)
        st.session_state.answered = False
        st.rerun()

if st.session_state.current_question_idx is not None:
    question = data.loc[st.session_state.current_question_idx]
    options = [question[col] for col in ['A', 'B', 'C', 'D'] if col in question.index and pd.notna(question[col])]
    
    # 顯示題號和問題
    st.markdown(f"#### 題號 {question['Id']} / {total_questions}")
    st.markdown(f"**題目：** {question['Question']}")    
    ans = st.radio("請選擇一個答案", options, key=str(st.session_state.current_question_idx))
    st.progress(answered_questions / total_questions)

    if not st.session_state.answered and st.button("提交答案"):
        correct = question[question['Answer']] if question['Answer'] in question else None
        if ans == correct:
            st.success("答對了！")
            st.session_state.score += 1
        else:
            # 找到正確選項的index
            correct_idx = options.index(correct)
            correct_letter = chr(65 + correct_idx)
            st.error(f"答錯了！正確答案是 {correct_letter} 解析：{question['Explain']}")
            qid = st.session_state.current_question_idx
            if qid not in st.session_state.wrong_ids:
                st.session_state.wrong_ids.append(qid)
        st.session_state.answered = True
        st.session_state.question_ids.append(st.session_state.current_question_idx)

        percent_score = (st.session_state.score / (answered_questions + 1) * 100)

        st.write(f"目前分數：{st.session_state.score} / {answered_questions+1} ({percent_score:.1f}%)")

    if st.session_state.answered:
        col1, col2 = st.columns(2)
        # 隨機下一題按鈕
        with col1:
            if st.button("隨機下一題"):
                pick_random_unanswered()
        # 隨機錯誤題目按鈕，僅有錯題時顯示
        with col2:
            if st.session_state.wrong_ids:
                if st.button("隨機錯誤題目"):
                    pick_random_wrong()
    else:
        st.write(f"目前分數：{st.session_state.score} / {answered_questions} ({percent_score:.1f}%)")
else:
    final_percent = st.session_state.score / total_questions * 100
    st.info("全部題目已完成！")
    st.markdown(f"### 最終分數：{st.session_state.score} / {total_questions}  \n**正確率：{final_percent:.1f}%**")
    st.progress(1.0)
    # 若有錯誤題，給一個按鈕可隨機重做
    if st.session_state.wrong_ids:
        if st.button("隨機重做錯題"):
            pick_random_wrong()





