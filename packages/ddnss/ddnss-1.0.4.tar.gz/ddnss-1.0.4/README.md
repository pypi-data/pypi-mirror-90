# ddnss
Script to update DynDNS hosts registered at ddnss.de.

## Installation
Install ddnss from the [AUR](https://aur.archlinux.org/packages/python-ddnss/) or via:

    pip install ddnss

## Usage
You can run the client from the console via

    ddnssupd <host> [-k <key>] [-f <config_file>] [-d]

Per default, the config file is read from `/etc/ddnss.conf` on POSIX systems and from `%LOCALAPPDATA%\ddnss.conf` on Windows systems.

## Configuration file
The expected config file format is a simple INI-Style:

    [<host>]
    key = <key>

## License
Copyright (C) 2018-2020 Richard Neumann <mail at richard dash neumann period de>

ddnss is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ddnss is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ddnss.  If not, see <http://www.gnu.org/licenses/>.
