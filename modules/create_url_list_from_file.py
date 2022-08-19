def createUrlListFromFile(txt_file_path=""):
    ''' create list of url from txt file '''

    open_file = open(txt_file_path)
    line_list = open_file.read().splitlines()

    full_file_path_split = txt_file_path.split('/')

    # exclude item(.txt, .bat, others)
    for line in line_list:
        if ".txt" in line:
            line_list.remove(line)
        if ".bat" in line:
            line_list.remove(line)
        if line.split('/')[-1] == 'raw':
            line_list.remove(line)

    open_file.close()

    # raw_result
    img_url_list = line_list

    return img_url_list # (list)