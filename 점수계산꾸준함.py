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

    # 경기 점수 계산
    max_경기 = df['경기'].max()
    min_경기 = df['경기'].min()
    average_경기 = average_player['경기'].values[0]
    df['경기점수'] = df['경기'].apply(calculate_score, args=(min_경기, max_경기, average_경기, 5))

    # 타율 점수 계산
    max_타율 = df['타율'].max()
    min_타율 = df['타율'].min()
    average_타율 = average_player['타율'].values[0]
    df['타율점수'] = df['타율'].apply(calculate_score, args=(min_타율, max_타율, average_타율, 2.5))

    # 출루율 점수 계산
    max_출루율 = df['출루율'].max()
    min_출루율 = df['출루율'].min()
    average_출루율 = average_player['출루율'].values[0]
    df['출루율점수'] = df['출루율'].apply(calculate_score, args=(min_출루율, max_출루율, average_출루율, 5))

    # 장타율 점수 계산
    max_장타율 = df['장타율'].max()
    min_장타율 = df['장타율'].min()
    average_장타율 = average_player['장타율'].values[0]
    df['장타율점수'] = df['장타율'].apply(calculate_score, args=(min_장타율, max_장타율, average_장타율, 5))

    # OPS 점수 계산
    max_ops = df['OPS'].max()
    min_ops = df['OPS'].min()
    average_ops = average_player['OPS'].values[0]
    df['OPS점수'] = df['OPS'].apply(calculate_score, args=(min_ops, max_ops, average_ops, 5))

    # 각 선수별 점수의 총합을 계산
    df['꾸준함점수'] = df[['경기점수', '타율점수', '출루율점수', '장타율점수', 'OPS점수']].sum(axis=1)

    # 결과를 CSV 파일로 저장
    output_file_path = '22년꾸준함점수.csv'  # 저장할 파일 경로
    df.to_csv(output_file_path, encoding='cp949', index=False)

    print(f"결과가 {output_file_path}로 저장되었습니다.")

else:
    print("평균이라는 이름을 가진 선수가 없습니다.")
