help:
	twistd motd_manhole --help

run-manhole:
	twistd -n motd_manhole --sshPort=9999 -p etc/passwd

run-insults:
	twistd -n motd_insults --sshPort=9999 -p etc/passwd

shell:
	@echo
	@echo "Just hit <ENTER> when prompted for a password ..."
	@echo
	-@ssh -p 9999 user@localhost
