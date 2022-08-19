import threading
import requests

def makeSendMailRequest(subject=None, message=None, recipient=None, csrftoken="", req_endpoint=""):
    ''' make request to 'api/send-mail' syncronously with multithreading
    csrftoken is required for django POST request
    '''
    
    def sendReq():  
        req = requests.post(
            req_endpoint,
            data={
                "subject": subject,
                "message": message,
                "recipient": recipient,
            },
            headers={
                'X-CSRFToken': csrftoken,
                'Origin': 'https://science2masu.herokuapp.com'
            },
            cookies={
                'csrftoken': csrftoken
            }
        )
        # internet says that i can pass csrf token in X-CSRFToken headers.
        # but it didn't work. until i pass csrftoken in cookies AND in headers, then it work

    if req_endpoint != "" and csrftoken != "":
        task = threading.Thread(target=sendReq)
        task.daemon = True
        task.start()

        print('success making send mail request')
    else:
        print('cannot make send mail request')
