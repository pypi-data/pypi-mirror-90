"""
Constants for MCDR
"""

import os


VERSION = '1.0.0-alpha.3'
VERSION_PYPI = '1.0.0a3'
NAME_SHORT = 'MCDR'
NAME = 'MCDReforged'
GITHUB_URL = 'https://github.com/Fallen-Breath/MCDReforged'
GITHUB_API_LATEST = 'https://api.github.com/repos/Fallen-Breath/MCDReforged/releases/latest'

LOGGING_FILE = os.path.join('log', '{}.log'.format(NAME_SHORT))
PARSER_FOLDER = os.path.join('mcdreforged', 'parser')
RESOURCE_FOLDER = 'resources'
RE_DEATH_MESSAGE_FILE = os.path.join(RESOURCE_FOLDER, 'death_message.yml')
UPDATE_DOWNLOAD_FOLDER = 'MCDR_update'
BASIC_PARSER_NAME = 'basic_parser'

PARSER_FILE_SUFFIX = '.py'
REACTOR_FILE_SUFFIX = '.py'
PLUGIN_FILE_SUFFIX = '.py'
DISABLED_PLUGIN_FILE_SUFFIX = '.disabled'
LANGUAGE_FILE_SUFFIX = '.yml'

PLUGIN_THREAD_POOL_SIZE = 4
MAX_TASK_QUEUE_SIZE = 2048
WAIT_TIME_AFTER_SERVER_STDOUT_END_SEC = 60
REACTOR_QUEUE_FULL_WARN_INTERVAL_SEC = 5
