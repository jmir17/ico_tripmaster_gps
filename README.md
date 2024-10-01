# Rally ICO / Tripmaster GPS with a Raspberry Pico

This project contain the instructions and source code on how to build an *adventure-ready* ICO / Tripmaster to assist a Roadbook using GPS signal. Using the a low-cost Raspberry Pico with a GPS module.

## 🎯Objective  
Create a budget friendly navigation solution to enable the participation in motorbike offroad rallies.

## 🧭What are we building?
In short: a GPS-based **compass** and **odometer**.

In long: We'll use the precision of GPS satellites to give you real-time odometry data (so you know how far you've gone) and directional information (so you know you are in the right course) to guide you like a digital roadbook whisperer keeping you on track during a rally event.

#### How it should look like

![Roadbook](https://c8.alamy.com/comp/2F3BXC4/ambiance-roadbook-during-stage-10-of-the-dakar-2020-between-haradh-and-shubaytah-608-km-ss-534-km-in-saudi-arabia-on-january-15-2020-photo-francois-flamand-dppi-2F3BXC4.jpg)


### The Roadbook
In a rally, you know where you’re starting, you know where you’re finishing, but the path in between? That’s a mystery only the **roadbook** can reveal. This trusty guide holds the instructions for your route —because just winging it won’t cut it here. As you tear through the course, you’ll pass through certain key checkpoints to prove you didn’t accidentally skip a part (the rally organizers are on to you!).

![Roadbook Explain](https://thumb.ac-illust.com/bc/bcc5f61e5c3ea98060a2d641318a1fcd_t.jpeg)

The roadbook itself is a collection of essential instructions: distances, directions (yep, precise degrees), and notes like "don't crash here" (okay, maybe not that specific). All you have to do is follow them, one by one, until you cross that finish line. Simple, right? Well... not really. Getting lost, taking a few *scenic* detours, and doing some U-turns are just part of the fun in these events. But hey, that's what makes it an adventure!

### The ICO / Tripmaster
To master the art of following the roadbook, you’ll need more than just a gut feeling and good luck—you need an ICO/Tripmaster. This handy device tells you two critical things: which direction you’re heading and how far you've gone, so you know exactly when that next instruction is coming (before you drive into oblivion).

![Roadbook Pro](https://c8.alamy.com/comp/2F3B717/roadbook-on-a-bike-during-the-dakar-2019-stage-1-lima-to-pisco-peru-on-january-7-photo-florent-gooden-dppi-2F3B717.jpg)

And since getting lost is basically a rally rite of passage, the Tripmaster should come with a quick and easy way to reset or adjust your distance. Because, let’s face it, you’ll probably have to recalibrate after realizing that "this way" was, in fact, the wrong way. But no worries, it’s all part of the rally charm!

## 🛠️Let's build!

#### Components required
 - Raspberry Pico           
 - LCD Screen 16x2          
 - GPS NEO M8N              
 - GPS Antenna        
 - Motorcycle Switch     
 - Cable                    

#### Connection diagram
Here the connection diagram:

![Connection Schema](https://imgur.com/a/IwaabVy)
![Connection Schema Local](img/schema.png)



