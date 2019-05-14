./cleanup.sh
while true; do
    python3 -W ignore implementation-demo.py &
    sleep 15
    echo Reloading script...
    ./cleanup.sh
done
./cleanup.sh
