from flask import Flask, render_template, request, session, send_file
# 필요한 라이브러리 임포트
import pandas as pd
from joblib import load
import os
import io
from graph import visualize_grouped_data_with_gender as gp

app = Flask(__name__)
model_path = './random_forest_model_30.joblib'
loaded_model = load(model_path)
purp_map = {0:'귀가', 1:'업무', 2:'학업', 3:'쇼핑여가',4:'기타',5:'여행'}
purp_map2 = {'귀가':0, '업무':1, '학업':2, '쇼핑여가':3,'기타':4,'여행':5}
gen_map = {0:'남', 1:'여'}
total_score_file = './random_forest_label_8_대피.csv'
total_socre = pd.read_csv(total_score_file)['score']
# 메인 화면
app.config["SECRET_KEY"] = "ABCD"
@app.route('/')
def main():
    return render_template('main.html')
@app.route('/p1')
def p1():
    return render_template('predict1.html')

@app.route('/p2')
def p2():
    return render_template('predict2.html')

def dest_all_char(dest_hdong_cd):
    result = []
    for age in range(9):
        for purpose in range(6):
            for gender in range(2):
                new_data = pd.DataFrame({'gender': [gender], 'age': [age], 'purpose': [purpose],'dest_hdong_cd':[dest_hdong_cd]})  # 예제 입력 데이터
                new_prediction = loaded_model.predict(new_data)
                result.append({'score' : new_prediction, 'gender': gender, 'age': age, 'purpose': purpose,'dest_hdong_cd':dest_hdong_cd})
    return result

def dest_all_region(gender, age, purpose):
    result = []
    hdong_file = './result_filtered.csv'
    hdong = pd.read_csv(hdong_file)
    for dong in hdong['행정동코드']:
        new_data = pd.DataFrame({'gender': [gender], 'age': [age], 'purpose': [purpose],'dest_hdong_cd':[dong]})  # 예제 입력 데이터
        new_prediction = loaded_model.predict(new_data)
        result.append({'score' : new_prediction, 'gender': gender, 'age': age, 'purpose': purpose,'dest_hdong_cd':dong})
    return result

@app.route('/mapclus')
def map_clustering():
    return render_template('map_before_cluster.html')

# 결과 화면
@app.route('/result1', methods=['POST'])
def result1():
    gender = request.form.get('gender')
    age = request.form.get('age')
    purpose = request.form.get('purpose')
    purposename = purpose
    dest_hdong_cd = request.form.get('dest_hdong_cd')
    name = dest_hdong_cd
    if '남' in gender:
        gender = 0
    else:
        gender = 1
    
    gendername = "남성" if gender == 0 else "여성"
    age = int(int(age)/10)
    resultage = age*10
    
    purpose = purp_map2[purpose]
    
    hdong_file = './region.csv'
    hdong = pd.read_csv(hdong_file)
    
    # 읍면동명 리스트 추출
    dest_hdong_cd = hdong[hdong['읍면동명']==dest_hdong_cd]['행정동코드'].iloc[0]
    new_data = pd.DataFrame({'gender': [gender], 'age': [age], 'purpose': [purpose],'dest_hdong_cd':[dest_hdong_cd]})  # 예제 입력 데이터
    new_prediction = loaded_model.predict(new_data)
    
    percentile = (total_socre > new_prediction[0]).mean() * 100
    percentile = round(percentile, 3)
    all_pram = dest_all_char(dest_hdong_cd)
    #print(all_pram)
    max_score = all_pram[0]
    for i in all_pram:
        if i['score'] > max_score['score']:
            max_score = i
      
    # 결과 메시지 생성
    #result = f"""
    #입력된 정보:
    #- 성별: {gendername}
    #- 연령대: {resultage}
    #- 목적: {purpose}
    #- 선택한 지역: {name}
    
    #결과:
    #입력된 정보에 대한 지역 점수는 {new_prediction[0]}입니다. 상위 {percentile}%에 해당합니다.
    #해당 지역에서는 {purpose}하는 {max_score['age'] * 10}대의 {gen_map[max_score['gender']]}성을 타겟으로 한 점수가 {max_score['score']}로 가장 높게 나타났습니다.
    #"""
    
    # 평균 점수와 비교
    average_score = total_socre.mean()
    #result += f"\n\n전체 평균 점수는 {average_score}입니다. 입력된 정보와 비교해 볼 때, 평균보다 {'높습니다.' if new_prediction[0] > average_score else '낮습니다.'}"
    
    # 목적별 최고 점수 지역
    top_purpose_area = max(all_pram, key=lambda x: x['score'] if x['purpose'] == purpose else -1)
    top_area_name = hdong[hdong['행정동코드'] == top_purpose_area['dest_hdong_cd']]['읍면동명'].iloc[0]
    #result += (
    #    f"\n\n목적 '{purpose}'와 관련하여 가장 높은 점수를 기록한 지역은 "
    #    f"'{top_area_name}'이며, 점수는 {top_purpose_area['score']}입니다."
    #)
    
    # 연령대별 점수 그래프 생성
    graph_dir = './web/static/graph'
    os.makedirs(graph_dir, exist_ok=True)
    try:
        graphs = gp(name.replace('제',''), graph_dir)
        print(graphs)
    except Exception as e:
        return f"<h1>그래프 생성 중 오류 발생: {e}</h1>"
    # 결과 데이터 전달
    print(resultage)
    print(purposename)
    print(name)
    result = {
        "gendername": gendername,
        "resultage": resultage,
        "purpose": purposename,
        "region": name,
        "new_prediction": new_prediction[0],
        "percentile": percentile,
        "max_target": {
            "purpose": purp_map[max_score['purpose']],
            "age": max_score['age'] * 10,
            "gender": gen_map[max_score['gender']],
            "score": max_score['score']
        },
        "average_score": average_score,
        "top_purpose": {
            "area_name": top_area_name,
            "score": top_purpose_area['score']
        }
    }
    
    return render_template('result1.html', result=result, graphs=graphs)
            
    #result = f"지역 점수는 {new_prediction}입니다! 이 점수는 상위 {percentile}%입니다.\n해당 지역에서는 {purp_map[max_score['purpose']]}하는 {max_score['age'] * 10}대의 {gen_map[max_score['gender']]}성을 타겟으로 한 지역 점수가 {max_score['score']}로 가장 높게 나타났습니다."
            


