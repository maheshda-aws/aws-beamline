#!/usr/bin/env python3
import os
import sys
import time
import logging
from datetime import datetime
from argparse import ArgumentParser

from awsbeamline.session import Session

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class Beamline():

    def __init__(self):
        parser = ArgumentParser(
            description="Beamline command line",
            usage="""./beamline <command> [<args>]

            The most commonly used beamline commands are:
            register                         Registers a task with beamline
            submit                           Submits a task instance that's already registered.
            execute_task_instance            Executes task in client mode
        """)
        parser.add_argument("command", help="Subcommand to run")
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            logging.error("Unrecognized command")
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def register(self):
        parser = ArgumentParser(description="Generates a task definition")
        parser.add_argument("-c", "--config-file", action="store", dest="config_file", help="Task config file path")
        parser.add_argument("-o", "--overwrite", action="store_true", dest="overwrite", help="Overwrite existing ")
        args = parser.parse_args(sys.argv[2:])
        logging.info("Register task , arguments={}".format(args))
        session = Session(job_config_location=args.config_file)
        session.task_manager.register_task(args.overwrite)

    def submit(self):
        parser = ArgumentParser(description="Creates job instance and submits to AWS Batch cluster")
        parser.add_argument("-n", "--name", action="store", dest="profile_name", help="Task profile name")
        parser.add_argument("-c", "--config-file", action="store", dest="config_file", help="Task config file in S3")
        parser.add_argument("-d", "--rundate", action="store", dest="run_date", help="Run date  for task instance.")
        parser.add_argument("-f", "--rundateformat", action="store", dest="run_date_format", default="%Y-%m-%dT%H:%M:%S", help="Run date format in unix format for task instance.")
        parser.add_argument("-a", "--async", action="store_true", dest="is_async", help="Boolean value to wait for task completion. When not provided: False")
        args = parser.parse_args(sys.argv[2:])
        logging.info("Submitting task to beamline cluster, arguments={}".format(args))

    def execute_task_instance(self):
        parser = ArgumentParser(description="Execute task instance in client mode")
        parser.add_argument("-n", "--name", action="store", dest="profile_name", help="Task profile name")
        parser.add_argument("-c", "--config-file", action="store", dest="config_file", help="Task config file in S3")
        parser.add_argument("-d", "--rundate", action="store", dest="run_date", help="Run date  for task instance.", default=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        parser.add_argument("-f", "--rundateformat", action="store", dest="run_date_format", help="Run date format in unix format for task instance." , default="%Y-%m-%dT%H:%M:%S")
        args = parser.parse_args(sys.argv[2:])
        logging.info("Executing beamline task in client mode, arguments={}".format(args))
        session = Session(job_config_location=args.config_file,
                          run_date_str=args.run_date,
                          profile_name=args.profile_name,
                          run_date_format=args.run_date_format
                        )
        # Make sure the config replaces wildcard here.
        session.task_manager.execute_sparksql_task()
if __name__ == '__main__':
    Beamline()





