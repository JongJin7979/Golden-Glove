import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 경우
fontprop = fm.FontProperties(fname=font_path, size=14)
plt.rc('font', family=fontprop.get_name())

# 포지션 코드와 설명을 매핑하는 딕셔너리
position_dict = {
    "1B": "1루수",
    "2B": "2루수",
    "3B": "3루수",
    "SS": "유격수",
    "F": "외야수",
    "H": "지명타자",
    "C": "포수"
}

# 포지션 검색 함수
def get_position_description(position_code):
    return position_dict.get(position_code.upper(), "존재하지 않는 포지션 코드입니다.")

# 연도 입력받기
year = input("연도를 입력하세요 (예: 22, 23, 24): ")

# CSV 파일 이름 생성
consistency_file = f"{year}년꾸준함점수.csv"
star_file = f"{year}년스타성점수.csv"

# 포지션 입력받기
user_input = input("검색할 포지션 코드를 입력하세요 (예: 1B, 2B, 3B, SS, F, H, C): ").strip()
description = get_position_description(user_input)
print(f"{user_input}: {description}")

# 화제성 점수 파일 이름 생성
buzz_scores_folder = '화제성점수'
buzz_file = f"{year}_{user_input}.csv"
buzz_file_path = os.path.join(buzz_scores_folder, buzz_file)

# CSV 파일 읽기 (인코딩을 여러 개 시도)
def read_csv_with_multiple_encodings(file_name):
    for encoding in ['utf-8', 'utf-8-sig', 'cp949', 'latin1']:
        try:
            df = pd.read_csv(file_name, encoding=encoding)
            return df  # 성공적으로 읽은 데이터프레임 반환
        except (UnicodeDecodeError, FileNotFoundError):
            continue  # 인코딩 오류 또는 파일 없음, 다음 인코딩 시도
    return None  # 모든 시도 실패

# 데이터 읽기
consistency_data = read_csv_with_multiple_encodings(consistency_file)
star_data = read_csv_with_multiple_encodings(star_file)
buzz_data = read_csv_with_multiple_encodings(buzz_file_path)

# 포지션 필터링
if consistency_data is not None:
    if user_input.upper() == 'F':
        consistency_data_filtered = consistency_data[consistency_data['포지션'].str.contains('F')]
    elif user_input.upper() == 'H':
        consistency_data_filtered = consistency_data[consistency_data['포지션'].str.contains('DH')]
    else:
        consistency_data_filtered = consistency_data[consistency_data['포지션'].str.contains(r'\b' + user_input.upper() + r'\b')]
else:
    consistency_data_filtered = None

if star_data is not None:
    if user_input.upper() == 'F':
        star_data_filtered = star_data[star_data['포지션'].str.contains('F')]
    elif user_input.upper() == 'H':
        star_data_filtered = star_data[star_data['포지션'].str.contains('DH')]
    else:
        star_data_filtered = star_data[star_data['포지션'].str.contains(r'\b' + user_input.upper() + r'\b')]
else:
    star_data_filtered = None

# 화제성 점수 데이터에서 필요한 열만 선택
if buzz_data is not None:
    buzz_data_filtered = buzz_data[['Player', 'Score']]
else:
    buzz_data_filtered = None

# 결과 출력 및 최종 점수 계산
if consistency_data_filtered is not None and star_data_filtered is not None:
    # 필요한 열 선택
    consistency_scores = consistency_data_filtered[['이름', '꾸준함점수']]
    star_scores = star_data_filtered[['이름', '총합점수']]
    
    # 두 데이터프레임 합치기 (화제성 점수에 있는 선수만)
    final_scores = pd.merge(consistency_scores, star_scores, on='이름', how='inner')

    # 화제성 점수와 최종 점수 합치기
    final_scores = pd.merge(final_scores, buzz_data_filtered, left_on='이름', right_on='Player', how='inner')

    # 최종 데이터프레임 정리
    final_scores = final_scores[['이름', '꾸준함점수', '총합점수', 'Score']]
    final_scores.rename(columns={'총합점수': '스타성점수', 'Score': '화제성 점수'}, inplace=True) 
    print("최종 점수 데이터 (필터링됨):")
    print(final_scores)

    # 레이더 차트 그리기
    categories = ['꾸준함점수', '스타성점수', '화제성 점수']
    
    # 각 선수의 점수를 가져와서 차트에 추가
    values_list = []
    names = []
    
    for index, row in final_scores.iterrows():
        values = row[categories].values.flatten().tolist()
        values.append(values[0])  # 첫 값을 다시 추가하여 닫힌 형태로 만들기
        values_list.append(values)
        names.append(row['이름'])

    # 각 선수의 각 점수를 차트에 그리기
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # 첫 각도를 다시 추가하여 닫힌 형태로 만들기

    # 최대 최소 범위 지정
    min_values = [0, 0, 0]  # 최소값
    max_values = [45, 45, 10]  # 최대값 (필요에 따라 조정)

    # 레이더 차트 그리기
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # 각 점수를 정규화하여 0~1로 변환
    normalized_values_list = []
    for values in values_list:
        normalized_values = [(val - min_val) / (max_val - min_val) for val, min_val, max_val in zip(values, min_values, max_values)]
        normalized_values.append(normalized_values[0])  # 첫 값을 다시 추가하여 닫힌 형태로 만들기
        normalized_values_list.append(normalized_values)

    for normalized_values, name in zip(normalized_values_list, names):
        ax.fill(angles, normalized_values, alpha=0.25)
        ax.plot(angles, normalized_values, linewidth=2, label=name)

    ax.set_yticklabels([])  # y축 라벨 제거
    ax.set_xticks(angles[:-1])  # x축 눈금 설정
    ax.set_xticklabels(categories)  # x축 라벨 설정
    
    # 라벨 위치 조정
    for tick in ax.get_xticklabels():
        tick.set_verticalalignment('center')  # 수직 정렬
        tick.set_y(tick.get_position()[1] - 0.1)  # y 좌표 조정 (아래로 이동)

    plt.title(f"{year}년 {description} 선수들의 레이더 차트", fontsize=16)
    plt.legend(loc='center left', bbox_to_anchor=(1, 1))  # 범례 위치 조정 (오른쪽 중앙)
    plt.show()
else:
    print(f"파일을 읽을 수 없거나 포지션이 없습니다.")
