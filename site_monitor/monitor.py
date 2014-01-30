#!/usr/bin/env python
__author__ = 'cahitonur'
# Simple site monitor.
# Usage: $ python monitor.py domain time_interval
# Usage example: $ python monitor.py github.com 60

from sys import argv
import urllib2
from smtplib import SMTP
import re
import time
import sched
import threading

scheduler = sched.scheduler(time.time, time.sleep)


def connection_is_on():
    """
    Check the internet connection by getting status of google and yahoo.
    They can't be down at the same time, right?
    """
    g = get_status('http://google.com')
    y = get_status('http://yahoo.com')
    if g and y:
        return True
    else:
        return False


def get_status(url):
    """
    Open given url and check the response status code against 200 and 302.
    If response status code is something else we can consider that the server is down.
    """
    url = normalize_url(url)
    url_file = urllib2.urlopen(url)
    response = url_file.code

    if response in (200, 302):
        return True
    else:
        return False


def email_alert(status):
    """
    Simple e-mail sender.
    Takes only one argument which will be used for both subject and message body.
    """
    sender = 'monitor@yourdomain.com'  # E-mail account to send alert mails.
    password = 'password'
    recipient = 'you@gmail.com'  # Recipient address for down alerts.
    server = SMTP('mail.your_domain.com:25')  # Your email server and port to login and send mails.
    server.ehlo()
    server.starttls()
    server.login(sender, password)
    headers = ["from: " + sender,
               "subject: " + status,
               "to: " + recipient,
               "mime-version: 1.0",
               "content-type: text/html"]
    headers = "\r\n".join(headers)
    server.sendmail(sender, recipient, headers + "\r\n\r\n" + status)
    server.quit()


def normalize_url(url):
    """
    If a url doesn't have a http/https prefix, add http://
    """
    if not re.match('^http[s]?://', url):
        url = "http://" + url
    return url


def test(url):
    """
    First check the internet connection if it's on then check the requested url.
    """
    if connection_is_on():
        site_is_up = get_status(url)
        if site_is_up:
            pass
        else:
            status = '%s is down!' % url
            email_alert(status)
    else:
        print 'Internet connection is down!'


def periodic(shclr, intrvl, action, action_args):
    """
    Scheduler to check server status in given time intervals.
    """
    shclr.enter(intrvl, 1, periodic,
                (shclr, intrvl, action, action_args))
    action(action_args)


if __name__ == '__main__':
    site_url = argv[1]
    interval = int(argv[2])
    periodic(scheduler, interval, test, site_url)

    t = threading.Thread(target=scheduler.run)
    t.start()