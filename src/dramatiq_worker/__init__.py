"""
This is a tiny layer that takes care  of initialising the shared
application layers (storage, logs) when running standalone workers
without having to initialise the HTTP framework (or other ones)
"""

from common.bootstrap import AppConfig, application_init

application_init(AppConfig())
