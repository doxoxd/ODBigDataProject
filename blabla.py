import pandas as pd
import pyproj
import chardet

# 파일 경로
file_path = 'D:/dohyun/3grade/빅데이터/프로젝트/aggregated_data.csv'

# 파일의 앞부분만 읽어서 인코딩 감지
with open(file_path, 'rb') as f:
    sample = f.read(100000)  # 처음 100,000 바이트만 읽기
    result = chardet.detect(sample)
    encoding = result['encoding']
    print(f"감지된 인코딩: {encoding}")

# 파일 불러오기
print("\n2. 파일 읽는 중...")
data = pd.read_csv(file_path, encoding=encoding)  # 감지된 인코딩 사용
print("   파일 읽기 완료.")
print(data.head())  # 데이터 첫 5개 확인

# 좌표 변환 설정
print("\n3. 좌표 변환 설정 중...")
proj_ktm = pyproj.Proj(init='epsg:2097')  # Korean Transverse Mercator (EPSG:2097)
proj_wgs = pyproj.Proj(init='epsg:4326')  # WGS 84 (EPSG:4326)
print("   좌표 변환 설정 완료.")

# 기존 lat, lon 값을 재정의 (엑스좌표_값과 와이좌표_값 사용하여 변환)
print("\n4. 좌표 변환 실행 중...")
data['lon'], data['lat'] = pyproj.transform(proj_ktm, proj_wgs, data['엑스좌표_값'].values, data['와이좌표_값'].values)
print("   좌표 변환 완료.")

# 기존 '엑스좌표_값'과 '와이좌표_값' 칼럼 삭제 (필요 시 삭제)
data.drop(['엑스좌표_값', '와이좌표_값'], axis=1, inplace=True)

# 결과 확인
print(data[['lat', 'lon']].head())  # 변환된 데이터 첫 5개 확인

# 변환된 데이터 저장
print("\n5. 변환된 데이터 저장 중...")
output_path = 'D:/dohyun/3grade/빅데이터/프로젝트/통합_위경도.csv'
data.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"   변환된 데이터가 '{output_path}'에 저장되었습니다.")
