import pandas as pd

# 파일 경로 설정
file1_path = 'D:/dohyun/3grade/빅데이터/프로젝트/상권배후지별_매출_평균.csv'
file2_path = 'D:/dohyun/3grade/빅데이터/프로젝트/길단위영역직장.csv'

# CSV 파일 읽기 (인코딩: EUC-KR)
df1 = pd.read_csv(file1_path, encoding='euc-kr')
df2 = pd.read_csv(file2_path, encoding='euc-kr')

# 열 이름 통일
df2.rename(columns={'상권배후지코드명': '상권배후지_코드_명'}, inplace=True)

# 데이터 병합 (기존 데이터 유지)
merged_df = pd.merge(df2, df1, on='상권배후지_코드_명', how='left')

# 병합 결과 저장
output_file = 'D:/dohyun/3grade/빅데이터/프로젝트/통합본.csv'
merged_df.to_csv(output_file, index=False, encoding='euc-kr')

# 결과 확인
print(f"병합된 데이터가 '{output_file}'에 저장되었습니다.")
