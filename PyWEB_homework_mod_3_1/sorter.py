import argparse
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from shutil import copyfile
from threading import Thread
"""
--source [-s] default folder = junk
--output [-o] default folder = sorted
"""
logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", default="junk")
parser.add_argument("--output", "-o", help="Output folder", default="sorted")

args = vars(parser.parse_args())
print(args)

source = Path(args.get("source"))
output = Path(args.get("output"))
folders = []


# Створюємо функцію рекурсивного обхода папок за вказаним шляхом
def folder_search(path):
    for item in path.iterdir():
        if item.is_dir():
            print(f"Знайдена директорія: {item}")
            folders.append(item)
            folder_search(item)


# загоняємо кожний виклик функції folder_search() в пул потоків
# кількість потоків можна задавати змінною number_threads
def parallel_search(path, number_threads):
    with ThreadPoolExecutor(max_workers=number_threads) as executor:
        executor.submit(folder_search, path)


# копіюємо файли в знайдених папках в папки створені згідно розширенню файла
def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            ext_folder = output / ext
            try:
                ext_folder.mkdir(exist_ok=True, parents=True)
                copyfile(el, ext_folder / el.name)
            except OSError as err:
                logging.error(err)
                sys.exit(1)


if __name__ == "__main__":

    folders.append(source)

    num_threads = 10  # Кількість потоків, які ви хочете використовувати
    parallel_search(source, num_threads)
    print(f"Копіюємо файли з папки '{source}' в папку '{output}' ...\n{'-' * 60}")
    # розкидуємо по потокам копіювання файлів
    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    print(f"Все готово,"
          f" файли розсортовані по папкам за розширенням. \nРезультат можна подивитись тут:\n{output.absolute()}")
