"""
This is a tiny layer that takes care  of initialising the shared
application layers (storage, logs) when running standalone workers
without having to initialise the HTTP framework (or other ones)
"""

from common.bootstrap import AppConfig, application_init
from common.telemetry import instrument_third_party

# These instrumentors patch and wrap libraries, we want
# to execute them ASAP
instrument_third_party()
application_init(AppConfig())
