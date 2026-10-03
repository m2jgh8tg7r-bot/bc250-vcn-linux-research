export LC_ALL=C
[[ -t 0 ]] && tty_status=YES || tty_status=NO
marker "INPUT_READY stdin_tty=$tty_status expected_bytes=18 diagnostic_only=YES"
stty -a </dev/console
acknowledgement=''
IFS= read -r acknowledgement
read_rc=$?
printf -v escaped '%q' "${acknowledgement:0:64}"
marker "INPUT_RESULT read_rc=$read_rc bytes=${#acknowledgement} escaped_prefix=$escaped"
if ((read_rc != 0)); then
    marker 'INPUT_READ_FAILURE; EOF or read error; GPU not included'
elif [[ "$acknowledgement" != 'R299-CP03-RECEIVED' ]]; then
    marker 'INPUT_MISMATCH; GPU not included'
else
    marker 'INPUT_EXACT_MATCH; diagnostic complete; GPU not included'
fi
