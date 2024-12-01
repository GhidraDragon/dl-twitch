while true; do
  python dl_twitch.py -NV -TS &
  python_pid=$!
  wait $python_pid
  rm *journal*
done
