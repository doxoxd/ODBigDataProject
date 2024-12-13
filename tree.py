# 필요한 라이브러리 임포트
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# 데이터 불러오기
file_path = 'D:\\study\\class\\빅데\\random_forest_label_8_대피.csv'
rf_data = pd.read_csv(file_path)

# 데이터 확인
print("Data Head:\n", rf_data.head())
print("Data Description:\n", rf_data.describe())

# 1. 입력 변수와 출력 변수 분리
# 입력 변수 X: 'gender', 'age', 'purpose'
# 출력 변수 y: 'score'
X = rf_data[['gender', 'age', 'purpose', 'dest_hdong_cd']]  # 입력 변수
y = rf_data['score']  # 출력 변수

# 2. 학습 데이터와 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. 랜덤 포레스트 회귀 모델 생성 및 학습
# n_estimators: 트리 개수, max_depth: 최대 깊이
model = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42)
model.fit(X_train, y_train)

# 4. 모델 예측
y_pred = model.predict(X_test)

# 5. 성능 평가
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 결과 출력
print("Mean Squared Error (MSE):", mse)
print("R^2 Score:", r2)

# 6. 중요도 확인
importances = model.feature_importances_
for i, col in enumerate(X.columns):
    print(f"Feature '{col}' Importance: {importances[i]:.4f}")

# 7. 예측값과 실제값 비교 시각화
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted')
plt.show()
