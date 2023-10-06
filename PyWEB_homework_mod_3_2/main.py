import time
from multiprocessing import cpu_count, Pool


# Декоратор для обчислення часу виконання функції
def timer(func):
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        start_time = time.time()
        output = func(*args, **kwargs)
        end_time = time.time()
        print(f"Total time for {func_name}: {end_time - start_time:.5f} s")
        return output

    return wrapper


# Синхронна версія функції factorize
@timer
def factorize_sync(numbers):
    return [[i for i in range(1, num + 1) if num % i == 0] for num in numbers]


# Паралельна версія функції factorize
def worker(num):
    return [i for i in range(1, num + 1) if num % i == 0]


@timer
def factorize_parallel(numbers):
    num_cores = cpu_count()  # Визначення кількості ядер
    print(f"Знайдено {num_cores} ядер")

    # Створення пулу процесів для паралельних обчислень
    with Pool(num_cores) as pool:
        results = pool.map(worker, numbers)

    return results


if __name__ == "__main__":
    numbers = [128, 255, 99999, 10651060]

    print("Синхронна версія:")
    print("Результати:", factorize_sync(numbers))
    print("*" * 60)
    print("Паралельна версія:")
    print("Результати:", factorize_parallel(numbers))
