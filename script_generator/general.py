from datetime import datetime
import pickle

user = "Michal"
localPath = "./script_generator/generated_scripts/dummy/"
realPath = "./script_generator/generated_scripts/pseudoReal/"

def get_date_for_name():
    timeFormat = "%d%m%Y%H%M%S"
    today = datetime.now().strftime(timeFormat)
    return today

def get_text_from_file(fileName):
    with open(fileName) as f:
        lines = f.readlines()
    return lines

def create_filename(isPseudoReal=False,extension=".py"):
    fileName = get_date_for_name()
    filePath = realPath if isPseudoReal else localPath
    fileName = filePath+user+"_"+fileName+extension
    return fileName

def create_filename(name,isPseudoReal=False, extension=".py"):
    fileName = get_date_for_name()
    filePath = realPath if isPseudoReal else localPath
    fileName = filePath+user+"_"+name+"_"+fileName+extension
    return fileName

def create_dummy_python_file(fileName, sometext=""):
    if sometext =="":
        with open(fileName, 'w') as f:
            f.write(print("Hello"))
    else:
        with open(fileName, 'w') as f:
            for element in sometext:
                f.write(element)

def textfile_to_script(inputFile, outputFile=""):
    if outputFile == "":
        outputFile = inputFile[:-3]+"py"
    with open(inputFile, "r") as _inputFile, open(outputFile, "w") as _outputFile:
        _outputFile.write(_inputFile.read())

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

def replace_params_in_File(listOfParams, sourcefileName,destinationFile):
    textFromFile = get_text_from_file(sourcefileName)
    newTexts = []
    for key,value in listOfParams:
        for line in textFromFile:
            newText= line.replace("@{"+key+"}",value)
            newTexts.append(newText)
    with open(destinationFile, 'w') as f:
        for element in newTexts:
            f.write(element)

def replace_params_in_Existing_File(listOfParams, destinationFile):
    for key in listOfParams:
        textFromFile = get_text_from_file(destinationFile)
        newTexts = []
        for line in textFromFile:
            newText = line.replace("@{"+key+"}",listOfParams[key])
            newTexts.append(newText)
        with open(destinationFile, 'w') as f:
            for element in newTexts:
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

    textfile_to_script(fileName)
    return fileName

def create_learning_with_fake_clients_MNIST(utilsFile, trainsetPath, isPassedAsScript =False):
    fileName = create_filename("learning", True, ".txt")
    pathToFiles= "./script_generator/source_chunks/MNIST_chunks/core_chunks/declarations_and_functions/"
    nameOfUtils = utilsFile[:-3] if isPassedAsScript else utilsFile[:-4]
    nameOfUtils=nameOfUtils.split("/")[-1]
    nameOfTrainset = "'./"+trainsetPath+"'"
    dict ={
        "utilzFileName": nameOfUtils,
        "trainsetPath": nameOfTrainset}


    source_1 = pathToFiles+ "MNIST_importPackages.txt"
    pathToFiles = "./script_generator/source_chunks/MNIST_chunks/model_dependant_chunks/"
    module_source = pathToFiles + "MNIST_utilz_dependant_import.txt"
    write_chunk_to_file(fileName,source_1, module_source)
    pathToFiles = "./script_generator/source_chunks/MNIST_chunks/core_chunks/"
    source_2 = pathToFiles + "MNIST_trainAndTestSplit.txt"
    write_chunk_to_file(fileName,source_2)
    source_3 = pathToFiles+"MNIST_parametrized_clientsCreation.txt"
    source_4 = pathToFiles+ "MNIST_processing_and_batching.txt"
    write_chunk_to_file(fileName,source_3)
    write_chunk_to_file(fileName,source_4)
    pathToFiles = "./script_generator/source_chunks/MNIST_chunks/model_dependant_chunks/"
    source_5 = pathToFiles+ "MNIST_optimizer_loss_metrics.txt"
    source_6 = pathToFiles+"MNIST_federated_learning.txt"
    write_chunk_to_file(fileName,source_5)
    write_chunk_to_file(fileName,source_6)
    replace_params_in_Existing_File(dict,fileName)

    textfile_to_script(fileName)
    return fileName

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

    utilsFileName = create_utils_MNIST()
    create_learning_with_fake_clients_MNIST(utilsFileName,"/Users/michal/Documents/trainingSet")