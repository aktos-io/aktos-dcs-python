# coding: utf-8

from aktos_dcs import *
from aktos_dcs_lib import *

# import preconfigured mail client
from telemetry_mail import TelemetryMail

class TestMailActor(EMailActor):
    def prepare(self):
        self.mail_client = TelemetryMail()

    def action(self):
        i = 0
        sending_period = 50
        print "Periodic sending mail will be started in %d seconds..." % sending_period
        while True:
            sleep(sending_period)
            print "Sending mail number: %d..." % i

            recipients = ["ceremcem@ceremcem.net", self.mail_client.username]
            subject = "test-subject-çalışöğün-number: %d" % i
            content = "çalışöğün22, seq: %d" % i
            attachments = []  #["./cca_signal.py"]
            self.send_mail(recipients, subject, content, attachments)
            i += 1

    def handle_EMail(self, mail):
        print "Got mail: "
        print "Index: ", mail["index"]
        print "From: ", mail["from"]
        print "To: ", mail["to"]
        print "Timestamp: ", mail["unix_timestamp"]
        print "Subject: ", mail["subject"]
        print "Body: ", mail["body"]

        print "This mail is received by inbox %d seconds ago." % (time.time() -
                                                                  mail["unix_timestamp"])


        ## Forward this mail anywhere 
        #print "Forwarding message to cem@aktos.io"
        #self.send_mail(["cem@aktos.io"], "Forwarded message from telemetry", pack(mail))

TestMailActor()
wait_all()
