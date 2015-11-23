#
# Regular cron jobs for the zipnish-ui package
#
0 4	* * *	root	[ -x /usr/bin/zipnish-ui_maintenance ] && /usr/bin/zipnish-ui_maintenance
