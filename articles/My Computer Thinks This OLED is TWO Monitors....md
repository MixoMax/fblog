# My Computer Thinks This OLED is TWO Monitors....
## Date: 2024-07-07

Topics: Hardware, Display, OLED, LG, 4K, 1080p, 480Hz, 240Hz, Dual Mode, Gaming, Monitor, Review

### Written by: Linus Sebastian (Linus Tech Tips)

["Linus Tech Tips - My Computer Thinks This OLED is TWO Monitors...."](https://www.youtube.com/watch?v=eJX-SJx-kQo)

---

**Dual Mode OLED Display: A New Generation of Displays**
=====================================================

This is part of a new generation of OLED displays that LG is calling "dual mode." It allows you to switch between the native 4K resolution and 1080p resolution. But wait, you must be thinking, "I can do that on my monitor right now." Is my monitor dual mode or not? Yes, but also no. If you have a modern display, it may be capable of interpreting a signal in all of those different modes, but only one of them is native, able to be displayed cleanly without any scaling. That's the trick here, or at least it would be if it worked as well as...

**Sponsor: UG Green**
--------------------

Before we get into the details, let's take a look at our sponsor, UG Green. Their super compact two-in-one magnetic foldable charging station features a 15W C2 charger for your phone, a 5W wireless charger for earbuds, and a pass-through port for plugging in a USB-C cable. Check it out at the link below.

**Dual Mode in Action**
---------------------

Let's try the two different modes because there's more to this than just setting it to the ideal mode and then forgetting about it forever. In theory, a display like this can offer the best of both worlds. Right now, we're looking at 4K 240Hz, obviously with outstanding picture clarity and amazing motion clarity. But because of how human vision works, OLED is still going to have some drawbacks compared to a classic CRT monitor, unless you use black frame insertion to artificially strobe the image.

**Mode Toggle**
-------------

We experimented with this before we started, and it turns out that mid-game, at least in this game, I can just press the mode toggle button, and now we're looking at 1080p 4:180Hz. We still get the same outstanding HDR and color performance, but at this size, I would say the image clarity is a bit of a drag. The upside is that by running at a lower resolution, we overcome the limitations of our DisplayPort link, and we can run it at a whopping 480 refreshers per second.

**EDID and Refresh Rate**
-------------------------

But why can't I just go into the advanced Windows menu and change my refresh rate here? Well, no. Since the days of this connector, monitors have included a bit of metadata called EDID. The EDID's purpose is to report the display's capabilities to any connected device, be it a computer or game console or what have you. This monitor has two EDIDs, which can be toggled through the OSD or this little button right here. We extracted them, ran them through an interpreter, and had a look at the output. Surprisingly, the only major difference is that the 4K mode will not allow the display to be driven past 240Hz, regardless of the configured resolution in the Windows settings, and the 1080p EDID doesn't list as many resolutions and maxes out at 1080p 480Hz.

**Performance and Limitations**
-----------------------------

Let's talk about the performance of the display and determine whether this thing is even worth jumping through all these hoops for. Starting with color accuracy, sRGB mode is solidly okay. The color temperature is a little cool, but if you don't know what that means, you're unlikely to notice it, and if you do, you can simply calibrate your troubles away. At least, unless you want to use gamer mode, unfortunately, it is tuned for colors that are pretty but not accurate. No problem, just ignore it then, right? I guess.

**Responsiveness and Latency**
-----------------------------

This is a gaming monitor first and foremost, and both of the modes are great, but they have some small differences. Because it refreshes at half the rate, the 4K mode has inherently worse input latency, of course. We're talking about a difference of about 1 millisecond, so who cares, right? Well, hold on. We've said for years that there's a point of diminishing returns past about 240Hz, but the reason that faster matters for OLED displays is because of how our eyes perceive motion. By switching more frequently, we will see fast-moving objects with better clarity.

**Scaling and Integer Scaling**
-------------------------------

The 1080p mode has a curious trait of its own, though. If you run it at a lower refresh rate, the latency goes up more faster than you would expect. Perhaps it has something to do with scaling those inputs. It is a 4K native panel, regardless of whether it's running in a 1080p mode, and scaling is impossible to avoid on a modern display because these panels are made up of a fixed array of pixels that can't change in size or shape.

**Conclusion**
----------

In summary, then, this is an intriguing product, hopefully a solution that we just won't need a few years from now. But if you want tomorrow's tech today and you don't mind pressing this switch depending on what mode you want to run in and what game you're running, and also if you don't mind spending $1,400, you're getting a genuinely impressive piece of technology, even if there are a few limitations.

**Sponsor: "Delete Me"**
--------------------

Delete Me isn't just about individuals; it's about families. That's why Delete Me is expanding to cover everyone you care about. Their new family plans make sharing and caring as simple as it can get. With their family account management, you can easily add family members, ensuring personalized protection for each person. Their privacy-first design means every family member gets their own data sheet, keeping their online footprint secure from kids to adults, everyone's covered, reducing the risk of exposure, spam, and scams. And with simplified management, overseeing your family's privacy has never been easier. Choose Delete Me for peace of mind for your entire family in the digital world. Check them out at the link below today and use the code LT at checkout for 20% off.

Thanks for watching, guys!