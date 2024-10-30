import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'

# 연도 입력받기
year_input = input("사용할 연도를 입력하세요 (22, 23, 24): ")

# CSV 파일 이름 설정
file_name = f"{year_input}년병합.csv"

# CSV 파일 읽기 (인코딩을 'euc-kr'로 지정)
for encoding in ['utf-8', 'utf-8-sig', 'cp949', 'latin1']:
    try:
        df = pd.read_csv(file_name, encoding=encoding)
        break  # 성공하면 루프 종료
    except UnicodeDecodeError:
        continue  # 인코딩 오류가 발생하면 다음 인코딩 시도

# 데이터가 로드되었는지 확인
if 'df' not in locals():
    raise ValueError("모든 인코딩에서 파일을 읽을 수 없습니다.")

# 결측치 처리 (결측치가 있는 행 제거)
df = df.dropna(subset=['타율', '출루율', '장타율', '경기', 'OPS'])

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

    # 레이더 차트에 사용할 데이터
    labels = ['타율', '출루율', '장타율', '경기', 'OPS']
    data = top_players[['타율', '출루율', '장타율', '경기', 'OPS']].values

    # 포지션에 해당하는 선수들의 평균 계산
    position_average = filtered_players[['타율', '출루율', '장타율', '경기', 'OPS']].mean().values

    # Min-Max 정규화
    # 추가할 선수 수
    extra_player_count = 1
    total_players_for_normalization = num_players + extra_player_count

    # 선수 수 조정
    if total_players_for_normalization > len(filtered_players):
        print("선수 데이터가 부족합니다. 가능한 만큼만 정규화합니다.")
        total_players_for_normalization = len(filtered_players)

    # 상위 total_players_for_normalization명 선택
    players_for_normalization = filtered_players.head(total_players_for_normalization)

    # 정규화할 데이터
    normalization_data = players_for_normalization[['타율', '출루율', '장타율', '경기', 'OPS']].values

    # Min-Max 정규화
    data_min = np.min(normalization_data, axis=0)
    data_max = np.max(normalization_data, axis=0)

    # 정규화 수행
    data_normalized = (normalization_data - data_min) / (data_max - data_min)
    data_normalized = data_normalized * 0.5 + 0.5

    # 포지션 평균 데이터 정규화
    position_average_normalized = (position_average - data_min) / (data_max - data_min)
    position_average_normalized = position_average_normalized * 0.5 + 0.5

    # 각 선수별 데이터 그리기
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # 색상 리스트
    colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FFD700']

    # 필요한 색상 수 조정
    used_colors = colors[:num_players] if num_players <= len(colors) else colors * (num_players // len(colors)) + colors[:num_players % len(colors)]

    # 서브플롯 생성
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # 선수별 레이더 차트 그리기
    for i in range(num_players):  # 입력받은 선수 숫자만큼만 표시
        values = data_normalized[i].tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=2, linestyle='solid', color=used_colors[i], label=top_players.iloc[i]['이름'])
        ax.fill(angles, values, alpha=0.25, color=used_colors[i])  # 색상 채우기

    # 포지션 평균 레이더 차트 그리기
    values_avg = position_average_normalized.tolist()
    values_avg += values_avg[:1]
    ax.plot(angles, values_avg, linewidth=2, linestyle='solid', color='black', label='포지션 평균')
    ax.fill(angles, values_avg, alpha=0.25, color='gray') 

    # 각 축 설정
    ax.set_yticklabels([])  # y축 레이블 숨기기
    ax.yaxis.grid(False)  # y축 그리드 숨기기
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    # 범례 위치 조정 (제목 오른쪽으로)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # 연도 표시 (차트 밖에 왼쪽)
    plt.figtext(0.1, 0.92, f'연도: {year_input}년', ha='left', va='top', fontsize=10)

    # 제목 추가
    plt.suptitle(f'{description} 성적 레이더 차트', size=15, x=0.5, y=0.95)
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()
