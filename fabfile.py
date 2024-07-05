# -*- coding: utf-8 -*-

from boto3 import client as aws
from fabric import Connection
from fabric.tasks import task
from termcolor import colored

SSH_USER = "cristhian"

INSTANCES_SSH = {
    "main": "seek.demo.pe",
}

REGIONS = ["us-east-1"]

WORK_DIR = "/home/{}/code".format(SSH_USER)
GIT_DIR = WORK_DIR

instances = []
instances_hosts = []


@task
def pull(c, stage):
    with c.cd(GIT_DIR):
        print(colored("Pulling changes ...", "white"))
        c.run("git fetch && git checkout {} && git pull origin {}".format(stage, stage))
        print(colored("Pulled changes", "white"))


@task
def dependencies(c):
    with c.cd(WORK_DIR):
        print(colored("Installing dependencies ...", "white"))
        if c.run("test -d {}/venv/".format(WORK_DIR), warn=True).failed:
            print(colored("Creating venv ...", "white"))
            c.run("python3 -m venv venv")
            print(colored("Created venv", "white"))
        c.run("source venv/bin/activate && pip install --upgrade pip setuptools wheel")
        c.run("source venv/bin/activate && pip install -r requirements.txt --upgrade")
        print(colored("Installed dependencies", "white"))


@task
def actions(c, stage):
    with c.cd(WORK_DIR):
        print(colored("Updating settings ...", "white"))
        c.run("source venv/bin/activate && scripts/settings/{}.sh".format(stage))
        print(colored("Updated settings", "white"))


@task
def actions_only_once(c, stage):
    with c.cd(WORK_DIR):
        print(colored("Migrating database ...", "white"))
        c.run("source venv/bin/activate && scripts/migrations/run.sh")
        print(colored("Migrated database", "white"))
        print(colored("Loading data ...", "white"))
        c.run("source venv/bin/activate && scripts/data.sh")
        print(colored("Loaded data", "white"))
        print(colored("Updating static files ...", "white"))
        c.run("source venv/bin/activate && scripts/static.sh")
        print(colored("Update static files", "white"))


@task
def supervisorctl(c, stage):
    print(colored("Obtaining supervisor files ...", "white"))
    c.sudo("ln -sf {}/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf".format(WORK_DIR))
    print(colored("Obtained configuration files", "white"))
    print(colored("Restarting supervisor ...", "white"))
    c.sudo("supervisorctl reread")
    c.sudo("supervisorctl update")
    c.sudo("supervisorctl restart gunicorn")
    c.sudo("supervisorctl status gunicorn")
    print(colored("Restarted supervisor", "white"))


@task
def nginx(c):
    print(colored("Restarting nginx ...", "white"))
    c.sudo("service nginx restart")
    print(colored("Restarted nginx", "white"))


@task
def instances_deploy(c, stage):
    get_instances_hosts(c, stage)
    for h_index, h in enumerate(instances_hosts):
        print(colored("Deploying ...", "white", attrs=["bold"]))
        pull(h, stage)
        dependencies(h)
        actions(h, stage)
        if h_index == 0:
            actions_only_once(h, stage)
        supervisorctl(h, stage)
        logs(h, stage)
        nginx(h)
        print(colored("Deployed", "white", attrs=["bold"]))


@task
def instances_system_update(c):
    get_instances_hosts(c, stage)
    for h in instances_hosts:
        print(colored("Updating system ...", "white", attrs=["bold"]))
        h.sudo("apt-get -y update")
        h.sudo("apt-get -y upgrade")
        print(colored("Updated system", "white", attrs=["bold"]))


@task
def instances_delete_logs(c, stage):
    get_instances_hosts(c, stage)
    for h in instances_hosts:
        print(colored("Deleting logs ...", "white", attrs=["bold"]))
        h.sudo("rm -R /var/log/*.log")
        print(colored("Deleted logs", "white", attrs=["bold"]))


@task
def instances_reboot(c):
    get_instances_hosts(c, stage)
    for h in instances_hosts:
        print(colored("Restarting server ...", "red", attrs=["bold"]))
        h.sudo("reboot")
        print(colored("Restarted server", "red", attrs=["bold"]))


@task
def where(c, stage):
    get_instances_hosts(c, stage)


def _aws_create_connection(region="us-east-1"):
    print(colored("Connecting to AWS in {} ...".format(region), "green"))
    connection = aws("ec2", region_name=region)
    print(colored("Connection with AWS in {} established".format(region), "green"))
    return connection


@task
def get_instances_hosts(c, stage):
    print(colored("Obtaining instances ...", "green", attrs=["bold"]))
    global instances
    global instances_hosts
    if not stage in INSTANCES_SSH:
        print(colored("stage {} is not defined".format(stage), "red", attrs=["bold"]))
    instances = _filter_hosts(INSTANCES_SSH[stage], stage)
    instances_hosts = [
        {
            "host": i,
            "user": SSH_USER,
            "inline_ssh_env": True,
        }
        for i in instances
    ]
    instances_hosts = [Connection(**i, gateway=Connection(**instance_door)) for i in instances_hosts]
    print(colored("Obtained instances", "green", attrs=["bold"]))


def _filter_hosts(name, stage):
    print(colored("Filtering instances ...", "green"))
    DNS = []
    for region in REGIONS:
        connection = _aws_create_connection(region)
        tags = [
            {"Name": "tag:Name", "Values": [name]},
            {"Name": "tag:Stage", "Values": [stage]},
        ]
        instances = connection.describe_instances(Filters=tags)
        for reservation in instances["Reservations"]:
            for instance in reservation["Instances"]:
                if instance["State"]["Name"] == "running":
                    DNS.append(str(instance["PrivateIpAddress"]))
    DNS = sorted(DNS)
    print(colored(" - ".join(DNS), "white", attrs=["bold"]))
    print(colored("Filtered instances by tags", "green"))
    return DNS
