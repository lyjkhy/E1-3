import json
import time

print("Mini NPU Simulator")
print("==================")
print("1. 직접 입력 모드")
print("2. data.json 테스트 모드")

def mac(input_data, filter_data):
    total = 0

    for i in range(len(input_data)):
        for j in range(len(input_data)):
            total += input_data[i][j] * filter_data[i][j]

    return total

with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("JSON 파일 읽기 성공!")

print(data.keys())
print(data["filters"]["size_5"].keys())
print(data["patterns"].keys())

filter_cross = data["filters"]["size_5"]["cross"]
filter_x = data["filters"]["size_5"]["x"]

print("Cross 필터 불러오기 성공")
print("X 필터 불러오기 성공")

print("Cross 필터:", filter_cross)
print("X 필터:", filter_x)

pattern = data["patterns"]["size_5_1"]

print("첫 번째 패턴 불러오기 성공")
print(pattern)


input_data = pattern["input"]

print("입력 데이터:", input_data)

total_time = 0

for i in range(10):
    start_time = time.perf_counter()
    score_cross = mac(input_data, filter_cross)
    score_x = mac(input_data, filter_x)
    end_time = time.perf_counter()

    elapsed_time = (end_time - start_time) * 1000
    total_time += elapsed_time

average_time = total_time / 10
print("평균 실행 시간:", average_time, "ms")









print("Cross 점수:", score_cross)
print("X 점수:", score_x)

if abs(score_cross - score_x) < 0.000000001:
    print("판정: UNDECIDED")
elif score_cross > score_x:
    print("판정: Cross")
else:
    print("판정: X")

expected = pattern["expected"]

print("기대 정답:", expected)

if expected == "x" and score_x > score_cross:
    print("테스트 결과: PASS")
elif expected == "cross" and score_cross > score_x:
    print("테스트 결과: PASS")
else:
    print("테스트 결과: FAIL")

total_count = 0
pass_count = 0
fail_count = 0
fail_cases = []



for pattern_name in data["patterns"]:
    pattern = data["patterns"][pattern_name]

    size = pattern_name.split("_")[1]
    filter_size = "size_" + size
    filters = data["filters"][filter_size]

    filter_cross = filters["cross"]
    filter_x = filters["x"]

    input_data = pattern["input"]
    total_time = 0

for i in range(10):
    start_time = time.perf_counter()
    score_cross = mac(input_data, filter_cross)
    score_x = mac(input_data, filter_x)
    end_time = time.perf_counter()

    elapsed_time = (end_time - start_time) * 1000
    total_time += elapsed_time

average_time = total_time / 10
print("평균 실행 시간:", average_time, "ms")

if abs(score_cross - score_x) < 0.000000001:
    result = "UNDECIDED"
elif score_cross > score_x:
    result = "Cross"
else:
    result = "X"

if pattern["expected"] == "+":
    expected_result = "Cross"
else:
    expected_result = "X"

if result == expected_result:
    test_result = "PASS"
else:
    test_result = "FAIL"

total_count += 1

if test_result == "PASS":
       pass_count += 1
else:
    fail_count += 1
    fail_cases.append(pattern_name)





    print("테스트 이름:", pattern_name)
    print("Cross 점수:", score_cross)
    print("X 점수:", score_x)
    print("판정:", result)
    print("기대 정답:", expected_result)
    print("테스트 결과:", test_result)
    print("--------------------")

    print("====================")
print("전체 테스트:", total_count)
print("성공:", pass_count)
print("실패:", fail_count)
print("====================")
print("실패한 테스트:", fail_cases)

