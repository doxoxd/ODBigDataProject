import pandas as pd
import chardet

# 파일 경로
file_path = 'D:/dohyun/3grade/빅데이터/프로젝트/통합_위경도.csv'

# 인코딩 감지
with open(file_path, 'rb') as f:
    result = chardet.detect(f.read(100000))
    encoding = result['encoding']
    print(f"감지된 인코딩: {encoding}")

# 파일 읽기
df_area = pd.read_csv(file_path, encoding=encoding)

# 상권배후지_코드_명별 고유 번호 생성 (클러스터 생성)
df_area['cluster'] = df_area['상권배후지_코드_명'].factorize()[0] + 1  # 1부터 시작

# 열 이름 변경
df_area = df_area.rename(columns={
    '엑스좌표_값': 'lon',  # '엑스좌표_값'을 'lon'으로 변경
    '와이좌표_값': 'lat'   # '와이좌표_값'을 'lat'으로 변경
})

# 결과 확인
print(df_area.head())

# 결과 저장
output_file = 'D:/dohyun/3grade/빅데이터/프로젝트/통합_위경도_클러스터.csv'
df_area.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"결과가 '{output_file}'에 저장되었습니다.")
