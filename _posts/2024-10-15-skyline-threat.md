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


