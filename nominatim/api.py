# SPDX-License-Identifier: GPL-2.0-only
#
# This file is part of Nominatim. (https://nominatim.org)
#
# Copyright (C) 2022 by the Nominatim developer community.
# For a full list of authors see the git log.
"""
Implementation of classes for API access via libraries.
"""
from typing import Mapping, Optional
import asyncio
from pathlib import Path

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import create_async_engine

from nominatim.config import Configuration
from nominatim.apicmd.status import get_status, StatusResult

class NominatimAPIAsync:
    """ API loader asynchornous version.
    """
    def __init__(self, project_dir: Path,
                 environ: Optional[Mapping[str, str]] = None) -> None:
        self.config = Configuration(project_dir, environ)

        dsn = self.config.get_database_params()

        dburl = URL.create(
                   'postgresql+asyncpg',
                   database=dsn.get('dbname'),
                   username=dsn.get('user'), password=dsn.get('password'),
                   host=dsn.get('host'), port=int(dsn['port']) if 'port' in dsn else None,
                   query={k: v for k, v in dsn.items()
                          if k not in ('user', 'password', 'dbname', 'host', 'port')})
        self.engine = create_async_engine(dburl,
                                          connect_args={"server_settings": {"jit": "off"}},
                                          future=True)


    async def status(self) -> StatusResult:
        """ Return the status of the database.
        """
        return await get_status(self.engine)


class NominatimAPI:
    """ API loader, synchronous version.
    """

    def __init__(self, project_dir: Path,
                 environ: Optional[Mapping[str, str]] = None) -> None:
        self.async_api = NominatimAPIAsync(project_dir, environ)


    def status(self) -> StatusResult:
        """ Return the status of the database.
        """
        return asyncio.get_event_loop().run_until_complete(self.async_api.status())
