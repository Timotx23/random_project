import csv
def convert_to_ints(number_lst: list[str])-> int:
    """This function will be used to convert to a list of strs to an int
    it uses maketrans to remove all the unwanted things from the string and 
    makes it real easy to convert to a string that then can be converted to an int
    """ 
    bads=",$" #which characters i want to remove     
    table=str.maketrans("","", bads) # allows me to remove any unwanted things from the string   first "" the thing that needs to be replaced second "" the thing the first should be replaced with. bads all things that should always be removed
    cleaned_lst=[x.translate(table) for x in number_lst]
    return sum([float(z) for z in cleaned_lst])

def csv_reader(csv_path: str)-> dict[str, int]:
    """This function will read the csv file and return something"""
    dicti: dict ={}
    with open( csv_path, newline='') as csvfile:
        reader= csv.DictReader(csvfile)
        for reads in reader:
            if reads["Sales Person"] not in dicti:
                dicti[reads["Sales Person"]]=[reads["Amount"]]
            else:
               dicti[reads["Sales Person"]].append(reads["Amount"])
        new_dict = {k: convert_to_ints(v) for k, v in dicti.items()} 
    return new_dict

def csv_writers(csv_input: str) -> bool:
    """This function will write to a csv file"""
    ...
csv_eval=csv_reader(r"/Users/timohildenbrand/dsa learning/Dl/random_project/Chocolate Sales (2).csv")
print(csv_eval)