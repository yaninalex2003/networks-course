import sys
import ftplib
import pathlib

USER = 'dlpuser'
PASSWORD = 'rNrKYTX9g7z3RgJRmxWuGHbeu'

def run(ftp):
    while True:
        cmd = input().split()
        if cmd[0] == 'list':
            res = ftp.retrlines('LIST')
            print(res)

        elif cmd[0] == 'upload':
            if len(cmd) != 2:
                print("Incorrect arguments number")
                continue
            filename = cmd[1]
            with open(filename, 'rb') as f: 
                ftp.storbinary(f"STOR {filename}", f)
            print(f"{filename} successfully uploaded")

        elif cmd[0] == 'download':
            if len(cmd) != 2:
                print("Incorrect arguments number")
                continue
            filename = cmd[1]
            with open(filename, 'wb') as f: 
                ftp.retrbinary(f"RETR {filename}", f.write)
            print(f"{filename} successfully downloaded")

        else:
            print("Incorrect command")

if __name__ == '__main__':
    ftp = ftplib.FTP('ftp.dlptest.com')
    ftp.login(USER, PASSWORD)
    run(ftp)
    ftp.close()