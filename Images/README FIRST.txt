i have uploaded the image of the load on my Laptop when handling multiple requests by the backend

my laptop specs
Ryzen 7 5800H ( 8 cores 16 threads )
GPU : Nvidia Geforce RTx 3070 mobile 8GB 
RAM : 16 GB DDR4 3200 MHz

i have first uploaded the load on my laptop without starting anything.
this helps see the ambient load and thus find the actual load the backend is facing.

my naming scheme:
for the images containing data, i will use two numbers scheme
XxYy
where X = Number of users (peak concurrency)
Y = Ramp Up (users started / second)
Ex. 50x100y means 50 max number of users and 100 users started per second


Also, 
XxYya and XxYyb means different data for XxYy


for 1000x1000y i have shown how the load isn't a problem after the server is running properly after a while it has started. only during the start there is high failure.
