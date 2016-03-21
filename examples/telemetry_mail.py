__author__ = 'ceremcem'

from aktos_dcs import *
from aktos_dcs_lib import *

class TelemetryMail(AktosTelemetryMailBase):
    def prepare(self):
        self.password = "this-is-your-mail-password"

if __name__ == "__main__":
    class TestMailSystem(Actor):
        def action(self):
            import time
            mail = TelemetryMail()
            recipients = ["cem@aktos.io"]
            i = 0

            print "sending test message, #%d..." % i, time.time()
            mail.send_mail(recipients, "Test Message from cca-erik #%d" % i, "test content")

            sleep(5)
            print "receiving last message..."
            print mail.get_last_mail()
            sleep(10)
            i += 1

    TestMailSystem()
    wait_all()
