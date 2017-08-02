#!/usr/bin/env python2.7
import os, sys, re, glob
# import subprocess
import argparse
import yaml
import logging 
# import numpy as np
from datetime import datetime

class YAMLChecker():
    def __init__(self, yaml_fname, logger=None):
        self.yaml_fname = yaml_fname
        self.yaml = self.read_config(self.yaml_fname)
        self.logger = logger or logging.getLogger(__name__).addHandler(logging.StreamHandler(sys.stdout)) # TODO look up best practices for passing logger in vs stdout

    def read_config(self, yaml_fname):
        with open(yaml_fname, "r") as f:
            return yaml.load(f)

    '''
    Extract a property defined in the yaml file.

    Nested configs can be extracted by separating the variable names with ':'. For example,
    in this yaml

    layer 1:
        layer 2: property

    'property' would be accessed by 'layer 1:layer 2'.
    '''
    def get_variable(self, var_name):
        nested_names = var_name.split(":")
        current_layer = self.config
        for name in nested_names:
            print name
            current_layer = current_layer.get(name)
        return current_layer

    ### Definitions of validation functions

    def check_defined(self, var_name):
        var = self.get_variable(var_name)
        if var is None:
            msg = "--- Variable %s must be defined." % var_name
            self.logger.error(msg)
            raise ValueError(msg)
        else:
            self.logger.debug("... Variable %s ok." % var_name)

    def check_nonempty_str(self, var_name):
        var = self.get_variable(var_name)
        if var is None or not isinstance(var, basestring) or len(var) == 0:
            msg = "--- Variable %s must be a string that is >=1 char long." % var_name
            self.logger.error(msg)
            raise ValueError(msg)
        else:
            self.logger.debug("... Variable %s ok." % var_name)

    def check_file_exists(self, var_name, optional=False):
        var = self.get_variable(var_name)
        if var is None or not isinstance(var, basestring) or not os.path.isfile(var):
            if optional:
                msg = "--- Variable %s does not exist yet. May be generated by this program." % var_name
                self.logger.warning(msg)
            else:
                msg = "--- Variable %s must be present and contain a valid file name." % var_name
                self.logger.error(msg)
                raise ValueError(msg)
        else:
            self.logger.debug("... Variable %s ok." % var_name)

    def check_directory(self, var_name, makedirs=False):
        var = self.get_variable(var_name)
        if var is None or not isinstance(var, basestring) or not os.path.isdir(var):
            if makedirs:
                os.makedirs(var)
                self.logger.debug("... Making directories: %s" % var)
            else:
                msg = "--- Variable %s must contain a valid directory; given %s" % (var_name, var)
                self.logger.error(msg)
                raise ValueError(msg)
        else:
            self.logger.debug("... Variable %s ok." % var_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description="""Read in a YAML file, and easily retrieve nested variables and check variables for existence.""",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(dest="config_file", help="""YAML configuration file""")
    parser.add_argument("--logfile", dest="log_file", default="yaml_checker.log", type=str,
    help="""Specify the log file for this run.""")
    parser.add_argument("--loglevel", dest="log_level", default="INFO", type=str,
    help="""Specify the log level for this run (DEBUG, INFO, WARNING, etc)""")
    args = parser.parse_args()

    numeric_log_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_log_level, int):
        raise ValueError('Invalid log level: %s' % args.log_level)
    
    logger.addHandler(logging.StreamHandler())
    logger.addHandler(logging.FileHandler(args.log_file))
    logger.setLevel(numeric_log_level)
    
    logger.info('Inputs:\n  config file: %s\n  log file: %s\n  log level: %s\n' % (args.config_file, args.log_file, args.log_level))
    logger.info('Run initiated at: %s' % (str(datetime.now())))

    yaml_chk = YAMLChecker(args.config_file, logger)
    config = read_config(args.config_file)
    run_alleleseq_pipeline(config)

