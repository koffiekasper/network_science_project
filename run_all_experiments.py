import os
from src.EvaluationProcess import MetricEvaluation

directory = os.fsencode("./dot_files/")
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)
    if filename.endswith(".dot"):
        print("Processing"+filename)
        os.system(f"./src/run_scripts_without_noweight.sh {filename}")
        continue
    else:
        continue


directory = os.fsencode("./output/")
m = MetricEvaluation()
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        print("Processing"+filename)
        m.run(filename)
        continue
    else:
        continue
