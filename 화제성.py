import os
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'

# "Count" 폴더 경로
folder_path = 'Count'

# 사용자로부터 연도와 포지션 입력받기
year_input = input("원하는 연도를 입력하세요 (22, 23, 24): ")  # 예: '22'
position_input = input("원하는 포지션을 입력하세요 (1루수, 2루수, 3루수, 포수, 외야수, 유격수, 지명타자): ")

# 유효한 포지션 목록
valid_positions = ['1루수', '2루수', '3루수', '포수', '외야수', '유격수', '지명타자']

if position_input not in valid_positions:
    print("유효한 포지션을 입력하세요.")
else:
    # 검색할 파일 이름 형식
    search_term = f"{year_input}_player_mentions_count_{position_input}.csv"

    # CSV 파일 경로
    csv_file_path = os.path.join(folder_path, search_term)

    # CSV 파일 읽기
    try:
        df = pd.read_csv(csv_file_path)
        print(f"Loaded: {csv_file_path}")

        # 데이터 확인
        print(df.head())  # 데이터의 처음 몇 줄을 출력하여 확인

        # 원형 그래프를 그리기 위한 열 선택
        if 'Count' in df.columns:
            # Count에 대한 데이터와 선수 이름
            data = df['Count']
            labels = df['Player']  # 선수 이름 열

            # 원형 그래프 그리기
            plt.figure(figsize=(5, 5))  # 사이즈 조정
            
            # 비율과 실제 값 함께 표시
            def func(pct, allvals):
                absolute = int(round(pct / 100. * sum(allvals)))
                return f'{pct:.1f}%\n({absolute})'

            # 원형 그래프 그리기 (labels 매개변수를 빈 리스트로 설정)
            wedges, texts, autotexts = plt.pie(data, labels=None, autopct=lambda pct: func(pct, data), startangle=90)
            plt.setp(autotexts, size=10, weight="bold", color="white")  # 텍스트 스타일 설정
            
            plt.title(f'{position_input} 언급 수 비율', pad=20)  # 제목에 패딩 추가
            plt.axis('equal')  # 원형 그래프가 원형으로 보이게 설정

            # 범례 추가
            plt.legend(wedges, labels, title="선수", loc="upper left", bbox_to_anchor=(1, 1))

            # 연도 표시 (차트 밖에 왼쪽)
            plt.figtext(0.1, 0.92, f'연도: {year_input}년', ha='left', va='top', fontsize=10)

            # 여백 조정
            plt.subplots_adjust(right=0.75)  # 오른쪽 여백 조정

            plt.show()
        else:
            print("'Count' 열이 데이터프레임에 존재하지 않습니다.")

    except FileNotFoundError:
        print(f"{csv_file_path} 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"Error loading {csv_file_path}: {e}")
