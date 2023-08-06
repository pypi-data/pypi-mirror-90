#!/bin/bash

TARGET_FILE_ABS="$1"

CONFIG_FILE="./config.json"

function config(){
	# function that reads JSON config file and returns value for var_name or default if var_name not found.
	var_name=$1
	default=$2

	echo "$(jq -e --raw-output ".$var_name // empty" $CONFIG_FILE; [[ $? = 0 ]] || echo "$default")"
}

URL=$(config URL "10.0.0.13:3000/ingress")
EVOECO_AUTH=$(config EVOECO_AUTH "AWDID, CLUSTERID")

SENT_DIR=$(config SENT_DIR "/var/evo-track/ingress/delivered")

echo "uploading: $TARGET_FILE_ABS"

# url should be variable (env?)
# i have made up the fact that -d means post (look it up)
# to lock the file during execution, use flock -x "/path/to/file" "some command" "file"
#
# on success, delete file (or maybe move to a graveyard that can be pruned in days via cron)
# on failure/on lock, flock should automatically do this
# "-n" means check for lock, -m might mean override
# curl "http://..." -d



# http://manpages.ubuntu.com/manpages/xenial/man1/flock.1.html	see "Examples" section
(
	flock -n 9 || exit 1
	#flock 9 || echo 1
	# ... commands executed under lock ...
	
	echo
	
	# https://stackoverflow.com/a/7173011/14362052
	# use --data-binary to send file with new lines
	# more than one file may be submitted, but the same key needs to be used. each file needs an additional `--form "data=@..."`
	curl "$URL" \
		--request POST \
		--header "Content-Type: multipart/form-data" \
		--header "Authorization: TODO" \
		--header "EvoEco-Authorization: $EVOECO_AUTH" \
		--form "data=@$TARGET_FILE_ABS" \
	| jq

	EXIT_CODE="$?"
	printf "\nexit code: %s\n" $EXIT_CODE

	#EXIT_CODE=0
	if [ "$EXIT_CODE" = "0" ]; then
		echo "successful post, removing $TARGET_FILE_ABS"
		#sudo mv "$TARGET_FILE_ABS" "$SENT_DIR"
		sudo rm "$TARGET_FILE_ABS"
	else
		echo "failed: [$EXIT_CODE] ($TARGET_FILE_ABS -> $URL)[$HTTP_CODE]"
	fi

) 9<"$TARGET_FILE_ABS"

