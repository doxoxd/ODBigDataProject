import pandas as pd
import matplotlib.pyplot as plt

def show_sang(d):
    # 데이터 로드
    file_path = 'D:\\study\\class\\빅데\\aggregated_data.csv'  # 파일 경로를 입력하세요
    data = pd.read_csv(file_path, encoding='UTF-8')
    
    want_data = data[data['행정동_코드'] == d]
    
        # 열 추출
    columns_of_interest = [
        "시간대_00~06_매출_금액",
        "시간대_06~11_매출_금액","시간대_11~14_매출_금액","시간대_14~17_매출_금액","시간대_17~21_매출_금액","시간대_21~24_매출_금액"
    ]

    # 열 이름을 x축, 값(평균)을 y축으로 설정
    daily_population = data[columns_of_interest].iloc[0]

    # 그래프 생성
    plt.figure(figsize=(10, 6))
    plt.bar(daily_population.index, daily_population.values, color='skyblue', edgecolor='black')
    plt.title("Average Floating Population by Day of the Week", fontsize=16)
    plt.xlabel("Day of the Week", fontsize=12)
    plt.ylabel("Average Population", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
show_sang(11110515)