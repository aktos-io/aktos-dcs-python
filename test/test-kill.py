from aktos_dcs import * 

class Test(Actor):
    def __init__(self, id): 
        Actor.__init__(self)
        self.id = id 

    def action(self): 
        while True: 
            print "Actor %d is running..." % self.id
            sleep(1)

    def handle_KillYourself(self, msg): 
        self.kill()

class Killer(Actor): 
    def action(self):
        sleep(2)
        print "sending kill message"
        self.send({'KillYourself': {}})


for i in range(10): 
    Test(i)

Killer()

wait_all()
