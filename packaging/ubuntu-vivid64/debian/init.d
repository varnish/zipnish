#!/bin/sh
### BEGIN INIT INFO
# Provides:          zipnish-ui
# Required-Start:    $local_fs $network $remote_fs $syslog
# Required-Stop:     $local_fs $network $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Zipnish user interface service
# Description:       Written in python mainly using the flask framework.
#                    <...>
#                    <...>
### END INIT INFO

# Author: Muhammad Adeel <adeel@varnish-software.com>

# Do NOT "set -e"

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="zipnish-ui"
NAME=zipnish-ui
DAEMON="/usr/share/zipnish/ui/venv/bin/python /usr/share/zipnish/ui/app.py"
DAEMON_ARGS=""
PIDFILE=/var/run/$NAME.pid
SCRIPTNAME=/etc/init.d/$NAME

# Exit if the package is not installed
[ -x "$DAEMON" ] || exit 0

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Load the VERBOSE setting and other rcS variables
. /lib/init/vars.sh

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.2-14) to ensure that this file is present
# and status_of_proc is working.
. /lib/lsb/init-functions

case "$1" in
  start)
  	echo -n "Starting daemon: "$NAME
	start-stop-daemon --start --quiet --make-pidfile --pidfile $PIDFILE --exec $DAEMON --name $NAME --background
	;;
  stop)
  	echo -n "Stopping daemon: "$NAME
	start-stop-daemon --stop --quiet --oknodo --pidfile $PIDFILE
	;;
  status)
	status_of_proc "$DAEMON" "$NAME" && exit 0 || exit $?
	;;
  restart|force-reload)
  	echo -n "Restarting daemon: "$NAME
  	start-stop-daemon --stop --quiet --oknodo --pidfile $PIDFILE
	start-stop-daemon --start --quiet --exec $DAEMON --name $NAME --background --pidfile $PIDFILE
	;;
  *)
	echo "Usage: $SCRIPTNAME {start|stop|status|restart}" >&2
	exit 1
	;;
esac

exit 0