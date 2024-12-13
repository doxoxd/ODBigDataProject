
# 🌟 OD 데이터를 통한 창업 지역 및 분야 추천
🚀 **창업핑 빅데이터 분석 프로젝트**



![Animation](https://drive.google.com/uc?id=1Kz8HM2qSak8u1XIuyqL_uRBhRshZTSrz)


🌐 사이트 바로가기

## 📖 프로젝트 소개
- 생활이동 데이터를 활용한 빅데이터 분석 프로젝트

- OD 데이터를 통한 창업 지역 종합적 추천 및 창업 타겟 추천

- 사업아이템 소유자의 창업지역 추천

- 창업지역 정보 제공 자동화 파이프라인 구축

## 🔗 Links
[![notion](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://katherineoelsner.com/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/)


                     
## 🚀 팀원 소개

| 이름        | 역할         | 
|-------------|--------------|
| **김도현**  | 데이터 분석 및 시각화, 전처리 및 군집화 지도 생성 |
| **도지현**  | 데이터 분석 및 시각화, R언어 활용 지도 시각화     | 
| **신정희**  | 데이터 분산 처리, 웹 페이지 구현     | 
| **조정민**  | 데이터 전처리 및 모델 학습, 변수 추출 및 산출식 도출  | 



## ⭐ 데이터 수집 및 전처리

### 데이터 수집

| 데이터명           | 규모             | 주소                     |
| ----------------- |----------------- | -------------------------|
| SKT OD 생활이동 공개데이터 | 1억 5천만 |https://www.bigcontest.or.kr/                             |
| 서울시 상권분석서비스(영역-상권배후지) | 1,072 |https://data.seoul.go.kr/dataList/OA-22159/S/1/datasetView.do|
| 서울시 상권분석서비스(길단위인구-상권배후지) | 23,979 |https://data.seoul.go.kr/dataList/OA-15582/S/1/datasetView.do|
| 서울시 상권분석서비스(추정매출-상권배후지) | 220,846 |https://data.seoul.go.kr/dataList/OA-15582/S/1/datasetView.do|
| 서울시 상권분석서비스(직장인구-상권배후지) | ? |https://data.seoul.go.kr/dataList/OA-15570/S/1/datasetView.do|



### 전처리
#### 🧑‍💻OD 데이터

| 속성             | 결측치 수     |
|------------------|--------------|
| origin_hdong_cd  | 0            |
| dest_hdong_cd    | 0            |
| date             | 0            |
| start_time       | 0            |
| end_time         | 0            |
| gender           | 0            |
| age              | 0            |
| modal            | 1,713        |
| origin_purpose   | 87,842       |
| dest_purpose     | 0            |
| od_dist_avg      | 0            |
| od_duration_avg  | 0            |
| od_cnts          | 0            |

- 데이터의 결측치를 찾아본 결과 modal 속성에 1,713개, origin_purpose에 87,842개의 결측치를 발견
- 출발지 체류 목적코드(origin_purpose)는 도착지의 체류 목적코드(dest_purpose)가 귀가가 아니면 귀가 설정정
- 귀가라면 같은 출발지 행정동 코드에서 머문 목적의 빈도수가 가장 많은 값을 넣을 수 있음
- 이동수단(modal)은 같은 곳을 이동하면 이동수단도 비슷할 것으로 보고 가장 비슷한 시간대에 사람들이 무엇으로 이동했는지 확인하고 채움

#### 📊 상권 분석 서비스 데이터
#### 데이터 설명
```bash
- 상권배후지_코드를 기준으로 4개의 데이터셋 병합
    - 영역-상권배후지
    - 길단위인구-상권배후지
    - 추정매출-상권배후지
    - 직장인구-상권배후지
```

#### 데이터 속성 추출
1️⃣ 영역-상권배후지
| 컬럼명                | 설명                                |
|----------------------|-----------------------------------|
| 상권배후지_구분_코드    | 상권배후지의 고유 구분 코드              |
| 상권배후지_구분_코드_명 | 상권배후지 구분 코드의 이름             |
| 엑스좌표_값             | 상권배후지의 중심 X좌표 값             |
| 와이좌표_값             | 상권배후지의 중심 Y좌표 값             |
| 행정동_코드            | 상권배후지의 행정동 코드                |
| 행정동_코드_명         | 상권배후지의 행정동 이름                |


2️⃣ 길단위인구-상권배후지
| 컬럼명                 | 설명                                |
|-----------------------|-----------------------------------|
| 상권배후지_코드         | 상권배후지의 고유 코드                  |
| 상권배후지_코드_명      | 상권배후지 코드 이름                  |
| 총_유동인구_수          | 전체 유동인구 수                    |
| 연령대_10_유동인구_수    | 10대 유동인구 수                    |
| 연령대_20_유동인구_수    | 20대 유동인구 수                    |
| 연령대_30_유동인구_수    | 30대 유동인구 수                    |
| 연령대_40_유동인구_수    | 40대 유동인구 수                    |
| 연령대_50_유동인구_수    | 50대 유동인구 수                    |
| 연령대_60_이상_유동인구_수 | 60대 이상 유동인구 수                |
| 시간대_00_06_유동인구_수 | 00~06시 유동인구 수                  |
| 시간대_06_11_유동인구_수 | 06~11시 유동인구 수                  |
| 시간대_11_14_유동인구_수 | 11~14시 유동인구 수                  |
| 시간대_14_17_유동인구_수 | 14~17시 유동인구 수                  |
| 시간대_17_21_유동인구_수 | 17~21시 유동인구 수                  |
| 시간대_21_24_유동인구_수 | 21~24시 유동인구 수                  |

3️⃣ 추정매출-상권배후지
| 컬럼명                  | 설명                                |
|------------------------|-----------------------------------|
| 상권배후지_코드          | 상권배후지의 고유 코드                  |
| 상권배후지_코드_명       | 상권배후지 코드 이름                  |
| 당월_매출_금액          | 당월 총 매출 금액                    |
| 시간대_00~06_매출_금액   | 00~06시 매출 금액                   |
| 시간대_06~11_매출_금액   | 06~11시 매출 금액                   |
| 시간대_11~14_매출_금액   | 11~14시 매출 금액                   |
| 시간대_14~17_매출_금액   | 14~17시 매출 금액                   |
| 시간대_17~21_매출_금액   | 17~21시 매출 금액                   |
| 시간대_21~24_매출_금액   | 21~24시 매출 금액                   |

4️⃣ 직장인구-상권배후지
| 컬럼명                     | 설명                                |
|---------------------------|-----------------------------------|
| 총_직장_인구_수             | 전체 직장인구 수                     |
| 남성_직장_인구_수           | 남성 직장인구 수                     |
| 여성_직장_인구_수           | 여성 직장인구 수                     |
| 연령대_10_직장_인구_수       | 10대 직장인구 수                    |
| 연령대_20_직장_인구_수       | 20대 직장인구 수                    |
| 연령대_30_직장_인구_수       | 30대 직장인구 수                    |
| 연령대_40_직장_인구_수       | 40대 직장인구 수                    |
| 연령대_50_직장_인구_수       | 50대 직장인구 수                    |
| 연령대_60_이상_직장_인구_수   | 60대 이상 직장인구 수                |
| 남성연령대_10_직장_인구_수    | 10대 남성 직장인구 수                 |
| 남성연령대_20_직장_인구_수    | 20대 남성 직장인구 수                 |
| 남성연령대_30_직장_인구_수    | 30대 남성 직장인구 수                 |
| 남성연령대_40_직장_인구_수    | 40대 남성 직장인구 수                 |
| 남성연령대_50_직장_인구_수    | 50대 남성 직장인구 수                 |
| 남성연령대_60_이상_직장_인구_수| 60대 이상 남성 직장인구 수             |
| 여성연령대_10_직장_인구_수    | 10대 여성 직장인구 수                 |
| 여성연령대_20_직장_인구_수    | 20대 여성 직장인구 수                 |
| 여성연령대_30_직장_인구_수    | 30대 여성 직장인구 수                 |
| 여성연령대_40_직장_인구_수    | 40대 여성 직장인구 수                 |
| 여성연령대_50_직장_인구_수    | 50대 여성 직장인구 수                 |
| 여성연령대_60_이상_직장_인구_수| 60대 이상 여성 직장인구 수             |


## 데이터 분산 처리

#### 하둡 데이터 업로드

```bash
hdfs dfs -mkdir -p /input
hdfs dfs -put /data/* /input
```

#### 업로드 확인
```bash
hdfs dfs -ls /input
```

#### 웹에서 확인하기
```bash
http://localhost:9870/explorer.html#
```

#### Spark를 활용한 데이터 읽기
```bash
# SparkSession 생성
spark = SparkSession.builder \
    .appName("HDFS and Local Save Example") \
    .getOrCreate()

# HDFS에서 데이터 읽기
input_path = "hdfs://namenode:9000/input/*/*.csv"
df = spark.read.csv(input_path, header=True, inferSchema=True)
```

#### spark-submit (실행행)
```bash
spark-submit /home/hadoop/cal.py
```

#### output 결과 확인인
```bash
spark-submit /home/hadoop/cal.py
```



## 모델 학습

## 📊 Random Forest Regression 모델 활용


  - 다양한 변수와 복잡한 관계를 효과적으로 다룰 수 있음
  - 비선형적인 관계를 모델링하는 데 유리
  - 입력변수가 나이, 성별, 목적, 지역의 비선형적인 관계이므로 랜덤포레스트가 적합함


### 프로젝트 개요
랜덤 포레스트 회귀 모델을 사용하여 데이터를 학습하고, 예측값과 실제값 간의 관계를 분석합니다. 데이터 로드, 전처리, 학습, 평가, 시각화까지의 전체 과정을 다룹니다.

---

#### 📂 1. 필요한 라이브러리 임포트

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
```
- `numpy`: 수치 계산을 위한 라이브러리
- `pandas`: 데이터 프레임 처리
- `scikit-learn`: 모델 학습, 평가 및 데이터 분리
- `matplotlib`: 데이터 시각화

#### 📂 2. 데이터 로드 및 확인

```python
file_path = 'D:\\study\\class\\빅데\\random_forest_label_8_대피.csv'
rf_data = pd.read_csv(file_path)

print("Data Head:\n", rf_data.head())
print("Data Description:\n", rf_data.describe())
```
- 데이터를 지정된 경로에서 로드
- `head()`: 데이터의 상위 5개 행을 출력
- `scikit-learn`: 모델 학습, 평가 및 데이터 분리
- `describe()`: 데이터의 통계 요약 정보를 제공

#### 📂 3. 입력 변수와 출력 변수 분리
```python
X = rf_data[['gender', 'age', 'purpose', 'dest_hdong_cd']]
y = rf_data['score']

```
- `X`: 입력 변수
  - `gender`: 성별
  - `age`: 나이
  - `purpose`: 목적
  - `dest_hdong_cd`: 목적지 코드

- `y`: 출력 변수
  - `score`: 예측하려는 값
  
#### 📂 4. 데이터 분리
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```
- 데이터를 학습 데이터와 테스트 데이터로 나눔눔
- `test_size=0.2`: 테스트 데이터 비율은 20%로 설정
- `random_state=42`: 결과 재현성을 보장하기 위한 고정값

#### 📂 5. 랜덤 포레스트 모델 학습
```python
model = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42)
```
- `n_estimators`: 랜덤 포레스트 트리의 개수 (100개)
- `max_depth`:각 트리의 최대 깊이 (20단계)
- `random_state`: 결과 재현성을 보장

#### 📂 6. 모델 예측
```python
y_pred = model.predict(X_test)
```
- 학습된 모델을 사용해 테스트 데이터의 값을 예측

#### 📂 7. 성능 평가
```python
mse = mean_squared_error(y_test, y_pred)max_depth=20, random_state=42)
r2 = r2_score(y_test, y_pred)
```
- 평가 결과
- `MSE (Mean Squared Error)`: 예측값과 실제값 간의 오차를 평가
- `R² (R-squared Score)`: 모델의 성능을 측정 (1에 가까울수록 좋음)

#### 📂 8. Feature Importance 확인
```python
importances = model.feature_importances_
```
- 각 입력 변수`(X)`가 모델 예측에 미치는 영향을 출력

### 모델 가중치

| Model | Acc     | Weight               |
| :-------- | :------- | :------------------------- |
| **의사 결정 트리**| `string` | **Required**. Your API key |




## 시각화

## 📊 웹 페이지 구현
