def writeLog(log_string="", max_log_line=5):
    # save log
    with open('request_logs.txt', 'r+') as file:
        # store lines
        lines = file.readlines()
        lines_total = len(lines)

        if lines_total >= max_log_line:
            # clear lines
            file.seek(0) # move cursor to beginning (required since using 'r+')
            file.truncate()

            # rewrite lines with given index
            file.writelines(lines[lines_total-max_log_line : lines_total])
        
        # add new line
        file.write(f'{log_string}\n')