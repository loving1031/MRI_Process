import random
import os

def generate_lut_file():
    # 文件名列表，从filename.txt文件中读取
    file_names = []
    with open('filename.txt', 'r') as name_file:
        file_names = [line.strip() for line in name_file.readlines()]

    if len(file_names) < 36840:
        raise ValueError("filename.txt中文件名数量少于40000个，无法满足生成要求，请补充足够的文件名。")

    with open('generated_lut.txt', 'w') as file:
        for i in range(1,36841):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            file.write(f"{i}\t{file_names[i - 1]}\t{r}\t{g}\t{b}\t0\n")

if __name__ == "__main__":
    generate_lut_file()
    