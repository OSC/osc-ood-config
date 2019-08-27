#!/bin/bash
#PBS -j oe
#PBS -l nodes=1:ppn=1
#PBS -l walltime=00:59:00
#PBS -N ondemand/sys/myjobs/vnc_job

module load turbovnc

# Note the default path for this would be $HOME/.vnc/passwd
PASSWD_FILE_PATH="$(pwd)/vnc.passwd"

notify_by_email () {
    # Change if you prefer be emailed somewhere else
    EMAIL_ADDRESS="$USER@osc.edu"
    echo "Successfully started VNC server on $1$2 using password: $3" | mail -s "VNC session ready" "$EMAIL_ADDRESS"
}

# Create a random password for VNC use
# Defaults to 8 characters long
create_passwd () {
  tr -cd 'a-zA-Z0-9' < /dev/urandom 2> /dev/null | head -c"${1:-8}"
}

# Setup one-time use passwords and initialize the VNC password in the current working directory
# If you do not want to usage a different password each time this is a place to make that change
# The default VNC password file is stored at $HOME/.vnc/passwd, and we are intentionally NOT
# clobbering that file
set_vnc_passwd () {
  echo "Setting VNC password..."
  password=$(create_passwd "8")
  spassword=${spassword:-$(create_passwd "8")}
  (
    umask 077
    echo -ne "${password}\n${spassword}" | vncpasswd -f > "$PASSWD_FILE_PATH"
  )

  echo "$password"
}

# Start up vnc server
start_vnc_session () {
    # (if at first you don't succeed, try, try again)
    for i in $(seq 1 10); do
      # Clean up any old VNC sessions you own that weren't cleaned before
      vncserver -list | awk '/^:/{system("kill -0 "$2" 2>/dev/null || vncserver -kill "$1)}'

      # Attempt to start VNC server
      VNC_OUT=$(vncserver -log "$(pwd)/vnc.log" -rfbauth "$PASSWD_FILE_PATH" -nohttpd -noxstartup -geometry 1152x720 -idletimeout 0  2>&1)
      VNC_PID=$(pgrep -s 0 Xvnc) # the script above will daemonize the Xvnc process

      # Sometimes Xvnc hangs if it fails to find working display, we
      # should kill it and try again
      kill -0 "${VNC_PID}" 2>/dev/null && [[ "${VNC_OUT}" =~ "Fatal server error" ]] && kill -TERM "${VNC_PID}"

      # Check that Xvnc process is running, if not assume it died and
      # wait some random period of time before restarting
      kill -0 "${VNC_PID}" 2>/dev/null || sleep "0.$(random_number 1 9)s"

      # If running, then all is well and break out of loop
      kill -0 "${VNC_PID}" 2>/dev/null && break
    done

    # If we fail to start it after so many tries, then just give up
    kill -0 "${VNC_PID}" 2>/dev/null

    # Parse output for ports used
    display=$(echo "${VNC_OUT}" | awk -F':' '/^Desktop/{print $NF}')
    port=$((5900+display))

    # Ensure that VNC_PID is not blank
    if [[ -z "$VNC_PID" ]]; then
        echo "VNC does not appear to be running. Exiting."
        exit 1
    fi

    echo "$VNC_PID:$display:$port"
}

wait_for_pid_to_end () {
  echo "Waiting on $1"
    while [[ -d "/proc/$1" ]]; do
        sleep 0.1
    done
}

main () {
    # Optionally perform work before starting the VNC session

    PASSWD="$(set_vnc_passwd)"
    # Set host of current machine
    PID_PORT=$(start_vnc_session)
    PID_TO_WAIT_ON=$(echo "$PID_PORT" | cut -d ':' -f 1)
    DISPLAY=":$(echo "$PID_PORT" | cut -d ':' -f 2)"
    # Some VNC viewers may prefer to know the port instead of the display
    PORT=$(echo "$PID_PORT" | cut -d ':' -f 3)

    export DISPLAY

    # Send yourself an email when the VNC session starts with the hostname, DISPLAY, and VNC password
    notify_by_email "$(hostname)" "$DISPLAY" "$PASSWD"

    # To be able to resize windows etc you will need a window manager
    # The one that will take the least resources away from your other work is probably Flux box
    # An example of Flux box being used may be found here:
    # https://github.com/OSC/bc_osc_abaqus/blob/d67d5b81cff0de609957d378f0f56b5da4973bb1/template/script.sh.erb#L21-L28

    # Start a graphical program here
    # e.g.
    # xeyes &
    # PID_TO_WAIT_ON= $(pgrep -u$USER xeyes)"

    wait_for_pid_to_end "$PID_TO_WAIT_ON"

    # Optionally perform work after the graphical session ends like moving files.
    # !! This is only safe to do if PID_TO_WAIT_ON is captured from a graphical  !!
    # !! program which can be exited; The PID returned by start_vnc_session is   !!
    # !! safe to use because it will not end until the job is qdel'd or has run  !!
    # !! out of time.                                                            !!
}
main
