a = input("Enter a number: ")
b = input("Enter a second number: ")
c = input("Enter a third number: ")

def count_numbers(target, array):
    count = 0
    for number in array:
        if number == target:
            count += 1
    return count

result = int(a)*int(b)*int(c)

for i in range(10):
    print(f"{i}는 {count_numbers(str(i), str(result))}번 등장합니다.")
