#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2013 Paul Robichaud <paul@paulrobichaud.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys

try:
    import DistUtilsExtra.auto
except ImportError:
    print >> sys.stderr, 'To build apt-deploy you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'

def update_config(values = {}):

    oldvalues = {}
    try:
        fin = file('apt_deploy/apt_deployconfig.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ') # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find apt_deploy/apt_deployconfig.py")
        sys.exit(1)
    return oldvalues


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        values = {'__apt_deploy_data_directory__': "'%s'" % (self.prefix + '/share/apt-deploy/'),
                  '__version__': "'%s'" % (self.distribution.get_version())}
        previous_values = update_config(values)
        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)


        
##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################

DistUtilsExtra.auto.setup(
    name='apt-deploy',
    version='13.04',
    license='GPL-3',
    author='Paul Robichaud',
    author_email='paul@paulrobichaud.com',
    #description='UI for managing …',
    #long_description='Here a longer description',
    url='https://launchpad.net/apt-deploy',
    cmdclass={'install': InstallAndUpdateDataDirectory}
    )

