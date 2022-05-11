import os
from subprocess import call
from invoke import task

CURR_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(CURR_DIR, "game")
UNIT_TEST_DIR = os.path.join(CURR_DIR, "game","tests","unit_tests")
INTEGR_TEST_DIR = os.path.join(CURR_DIR, "game","tests", "integration")
COV_PATH = os.path.join(CURR_DIR, ".coveragerc")
LINT_PATH = os.path.join(CURR_DIR, ".pylintrc")

@task
def style(_):
    call(f"pycodestyle {SRC_DIR} --ignore=E501", shell=True)

@task
def lint(_):
    call(f"pylint {SRC_DIR} --rcfile {LINT_PATH}", shell=True)

@task
def unit_tests(_):
    cmd = f"pytest {UNIT_TEST_DIR} --cov {SRC_DIR} --cov-config={COV_PATH}"
    print(cmd)
    call(cmd, shell=True)

@task
def integr_test(_):
    cmd = f"pytest {INTEGR_TEST_DIR}"
    print(cmd)
    call(cmd, shell=True)