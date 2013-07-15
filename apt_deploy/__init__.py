import logging
import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('apt-deploy')
import subprocess
from subprocess import call

from apt_deploy import apt_deployconfig

LEVELS = (  logging.ERROR,
            logging.WARNING,
            logging.INFO,
            logging.DEBUG,
            )

def main():
    version = apt_deployconfig.__version__
    # Support for command line options.
    usage = _("apt-deploy [options]")
    parser = optparse.OptionParser(version="%%prog %s" % version, usage=usage)
    parser.add_option('-d', '--debug', dest='debug_mode', action='store_true',
        help=_('Print the maximum debugging info (implies -vv)'))
    parser.add_option('-v', '--verbose', dest='logging_level', action='count',
        help=_('set error_level output to warning, info, and then debug'))
    # exemple of silly CLI option
    parser.add_option("-f", "--config-file", action="store", dest="configFile",
                      help=_("specify host list file location"))
    parser.set_defaults(logging_level=0, foo=None)
    (options, args) = parser.parse_args()

    # set the verbosity
    if options.debug_mode:
        options.logging_level = 3
    logging.basicConfig(level=LEVELS[options.logging_level], format='%(asctime)s %(levelname)s %(message)s')


    # Run your cli application there.
    #print _("I'm launched and my args are: %s") % (" ".join(args))

    if options.configFile:
         configFile = options.configFile
    else:
         configFile = '/etc/apt-deploy/host-list.conf'

    f = open(configFile, 'r')
    print f

    cmd = _("apt-get %s") % ("".join(args))

    for host in f:
         call(["ssh", "-lroot", host, cmd]),

    print "-----apt-deploy complete-----"

    logging.debug(_('end of prog'))


if __name__ == "__main__":
    main()
