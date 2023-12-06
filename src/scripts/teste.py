import os
dir_path = os.getcwd()  # Ou substitua por outro caminho
print(os.access(dir_path, os.W_OK))