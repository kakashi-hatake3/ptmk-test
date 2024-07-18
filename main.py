import sys


def algorithm1():
    print("Выполняется алгоритм 1")
    # Здесь можно добавить код для алгоритма 1


def algorithm2():
    print("Выполняется алгоритм 2")
    # Здесь можно добавить код для алгоритма 2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python main.py <номер алгоритма>")
        print("Номер алгоритма может быть 1 или 2")
        sys.exit(1)

    algorithm_number = sys.argv[1]

    if algorithm_number == "1":
        algorithm1()
    elif algorithm_number == "2":
        algorithm2()
    else:
        print("Неверный номер алгоритма. Допустимые значения: 1 или 2")
        sys.exit(1)
