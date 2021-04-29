"""COMP0015 grep - a simple search engine
"""
import os, string


def common_elements(lis1, lis2):

    """Find the common elements in two lists.
    Args:
        lis1 (list): one of the lists to compare
        lis2 (list): the other list to compare
    Returns:
        list : contains the elements common to both lists.
    """    

    tempLis = []
    for word in lis1:
        if word in lis2:
            if word not in tempLis:
                tempLis.append(word)
    return tempLis

def remove_punc(string):

    """Remove punctuation from split words of a list
    Args:
        string (string): a word from a list
    Returns:
        string: word without punctuation 
    """ 

    punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
    for ele in string:  
        if ele in punc:  
            string = string.replace(ele, "") 
    return string
 


def build_index(file_list, index, title_index):

    """Build a word index and a title index for all the files in a file list.
    Args:
        file_list (list): List containing file names
        index (dictionary): Index mapping words to filenames
        title_index (dictionary): Index mapping filenames to the title of the article.
    """

    for file_name in file_list:
        title, content = get_content(file_name)
        words = [] #list for storring words of content

        wordsList = title.strip(string.punctuation) + content.strip(string.punctuation)
        wordsList = title.split() + content.split()
        wordsList = [remove_punc(i) for i in wordsList] #removing all left punctutation (which will be end of sentences)

        #making all words from lower letter before checking for repetitions
        for x in range(len(wordsList)):
            wordsList[x] = wordsList[x].lower()


        #adding words to list that are not there yet
        for x in wordsList:
                x.strip(string.punctuation)
                words.append(x)


        for word in words:
            if word not in index and word != ' ':
                index[word] = [file_name]
            elif word in index and file_name not in index[word] and word != ' ':
                index[word].append(file_name)
    
        if file_name not in title_index:
            title_index[file_name] = title
        
    return index

def get_content(file_name):

    """Return the title and contents of the file.
    Args:
        file_name (str): String containing file name
    Returns:
        title (str): String containing the file title
        content (str): String containing the remaining words in the file
    """    

    with open(file_name) as file:
        title = file.readline().strip() # get the title
        contents = file.read()        # read the rest
        file.close()
        return title, contents

def search(index, query):

    """Search the index for the words in the query string.
    Args:
        index (dictionary): dictionary containing word to filename mapping.
        query (string): string containing words in the query. String is lowercase.
    Returns:
        list: list of file in which all the words in the query appear.
    """   
    searched_words_list = []
    sliced_query = query.split() #slicing query into seperate words if user inputs multiple words
    sliced_query = [remove_punc(i) for i in sliced_query] #removing punctuation
    k = 0 # number for storing successful matches of query, 
    # if user inputs 2 words function will check wether both words are found and not only one
    n = 0 

    #this part check wether all words can be found in file
    for word in sliced_query:
        word_lowercase = word.lower()
        if word_lowercase in index:
            n += 1

    print(len(sliced_query))
    if n == len(sliced_query):       
        for word in sliced_query:
            word_lowercase = word.lower()
            if word_lowercase in index:
                if k == 0:
                    searched_words_list = index[word_lowercase]
                elif k > 0:
                    searched_words_list = common_elements(searched_words_list, index[word_lowercase])
                k += 1

    return searched_words_list

def pretty_print(index, title_index):

    """Print the dictionaries passed as parameters
    Args:
        index (dictionary): Index mapping words to filenames
        title_index (dictionary): Index mapping filenames to the title of the article.
    """    

    print("\nIndex:")
    print(index)
    print("\nFile names and titles:")
    print(title_index)

def get_filenames(directory_name):

    """Return list of the files in the given directory.
    Args:
        directory_name (directory): Name of the directory
    Returns:
        list: list of filenames in the directory
    """    

    file_list = []
    for filename in os.listdir(directory_name):
        if filename.endswith('.txt'):
            file_list.append(os.path.join(directory_name, filename))
    return file_list

def menu(index, titles):

    """Menu for the application
    Args:
        index (dictionary): Index mapping words to filenames
        title_index (dictionary): Index mapping filenames to the title of the article.
    """    

    search_query = input('Enter a search query, (empty to finish): ')  
      
    while search_query != '':
        filename_list = search(index, search_query)
        print("Results: ", search_query)
        if len(filename_list) == 0:
            print("No results")
        else:
            for file in filename_list:
                title = titles[file]
                print("File: ", file, "Title: ", title)
        search_query = input('Enter a search query, (empty to finish): ')

def main():

    # Test 1: test common_elements

    # print(common_elements(['a', 'b', 'c'], ['a', 'p', 'c']))
    # print(common_elements(['a', 'b', 'c'],['x', 'y', 'z']))
    # print(common_elements(['a', 'b', 'a'],['a', 'a', 'a']))  

    # Test 2: test with small files
    #index = {}
    #titles = {}
    #build_index(['sentimental_1.txt', 'sentimental_2.txt', 'sentimental_3.txt'], index, titles)
    #pretty_print(index, titles)

    # Test 3: test with bbc sport news files
    #index = {}
    #titles = {}    
    #build_index(get_filenames('bbc_football'), index, titles)
    #pretty_print(index, titles)

    #Test 4: test with small files
    #index = {}
    #titles = {}
    #build_index(['sentimental_1.txt', 'sentimental_2.txt', 'sentimental_3.txt'], index, titles)
    #print(index)
    #print("\nsentimental: ", search(index, 'sentimental'))
    #print("\ncoltrane: ", search(index, 'coltrane'))
    #print('\nellington: ', search(index, 'ellington'))
    #print('\nsentimental journey: ', search(index, 'sentimental journey'))
    #print('\nnot_in_files', search(index, 'not_in_files'))
    #print('\nlong journey', search(index, 'long journey'))

    # Test 5:test all
    index = {}
    titles = {} 
    build_index(get_filenames('bbc_football'), index, titles)
    menu(index, titles)

    pass

if __name__ == '__main__':
    main()