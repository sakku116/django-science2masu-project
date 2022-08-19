def convertUrlsBase(
        url_list,
        use_imgix_url=False, 
        use_statically_url=False,
        without_base_url=False, 
        name_only=False,
        use_custom_url="",
        query_params="", 
    ):
    ''' convert url base of url list to another url base '''
    img_url_list = url_list

    first_prefix_path_name = "static"

    def useCustomBaseUrl(custom_base_url, img_url_list=img_url_list):
        result_list = []

        for img_url in img_url_list:
            # split url by '/' char
            img_url = img_url.split('/')
            # find 'static' index from list
            first_prefix_path_name_index = img_url.index(first_prefix_path_name)

            # remove default base url (if exist) by slicing the list from 'static' to end
            img_path = img_url[first_prefix_path_name_index:]

            # join list using '/' char
            img_path = '/'.join(img_path)

            # add '/' between base_url and img_path if does not exist
            if custom_base_url[-1] != '/' and img_path[0] != '/':
                result = f"{custom_base_url}/{img_path}"
            else:
                result = f"{custom_base_url}{img_path}"

            result_list.append(result)

        img_url_list = result_list

        return img_url_list

    if use_imgix_url == True:
        img_url_list = useCustomBaseUrl('https://science2masu-sf-gh.imgix.net/')

    if use_statically_url == True:
        github_user = "sakku116"
        github_repo = "science2masu-static-files"
        github_branch = "main"
        img_url_list = useCustomBaseUrl(f'https://cdn.statically.io/gh/{github_user}/{github_repo}/{github_branch}/')

    if use_custom_url:
        if 'https://' not in use_custom_url:
            # prevent img src use relative url
            use_custom_url = f'https://{use_custom_url}'
        img_url_list = useCustomBaseUrl(use_custom_url)

    if query_params:
        ''' add query parameters string  '''
        result_list = []

        for img_url in img_url_list:
            if '?' not in query_params: # add '?'
                result = f'{img_url}?{query_params}'
            else: # dont add '?'
                result = f'{img_url}{query_params}'

            result_list.append(result)

        img_url_list = result_list

    if without_base_url == True:
        ''' remove base_url if exist '''
        # img src will use relative url because the url will be started with '/'
        result_list = []

        for img_url in img_url_list:
            img_url = img_url.split('/')
            first_prefix_path_name_index = img_url.index(first_prefix_path_name)

            img_path = img_url[first_prefix_path_name_index:]
            img_path = '/'.join(img_path)

            result_list.append(img_path)
        
        img_url_list = result_list

    if name_only == True:
        result_list = []

        for img_url in img_url_list:
            img_url = img_url.split('/')
            file_name = img_url[-1]

            result_list.append(file_name)
        
        img_url_list = result_list

    return img_url_list # (list)