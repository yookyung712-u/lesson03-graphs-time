import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------
# 기본 설정
# -----------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

st.title("영화 데이터 그래프 도감 1 - 시간")
st.write("1년치 일별 박스오피스 데이터를 이용해 영화의 시간에 따른 관객 변화를 살펴봅니다.")

# -----------------------------------------
# 데이터 불러오기
# -----------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜: YYYYMMDD → 실제 날짜형
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce",
    )

    # 숫자형 열 변환
    numeric_columns = ["순위", "영화코드", "일관객", "누적관객", "스크린수", "상영횟수"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 날짜순 정렬
    df = df.sort_values(["날짜", "순위"]).reset_index(drop=True)

    return df


try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.code(str(e))
    st.stop()

# -----------------------------------------
# 1. 날짜에 따른 일관객 변화
# -----------------------------------------
st.header("1. 날짜에 따른 영화별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique().tolist())

if movie_list:
    selected_movie = st.selectbox(
        "영화를 선택하세요.",
        movie_list,
    )

    movie_df = (
        df[df["영화명"] == selected_movie]
        .sort_values("날짜")
        .copy()
    )

    fig = px.line(
        movie_df,
        x="날짜",
        y="일관객",
        markers=True,
        title=f"「{selected_movie}」 날짜별 일관객 변화",
        labels={
            "날짜": "날짜",
            "일관객": "일관객 수",
        },
        hover_data={
            "날짜": "|%Y-%m-%d",
            "일관객": ":,",
        },
    )

    fig.update_traces(
        hovertemplate="날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>"
    )
    fig.update_layout(
        hovermode="x unified",
        xaxis_title="날짜",
        yaxis_title="일관객 수(명)",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**이 그래프로 알 수 있는 것:**")
    st.text_input(
        "한 문장으로 적어 보세요.",
        placeholder="예: 이 영화는 개봉 후 시간이 지나면서 일관객 수가 어떻게 변했는지 알 수 있다.",
        key="graph1_note",
        label_visibility="collapsed",
    )

# -----------------------------------------
# 2. 기간 전체 일관객 합계가 가장 큰 5편
# -----------------------------------------
st.divider()
st.header("2. 기간 전체 일관객 합계가 가장 큰 5편")

# 영화별로 이 기간의 일관객을 합산한 뒤 상위 5편을 선택합니다.
top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)["영화명"]
    .tolist()
)

top5_df = (
    df[df["영화명"].isin(top5_movies)]
    .groupby(["날짜", "영화명"], as_index=False)["일관객"]
    .sum()
    .sort_values(["날짜", "영화명"])
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=False,
    title="기간 전체 일관객 합계 상위 5편의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화",
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "영화명": True,
        "일관객": ":,",
    },
)

fig2.update_traces(
    hovertemplate="영화: %{fullData.name}<br>날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>"
)

fig2.update_layout(
    hovermode="closest",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화",
)

# Plotly 기본 범례는 항목을 클릭하면 해당 영화의 선을 켜고 끌 수 있습니다.
fig2.update_layout(
    legend=dict(
        itemclick="toggle",
        itemdoubleclick="toggleothers",
    )
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.text_input(
    "한 문장으로 적어 보세요.",
    placeholder="예: 기간 전체 관객이 많았던 영화들의 날짜별 관객 변화 양상을 비교할 수 있다.",
    key="graph2_note",
    label_visibility="collapsed",
)

# -----------------------------------------
# 앞으로 그래프를 추가할 공간
# -----------------------------------------
st.divider()
st.header("3. 다음 그래프")
st.info("앞으로 새로운 그래프를 이 구역에 계속 추가할 수 있습니다.")

st.divider()
st.header("4. 다음 그래프")
st.info("앞으로 새로운 그래프를 이 구역에 계속 추가할 수 있습니다.")
