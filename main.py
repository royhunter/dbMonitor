#!/usr/bin/python


from httpd import httpd

PORT_NUMBER = 8000

def main():
    dbmHttpd = httpd.dbmHttpServer(PORT_NUMBER)
    dbmHttpd.Run()


if __name__ == '__main__':
    main()