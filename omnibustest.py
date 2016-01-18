from omnibus.api import publish
from datetime import datetime
import random
import string
import time


def send_hello_world():
    while True:
        time.sleep(0.5)
        message = "".join([random.choice(string.ascii_letters)
                           for i in range(10)])
        timestamp = str(datetime.now())
        print("Sending: %s, %s" % (message, timestamp))
        publish(
            '24',  # the name of the channel
            'approval',  # the `type` of the message/event,
            # clients use this name
            # to register event handlers

            # payload of the event, needs to be
            # a dict which is JSON dumpable.
            {'message': message,
             'timestamp': timestamp},

            sender='server'  # sender id of the event, can be None.
        )


if __name__ == '__main__':

    print("Running omnibus test ...")
    send_hello_world()
