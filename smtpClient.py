from socket import *

DIAG_EN = False

def smtp_client(port=1025, mailserver='127.0.0.1'):
    if DIAG_EN:
        print("DIAGNOSTIC STATEMENTS ENABLED! WATCH FOR PRECEDING '>'")

    msg = "\r\n This is a test message"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope
    ARGS_SERV = (mailserver, port)
    NYU_SERV = ('smtp.nyu.edu', 25) 


    # Create socket called clientSocket and establish a TCP connection with mailserver and port

    # Fill in start
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(NYU_SERV)
    # Fill in end

    recv = clientSocket.recv(1024).decode()
    diag_print(recv)
    #print(recv) #You can use these print statement to validate return codes from the server.
    #if recv[:3] != '220':
    #    print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Lorenzo\r\n'
    clientSocket.send(heloCommand.encode())
    diag_print(heloCommand)
    recv1 = clientSocket.recv(1024).decode()
    if not validate_status(recv1, '250'):
        print('ERROR - FAILURE TO SEND HELO:')
    diag_print(recv1,'') 
    #if recv1[:3] != '250':
    #    print('250 reply not received from server.')

    # Send MAIL FROM command and handle server response.
    # Fill in start
    mailFromCMD = 'MAIL FROM: <llg8192@nyu.edu>\r\n'
    clientSocket.send(mailFromCMD.encode())
    diag_print(mailFromCMD)
    recv_mailFrom = clientSocket.recv(1024).decode()
    if not validate_status(recv_mailFrom, '250'):
        print('ERROR - FAILURE TO SET SENDER:\n')
    diag_print(recv_mailFrom,'')
    # Fill in end

    # Send RCPT TO command and handle server response.
    # Fill in start
    rcptToCMD = 'RCPT TO: <llg8192@nyu.edu>\r\n'
    clientSocket.send(rcptToCMD.encode())
    diag_print(rcptToCMD)
    recv_rcptTo = clientSocket.recv(1024).decode()
    if not validate_status(recv_rcptTo, '250'):
        print('ERROR - FAILURE TO SET RECEPIENT:\n')
    diag_print(recv_mailFrom,'')
    # Fill in end

    # Send DATA command and handle server response.
    # Fill in start
    dataCMD = 'DATA\r\n'
    clientSocket.send(dataCMD.encode())
    diag_print(dataCMD)
    recv_data = clientSocket.recv(1024).decode()
    if not validate_status(recv_data, '354'):
        print('ERROR - FAILURE TO BEGIN DATA INPUT:\n')
    diag_print(recv_data,'')
    # Fill in end

    # Send message data.
    # Fill in start
    subjectline = 'Subject: SMTP Client output\r\n'
    clientSocket.send(subjectline.encode())
    clientSocket.send(msg.encode())
    clientSocket.send(endmsg.encode())
    diag_print(subjectline)
    diag_print(msg)
    diag_print(endmsg)
    recv_msg = clientSocket.recv(1024).decode()
    if not validate_status(recv_msg, '250'):
        print('ERROR - FAILURE TO TRANSMIT MESSAGE BODY AND/OR END:\n')
    diag_print(recv_msg,'')
    # Fill in end

    # Message ends with a single period, send message end and handle server response.
    # Fill in start
    # Fill in end

    # Send QUIT command and handle server response.
    # Fill in start
    quitCMD = 'QUIT\r\n'
    clientSocket.send(quitCMD.encode())
    recv_quit = clientSocket.recv(1024).decode()
    if not validate_status(recv_quit, '221'):
        print('ERROR - CONNECTION TERMINATION FAILURE:\n')
    diag_print(recv_quit,'')
    # Fill in end

def validate_status(stmt, expected_stat):
    return stmt[:3] == expected_stat

def diag_print(stmt,initial='>'):
    if DIAG_EN:
        print(f"${initial}${stmt}",end='')

if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')