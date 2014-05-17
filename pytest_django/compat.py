# In Django 1.6, the old test runner was deprecated, and the useful bits were
# moved out of the test runner

try:
    from django.test.runner import DiscoverRunner as DjangoTestRunner
except ImportError:
    from django.test.simple import DjangoTestSuiteRunner as DjangoTestRunner

_runner = DjangoTestRunner(interactive=False)


try:
    from django.test.runner import setup_databases
except ImportError:
    setup_databases = _runner.setup_databases

teardown_databases = _runner.teardown_databases

try:
    from django.test.utils import (setup_test_environment,
                                   teardown_test_environment)
except ImportError:
    setup_test_environment = _runner.setup_test_environment
    teardown_test_environment = _runner.teardown_test_environment


del _runner


try:
    from django import setup
except ImportError:
    # Emulate Django 1.7 django.setup() with get_models
    from django.db.models import get_models as setup
    setup


# OperationalError was introduced in Django 1.6
# Guess OperationalErrors for other databases for older versions of Django
def _get_operational_errors():
    try:
        from django.db.utils import OperationalError
        return OperationalError
    except ImportError:
        errors = []

    try:
        import MySQLdb
        errors.append(MySQLdb.OperationalError)
    except ImportError:
        pass

    try:
        import psycopg2
        errors.append(psycopg2.OperationalError)
    except ImportError:
        pass

    return tuple(errors)


OPERATIONAL_ERRORS = _get_operational_errors()