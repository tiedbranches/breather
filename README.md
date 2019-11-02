# breather

Breather is connected to Arduino1 which sends breathing data wirelessly to Arduino2. Arduino2 then sends the data over a serial connection to a Python script that processes the data (smoothing and hopefully in/out detection) before sending it back to Arduino2, which in turn drives a stepper.
