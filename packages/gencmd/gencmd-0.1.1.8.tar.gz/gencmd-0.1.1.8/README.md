# gencmd
Simple library (python3) for send commands to the video-core on Raspberry Pi

## motivation
When I've tested my own solution to measure voltage and temperature on video-core. I discovered that run 'gencmd' directly like a process sometimes is not good enough. For example, in the case when the measurement frequency is less than one second. So there is a simple library for pass commands directly to the video-core.