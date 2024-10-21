import pandas as pd

# 선수 명단
players = ['페디', '고영표', '양의지', '박동원', '오스틴', '양석환', '김헤성', '박민우', '노시환', '최정', 
           '오지환', '박찬호', '홍창기', '구자욱', '박건우', '정수빈', '소크라테스', '손아섭', '최형우']

# CSV 파일 읽기
df = pd.read_csv('23년 야구관련기사(11.14~12.10).csv')

# 선수별로 언급된 횟수를 저장할 딕셔너리
player_counts = {player: 0 for player in players}

# 기사 제목에서 선수 이름이 포함된 경우 카운트
for title in df['Title']:
    for player in players:
        if player in title:
            player_counts[player] += 1

# 결과를 DataFrame으로 변환
player_count_df = pd.DataFrame(list(player_counts.items()), columns=['Player', 'Count'])

# CSV 파일로 저장
player_count_df.to_csv('23_player_mentions_count.csv', index=False)

print("선수별 언급 횟수가 '23_player_mentions_count.csv' 파일로 저장되었습니다.")
