from multiprocessing.pool import ThreadPool as Pool
import helpers
import time
import paramiko
import datetime as t
import sys
import logging
import glob

class ssh:
    def __init__(self,lMap,path="scripts\\script.txt"):
        self.lMap = lMap
        self.finished = []
        self.path = path

    def finish(self, name):
        #report back that thread has ended
        self.finished.append(name)
        print("{0} | {1} done.".format(t.datetime.now().strftime("%H:%M:%S"), name))
        if len(self.finished) == len(self.lMap):
            print(t.datetime.now().strftime("%H:%M:%S"), " | Finished!")

    def startQueue(self):
        #configures connection and starts sending off connections
        pool = Pool(len(self.lMap))
        for ip in self.lMap:
            dict= {
            "host": ip,
            "username": self.lMap.get(ip)[0],
            "password":  self.lMap.get(ip)[1],
            "secret": self.lMap.get(ip)[1]
            }
            self.ip = ip
            print(t.datetime.now().strftime("%H:%M:%S"), " | Sending to ",ip)
            pool.apply_async(self.packageSend, (dict,), callback=self.finish)

    def packageSend(self, dict):
        #pulls in scripts and executed them
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            LOG_FILENAME = 'logs\\{0}.log'.format(len(glob.glob("logs\\*.log")))
            logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

            time.sleep(2)
            logging.info("logged in as {0} on {1} at {2}".format(dict["username"],
                                                                 dict["host"],
                                                                 t.datetime.now().strftime("%H:%M:%S")
                                                                 ))

            ssh_client.connect(hostname=dict["host"],username=dict["username"],password=dict["password"])
            remote_connection = ssh_client.invoke_shell()
            loglist= []
            remote_connection.send("enable".replace("\r","")+"\n")
            remote_connection.send(dict["password"].replace("\r","")+"\n")
            for c in helpers.getCArr(self.path):
                remote_connection.send(c.replace("\r","")+"\n")
                time.sleep(1)
                output = remote_connection.recv(65535).decode('ascii')
                print(self.ip, ": ", output)
                loglist.append(output)
            log = "\n".join(loglist)
            logging.info(log)
            ssh_client.close()

        except:
            print("ERROR: ", sys.exc_info()[0])

        finally:
            return dict["host"]
