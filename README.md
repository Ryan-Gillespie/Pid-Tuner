# Pid-Tuner

Uses a genetic algorithm to tune PID Robotic control loops. This was made during my time on a FIRST Robotics team when we were encountering difficulties tuning our PID loops. 
This program uses a custom-built simulator as a fitness function to quickly find a viable PID candidate for testing on a phisical robot.

## Results of Testing

While this did produce some PID triplets that were usable as real PID loops, the simulator is very forgiving. This resulted in far too many PID loops making it past their testing phase.
