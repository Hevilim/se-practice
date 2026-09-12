file = open("marks.txt", "r")
result = {}
for line in file:
    line = line.rstrip().split()
    name = line[0]
    scores = "".join(line[1:]).split(",")
    scores = [int(score) for score in scores 
              if score.isdigit() and 0 <= int(score) <= 100]

    result[name] = scores

print("Name | Valid | Average | Highest | Lowest | Pass rate")
print("-----+-------+---------+---------+--------+----------")
for name in result:
    valid = len(result[name])
    nan = "-"
    if valid == 0:
        print(f"{name:<5}| {valid:<6}| {nan:<8}| {nan:<8}| {nan:<7}| {nan}")
        continue

    average = sum(result[name]) / len(result[name])
    highest = max(result[name])
    lowest = min(result[name])
    passed = sum([1 for score in result[name] if score >= 50])
    pass_rate = passed / valid * 100
    print(f"{name:<5}| {valid:<6}| {average:<8.2f}| {highest:<8}| {lowest:<7}| {pass_rate}%")