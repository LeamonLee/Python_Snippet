import os
from datetime import datetime

print(os.getcwd())

# os.chdir(r"C:\Leamon\PythonExercise\")
# print(os.getcwd())


print(os.listdir())


file_path = os.path.join(os.getcwd(), "Text.txt")
print(file_path)
print(os.path.basename(file_path))
print(os.path.dirname(file_path))
print(os.path.split(file_path))
print(os.path.splitext(file_path))

print(os.path.exists("/fakePath/Test.txt"))
print(os.path.exists("C:\\Leamon\\PythonExercise\\"))

print(os.path.isdir("C:\\Leamon\\PythonExercise\\"))
print(os.path.isfile("C:\\Leamon\\PythonExercise\\"))

# os.mkdir("os-demo-2")
# os.makedirs("os-demo-3/subFolder")
# print(os.listdir())


# os.rmdir("os-demo-2")
# os.removedirs("os-demo-3/subFolder")
# print(os.listdir())


# os.mkdir("os-demo-4")
# print(os.listdir())
# os.rename("os-demo-4", "os-demo-5")
# print(os.listdir())


# print(os.stat("os_tut.py"))
# print(os.stat("os_tut.py").st_size)
# print(os.stat("os_tut.py").st_mtime)            # Last modification time

# lstmod_time = os.stat("os_tut.py").st_mtime     # parse to human-readablt time
# print(datetime.fromtimestamp(lstmod_time))


# for dirPath, dirNames, fileNames in os.walk("C:\\Users\\Leamon\\Desktop\\"):
#     print("Current Path: ", dirPath)
#     print("Directories: ", dirNames)
#     print("Files: ", fileNames)
#     print()


# print(os.environ.get("Path"))