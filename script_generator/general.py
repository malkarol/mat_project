from datetime import datetime
import pickle

user = "Michal"
localPath = "./script_generator/generated_scripts/dummy/"
realPath = "./script_generator/generated_scripts/pseudoReal/"

def get_date_for_name():
    timeFormat = "%H%M%S%d%m%Y"
    today = datetime.now().strftime(timeFormat)
    return today

def get_text_from_file(fileName):
    with open(fileName) as f:
        lines = f.readlines()
    return lines

def create_filename(isPseudoReal=False,extension=".py"):
    fileName = get_date_for_name()
    filePath = realPath if isPseudoReal else localPath
    fileName = filePath+fileName+"_"+user+extension
    return fileName

def create_filename(name,isPseudoReal=False, extension=".py"):
    fileName = get_date_for_name()
    filePath = realPath if isPseudoReal else localPath
    fileName = filePath+fileName+"_"+name+"_"+user+extension
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

def script_to_pickle(inputFile,outputFile=""):
    if outputFile == "":
        outputFile = inputFile[:-2]+"pickles"
    with open(inputFile, "r") as _inputFile:
        readText = _inputFile.read()
    with open(outputFile, "wb") as _outputFile:
        pickle.dump(readText, _outputFile)

def write_chunk_to_file(destinationFile, chunkFile, sourceFile=""):
    if sourceFile == "":
        sourceFile = destinationFile
    destinationText = get_text_from_file(sourceFile)+ get_text_from_file(chunkFile)
    with open(destinationFile, 'w') as f:
            for element in destinationText:
                f.write(element)


def create_utils_MNIST():
    fileName = create_filename("utils",True,".txt")
    pathToFiles= "./script_generator/source_chunks/MNIST_chunks/core_chunks/declarations_and_functions/"
    source_1 = pathToFiles+ "MNIST_importPackages.txt"
    source_2 = pathToFiles+ "MNIST_createClients.txt"
    source_3 = pathToFiles + "MNIST_loadImageData.txt"
    source_4 = pathToFiles + "MNIST_batchData.txt"

    write_chunk_to_file(fileName,source_2,source_1)
    write_chunk_to_file(fileName,source_3)
    write_chunk_to_file(fileName,source_4)

    pathToFiles ="./script_generator/source_chunks/MNIST_chunks/model_dependant_chunks/"
    source_5 = pathToFiles+"MNIST_test_model.txt"
    source_6 = pathToFiles+"MNIST_simpleMLP_model.txt"
    source_7 = pathToFiles +"MNIST_weighting_and_scaling.txt"

    write_chunk_to_file(fileName,source_5)
    write_chunk_to_file(fileName,source_6)
    write_chunk_to_file(fileName,source_7)
    pass

def create_learning_with_fake_clients_MNIST():
    pass

def create_aggregator_script_MNIST():
    pass

def parametrize_chunk():
    """
    TO DO
    :type params: list<string>
    """
    pass

def get_parameters(params):
    """
    TO DO
    :type params: list<string>
    """
    pass

if __name__ == "__main__":
    # fileName = create_filename()
    # sometext = get_text_from_file("./script_generator/testSource.py")
    # create_dummy_python_file(fileName, sometext)
    # script_to_textfile(fileName)
    # script_to_pickle(fileName)

   create_utils_MNIST()



