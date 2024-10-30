import pandas as pd

# CSV 파일을 불러옵니다.
file_path = '22년병합.csv'  # 실제 파일 경로를 입력하세요.
df = pd.read_csv(file_path, encoding='cp949')

# "평균"이라는 이름을 가진 선수의 데이터를 찾습니다.
average_player = df[df['이름'].str.contains('평균', na=False)]

# 예외 처리: "평균" 선수가 존재하는지 확인
if not average_player.empty:
    
    # 점수 계산 함수 정의
    def calculate_score(value, min_value, max_value, average_value, score_range):
        if value <= average_value:
            return score_range * (value - min_value) / (average_value - min_value)  # 평균 이하일 경우
        else:
            return score_range + score_range * (value - average_value) / (max_value - average_value)  # 평균 이상일 경우

    # 득점권 타율 점수 계산
    max_득점권타율 = df['득점권타율'].max()
    min_득점권타율 = df['득점권타율'].min()
    average_득점권타율 = average_player['득점권타율'].values[0]
    df['득점권타율점수'] = df['득점권타율'].apply(calculate_score, args=(min_득점권타율, max_득점권타율, average_득점권타율, 2.5))

    # 득점권 출루율 점수 계산 
    max_득점권출루율 = df['득점권출루율'].max()
    min_득점권출루율 = df['득점권출루율'].min()
    average_득점권출루율 = average_player['득점권출루율'].values[0]
    df['득점권출루율점수'] = df['득점권출루율'].apply(calculate_score, args=(min_득점권출루율, max_득점권출루율, average_득점권출루율, 5))

    # 득점권 장타율 점수 계산 
    max_득점권장타율 = df['득점권장타율'].max()
    min_득점권장타율 = df['득점권장타율'].min()
    average_득점권장타율 = average_player['득점권장타율'].values[0]
    df['득점권장타율점수'] = df['득점권장타율'].apply(calculate_score, args=(min_득점권장타율, max_득점권장타율, average_득점권장타율, 5))

    # 득점권 OPS 점수 계산 
    max_득점권OPS = df['득점권OPS'].max()
    min_득점권OPS = df['득점권OPS'].min()
    average_득점권OPS = average_player['득점권OPS'].values[0]
    df['득점권OPS점수'] = df['득점권OPS'].apply(calculate_score, args=(min_득점권OPS, max_득점권OPS, average_득점권OPS, 5))

    # 월간 MVP 점수 계산 
    df['월간MVP점수'] = df['월간MVP'].apply(lambda x: 5 if x == 'O' else 0)

    # 올스타 점수 계산 
    df['올스타점수'] = df['올스타'].apply(lambda x: 5 if x == 'O' else 0)

    # 각 선수별 점수의 총합을 계산
    df['총합점수'] = df[['득점권타율점수', '득점권출루율점수', '득점권장타율점수', '득점권OPS점수', '월간MVP점수', '올스타점수']].sum(axis=1)

    # 결과를 CSV 파일로 저장
    output_file_path = '22년스타성점수.csv'  # 저장할 파일 경로
    df.to_csv(output_file_path, encoding='cp949', index=False)

    print(f"결과가 {output_file_path}로 저장되었습니다.")

else:
    print("평균이라는 이름을 가진 선수가 없습니다.")
