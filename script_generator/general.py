from datetime import date

user = "Michal"
localPath = "./script_generator/generated_scripts/dummy/"

def get_date_for_name():
    timeFormat = "%d%m%Y"
    today = date.today().strftime(timeFormat)
    print("Today's date:", today)
    return today

def create_dummy_python_file(fileName,localPath):
    fileName = localPath+fileName+"_"+user+".py"
    with open(fileName, 'w') as f:
        f.write('print("Hello")')

def create_common_part():
    pass
def get_parameters():
    """
    :type listOfObjects: list<Object>
    """
    pass

if __name__ == "__main__":
    fileName = get_date_for_name()
    create_dummy_python_file(fileName,localPath)

