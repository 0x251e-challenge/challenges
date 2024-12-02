---
title: Skyline Threat
time: 2024-10-15
categories: [osint]
tags: [reverse image search, medium]
image: /assets/posts/chall_category/osint.jpg
---

An investigation authority found an image from a terrorists’ email without any context but with the title **“Next attack”**. They have to find out which airport, which airline hanger and which aircraft. Are you able to assist them in this investigation ?

The flag format is **CTF{AIRPORT_AIRLINE_AIRCRAFT}**. `AIRPORT` is the 3 letter IATA airport code, `AIRLINE` is the 2 letter IATA code, and `AIRCRAFT` is the aircraft model and variant (omit manufacturer name). 

For example: 
KLIA, Airasia, Airbus A320-200 -> `CTF{KUL_AK_A320-200}`
KKIA, MAS, Boeing 737-300 -> `CTF{BKI_MH_B737-300}`

- Category: OSINT
- **Flag format:** `CTF{AIRPORT_AIRLINE_AIRCRAFT}`

![chall.png](/union-depository/osint/skyline-threat/chall.png)

# Solutions:

This is the image given. If you zoom in, you can see a logo with three boxes.

![1](/assets/posts/chall-writeup-img/skyline-threat/1.png)

Throw the picture into google lens and you will find that the company name is called
Cargolux Airlines. The IATA code for Cargolux Airlines is **CV**. I also found out from google
lens that this airport is in Luxembourg through this link:

[https://www.wikiloc.com/trails/mountain-biking/luxembourg/luxembourg/fentange](https://www.wikiloc.com/trails/mountain-biking/luxembourg/luxembourg/fentange)

The only airport in Luxembourg is called Luxembourg Findel Airport.

![2](/assets/posts/chall-writeup-img/skyline-threat/2.png)

Now that we got the airport name, it’s IATA is **LUX**. Next, we are going to find the aircraft.
This airline commonly operates Boeing 747 variants for cargo transport. From the image, it
seems likely to be a **Boeing 747-400F (freighter)** or a newer **747-8F**, both popular models
used by Cargolux.

[https://www.cargolux.com/fleet-equipment/](https://www.cargolux.com/fleet-equipment/)

![3](/assets/posts/chall-writeup-img/skyline-threat/3.png)

**Flag:** `CTF{LUX_CV_B747-400F}`

### Credits:
Thanks to Wong Wan Yin from MCC 2024 manage to solve the challenge with the writeup. 
