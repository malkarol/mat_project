from datetime import datetime
import pickle

user = "Michal"
localPath = "./script_generator/generated_scripts/dummy/"

def get_date_for_name():
    timeFormat = "%H%M%S%d%m%Y"
    today = datetime.now().strftime(timeFormat)
    return today

def get_text_from_file(fileName):
    with open(fileName) as f:
        lines = f.readlines()
    return lines

def create_filename(extension=".py"):
    fileName = get_date_for_name()
    fileName = localPath+fileName+"_"+user+".py"
    return fileName

def create_dummy_python_file(fileName, sometext=""):
    if sometext =="":
        with open(fileName, 'w') as f:
            f.write(print("Hello"))
    else:
        with open(fileName, 'w') as f:
            for element in sometext:
                f.write(element)

def script_to_textfile(inputFile,outputFile=""):
    if outputFile == "":
        outputFile = inputFile[:-2]+"txt"
    with open(inputFile, "r") as _inputFile, open(outputFile, "w") as _outputFile:
        _outputFile.write(_inputFile.read())

def create_common_part():
    pass

def script_to_pickle(inputFile,outputFile=""):
    if outputFile == "":
        outputFile = inputFile[:-2]+"pickles"
    with open(inputFile, "r") as _inputFile:
        readText = _inputFile.read()
    with open(outputFile, "wb") as _outputFile:
        pickle.dump(readText, _outputFile)


def get_parameters():
    """
    :type listOfObjects: list<Object>
    """
    pass

if __name__ == "__main__":
    fileName = create_filename()
    sometext = get_text_from_file("./script_generator/testSource.py")
    create_dummy_python_file(fileName, sometext)
    script_to_textfile(fileName)
    script_to_pickle(fileName)


