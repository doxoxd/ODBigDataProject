import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

start_folder = 'D:\\dohyun\\3grade\\빅데이터\\프로젝트\\project_code\\move_data'
folder_list = os.listdir(start_folder)
all_data = []
for folder_name in folder_list:
    date_folder = os.path.join(start_folder, folder_name)
    if not os.path.isdir(date_folder):
        continue
    
    file_list = os.listdir(date_folder)
    
    for file_name in file_list:
        file_path = os.path.join(date_folder, file_name)
        data = pd.read_csv(file_path)
        #data = data.sample(frac=0.1, random_state=404)
        all_data.append(data)

combined_df = pd.concat(all_data, ignore_index=True)

combined_df['start_time'] = pd.to_datetime(combined_df['start_time'], format='%H:%M').dt.hour
combined_df['end_time'] = pd.to_datetime(combined_df['end_time'], format='%H:%M').dt.hour

#combined_df = combined_df[combined_df["dest_purpose"] == 3] #####여기서 군집화
combined_df = combined_df.drop(columns=['H'])
combined_df = combined_df.dropna()

# CSV 파일 읽기
csv1 = pd.read_csv('D:\\dohyun\\3grade\\빅데이터\\프로젝트\\project_code\\random_forest_label_8_대피.csv')
csv2 = combined_df

# 중복 열 제거 없이 통합 (공통 열: dest_hdong_cd, gender, age, purpose)
merged_csv = pd.merge(
    csv1,
    csv2,
    on=['dest_hdong_cd', 'gender', 'age', 'dest_purpose'],  # 기준 열
    how='outer'  # 중복 없이 합치기 위해 outer join 사용
)

def create_correlation_matrix(df, exclude_columns=None):
    """
    데이터프레임에서 상관행렬을 생성하며 특정 열을 제외할 수 있는 함수.

    Args:
        df (pd.DataFrame): 상관행렬을 생성할 데이터프레임
        exclude_columns (list, optional): 제외할 열의 리스트. 기본값은 None.

    Returns:
        pd.DataFrame: 생성된 상관행렬
    """
    if exclude_columns:
        # 제외할 열 삭제
        df = df.drop(columns=exclude_columns, errors='ignore')
    
    # 상관행렬 계산
    correlation_matrix = df.corr()
    return correlation_matrix



# 상관행렬 생성
correlation_matrix = create_correlation_matrix(merged_csv)

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.show()