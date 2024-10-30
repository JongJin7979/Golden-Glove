import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'

# 연도 입력받기
year_input = input("사용할 연도를 입력하세요 (22, 23, 24): ")

# CSV 파일 이름 설정
file_name = f"{year_input}년병합.csv"

# CSV 파일 읽기 (인코딩 여러 개 시도)
for encoding in ['utf-8', 'utf-8-sig', 'cp949', 'latin1']:
    try:
        df = pd.read_csv(file_name, encoding=encoding)
        break  # 성공하면 루프 종료
    except UnicodeDecodeError:
        continue  # 인코딩 오류가 발생하면 다음 인코딩 시도

# 데이터가 로드되었는지 확인
if 'df' not in locals():
    raise ValueError("모든 인코딩에서 파일을 읽을 수 없습니다.")

# 포지션 설명 딕셔너리
position_dict = {
    'SS': '유격수',
    'C': '포수',
    '1B': '1루수',
    '2B': '2루수',
    '3B': '3루수',
    'H': '지명타자',
    'F': '외야수'
}

# 포지션 검색 함수
def get_position_description(position_code):
    return position_dict.get(position_code.upper(), "존재하지 않는 포지션 코드입니다.")

# 포지션 입력 받기
user_input = input("검색할 포지션 코드를 입력하세요 (예: SS, C 등): ").strip()
description = get_position_description(user_input)
print(f"{user_input}: {description}")

# 포지션에 해당하는 선수들 필터링
if user_input.upper() == 'F':
    filtered_players = df[df['포지션'].str.contains('F')]
elif user_input.upper() == 'H':
    filtered_players = df[df['포지션'].str.contains('DH')]
else:
    filtered_players = df[df['포지션'].str.contains(r'\b' + user_input.upper() + r'\b')]

if filtered_players.empty:
    print("선수 데이터가 없습니다.")
else:
    # 상위 몇 명의 선수 선택할 것인지 입력 받기
    while True:
        try:
            num_players = int(input("몇 명의 선수를 선택하시겠습니까? (숫자를 입력하세요): "))
            break
        except ValueError:
            print("유효한 숫자를 입력하세요.")

    # 데이터의 개수 확인 후 최댓값으로 조정
    num_players = min(num_players, len(filtered_players))

    # 상위 num_players명 선택 (순위 기준으로)
    top_players = filtered_players.head(num_players)

    # 포지션에 따라 사용할 통계 항목 설정
    stat_options = {
        'SS': ['타율', '출루율', '장타율', 'OPS'],
        'C': ['타율', '출루율', '장타율', 'OPS'],
        '1B': ['타율', '출루율', '장타율', 'OPS'],
        '2B': ['타율', '출루율', '장타율', 'OPS'],
        '3B': ['타율', '출루율', '장타율', 'OPS'],
        'H': ['타율', '출루율', '장타율', 'OPS'],
        'F': ['타율', '출루율', '장타율', 'OPS']
    }

    # 포지션에 따라 사용할 x축 항목 선택
    x_labels = stat_options.get(user_input.upper(), ['타율', '출루율', '장타율', 'OPS'])

    # 각 선수의 데이터를 꺾은선 그래프로 그리기 위한 서브플롯 생성 (가로로 배치)
    num_players = len(top_players)
    fig, axs = plt.subplots(1, num_players, figsize=(4 * num_players, 4), sharey=True)

    # 각 선수의 성적을 꺾은선 그래프로 그리기
    for i, player in enumerate(top_players['이름']):
        general_stats = top_players.loc[top_players['이름'] == player, x_labels].values.flatten()
        clutch_stats = top_players.loc[top_players['이름'] == player, ['득점권타율', '득점권출루율', '득점권장타율', '득점권OPS']].values.flatten()

        # 꺾은선 그래프 그리기
        axs[i].plot(x_labels, general_stats, marker='o', label='일반', alpha=0.7, linestyle='-')
        axs[i].plot(x_labels, clutch_stats, marker='o', label='득점권', alpha=0.7, linestyle='--')

        # y축 최대값을 1.0보다 크게 설정하고 여유 공간 0.1 추가
        axs[i].set_ylim(0, max(1.0, general_stats.max(), clutch_stats.max()) + 0.1)

        # 차트 설정
        axs[i].set_title(player)

    # 범례 추가 (하나의 범례로 통일)
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, ['일반', '득점권'], loc='upper right', bbox_to_anchor=(1, 1), frameon=True)

    # y축 레이블 제거
    for ax in axs:
        ax.set_ylabel('')

    # 연도 표시 (차트 밖에 왼쪽)
    plt.figtext(0.1, 0.92, f'연도: {year_input}년', ha='left', va='top', fontsize=10)

    # 제목 추가
    plt.suptitle('스타성 확인', fontsize=16)

    plt.tight_layout(rect=[0, 0, 1, 0.9])  
    plt.show()
