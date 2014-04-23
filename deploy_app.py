#!/usr/bin/env python
import os
import sys
from fabric.api import env, run, settings, put, sudo
from configparser import ConfigParser, ExtendedInterpolation

# load config file
conf_file = "deploy_app.conf"
conf = ConfigParser(interpolation=ExtendedInterpolation())
try: conf.read(conf_file)
except: 
    sys.exit('Cannot read configuration file %s; exiting.' % conf_file) 
try: 
    branch = conf.get('main', 'branch')
    username = conf.get('main', 'username')
    ip_address = conf.get('main', 'ip_address')
    web_dir = conf.get('main', 'web_dir')
    git_archive = conf.get('main', 'git_archive')
except: 
    sys.exit("Bad configuration file; exiting.")

# check if we can SSH into the machine
with settings(warn_only=True):
    env.host_string = ip_address
    env.reject_unknown_hosts = False
    env.user = username 
    result = run("ls")
    if 0 != result.return_code:
        sys.exit('SSH test failed. ls output: ' + result)

# export git archive
os.system("git archive --format zip --output {git_archive} {branch}".format(git_archive=git_archive,branch=branch))

# upload
run("mkdir -p {0}".format(web_dir))
put(git_archive, web_dir)
run("cd {0}; unzip {1}".format(web_dir,git_archive))
sudo("cd {web_dir}; chown -R www-data:www-data {web_dir}".format(web_dir=web_dir))

# cleanup
os.system("rm {0}".format(git_archive))


