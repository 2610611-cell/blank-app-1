import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="화장실 사용 현황 모니터링", layout="centered")
st.title("🚽 화장실 실시간 사용 현황")
st.markdown("---")

# 2. 세션 상태(Session State) 초기화 (6개 칸의 상태 저장: 0은 빈칸, 1은 사용중)
if "stalls" not in st.session_state:
    st.session_state.stalls = [0] * 6

# 3. 화장실 칸별 질문 및 상태 업데이트
st.subheader("❓ 화장실 칸별 현황 확인")

# 6개의 칸을 입력받기 편하게 3열씩 2줄로 배치
row1 = st.columns(3)
row2 = st.columns(3)
all_rows = row1 + row2

for i in range(6):
    with all_rows[i]:
        st.markdown(f"### 🧻 {i+1}번 칸")
        # 사용자가 라디오 버튼으로 "네" 또는 "아니요" 선택
        choice = st.radio(
            "사람이 있나요?",
            ["아니요", "네"],
            key=f"stall_question_{i}",
            horizontal=True
        )
        # 선택에 따라 0 또는 1로 변환하여 저장
        st.session_state.stalls[i] = 1 if choice == "네" else 0

st.markdown("---")

# 4. [요구사항] 전체 인원 수 계산 및 1/6 형태로 표시
occupied_count = sum(st.session_state.stalls)
total_stalls = 6

st.subheader("📊 실시간 혼잡도 결과")
st.metric(label="현재 이용 중인 칸", value=f"{occupied_count} / {total_stalls}")

# 5. 각 칸의 현재 상태를 시각적으로 한 눈에 보여주기
status_cols = st.columns(6)
for i in range(6):
    with status_cols[i]:
        if st.session_state.stalls[i] == 1:
            st.error(f"**{i+1}번**\n\n🔴 사용중\n(1명)")
        else:
            st.success(f"**{i+1}번**\n\n🟢 비어있음\n(0명)")

st.markdown("---")

# 6. [요구사항] 쉬는 시간 타이머 (1분 남았을 때 알림)
st.subheader("⏱️ 쉬는 시간 타이머")
duration_minutes = st.number_input("쉬는 시간 설정 (분)", min_value=1, max_value=60, value=10)

if st.button("타이머 시작"):
    total_seconds = duration_minutes * 60
    
    timer_placeholder = st.empty()
    alert_placeholder = st.empty()