@app.route('/result2', methods=['POST'])
def result2():
    gender = request.form.get('gender')
    age = request.form.get('age')
    purpose = request.form.get('purpose')
    purposename = purpose
    if '남' in gender:
        gender = 0
        gender_name = "남성"
    else:
        gender = 1
        gender_name = "여성"
    
    age = int(int(age)/10)
    resultage = age*10
    purpose = purp_map2[purpose]
    new_prediction = dest_all_region(gender, age, purpose)
    max_score = 0
    max_region = ''
    download_csv_list = []
    hdong_file = './result_filtered.csv'
    hdong = pd.read_csv(hdong_file)
    for i in new_prediction:
        input = {}
        input['score'] = i['score'][0]
        input['gender'] = gen_map[i['gender']]
        input['age'] = i['age']*10
        input['purpose'] = purp_map[i['purpose']]
        result = []
        
        input['dest_hdong_cd'] = hdong[hdong['행정동코드'] == i['dest_hdong_cd']]['읍면동명'].iloc[0]
        if max_score<i['score']:
            max_score = i['score']
            max_region = i['dest_hdong_cd']
        download_csv_list.append(input)
    eup_myeon_dong_list = hdong[hdong['행정동코드'] == max_region]['읍면동명'].iloc[0].replace('제','')
    result_message = f"{hdong[hdong['행정동코드'] == max_region]['읍면동명'].iloc[0]}이 {max_score}로 가장 적합한 것으로 나타났습니다."
    predicted_results = pd.DataFrame(download_csv_list)
    csv_name = "D:/sjh/three/빅데이터/조정민조/web" + str(len(os.listdir("D:/sjh/three/빅데이터/조정민조/web"))) + '.csv'
    predicted_results.to_csv(csv_name, index=False, encoding='utf-8-sig')
    session['csv_name'] = csv_name
    
    print(eup_myeon_dong_list)
     # 그래프 저장 및 생성
    graph_dir = './web/static/graph'
    os.makedirs(graph_dir, exist_ok=True)
    try:
        graphs = gp(eup_myeon_dong_list, graph_dir)
        print(graphs)
    except Exception as e:
        return f"<h1>그래프 생성 중 오류 발생: {e}</h1>"
    print(result_message)
    result = {
        "gender": gender_name,
        "age": resultage,
        "purpose": purposename,
        "resultmessage": result_message
        }
    return render_template('result2.html', result=result, graphs=graphs)

@app.route('/download', methods=['GET'])
def download():
    return send_file(
        session['csv_name'],
        as_attachment=True,
        download_name='example.csv'
    )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2201, debug=True)
