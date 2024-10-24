import pandas as pd

# 선수 명단
players = ['안우진', '김광현', '양의지', '박동원', '박병호', '오재일', '김혜성', '김선빈', '최정', '문보경', 
           '오지환', '박성한', '이정후', '나성범', '피렐라', '최치훈', '소크라테스', '이대호', '페르난데스']

# CSV 파일 읽기
df = pd.read_csv('22년 야구관련기사(11.08~12.08).csv')

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
player_count_df.to_csv('player_mentions_count.csv', index=False)

print("선수별 언급 횟수가 'player_mentions_count.csv' 파일로 저장되었습니다.")
