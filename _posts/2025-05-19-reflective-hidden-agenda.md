---
title: Reflective Hidden Agenda
time: 2025-05-19
categories: [reverse]
tags: [medium]
image: /assets/posts/chall_category/rev.jpg
---

## Description:

Sam, a gamer struggling to level up, stumbles upon a mysterious DLL named Helper.dll in a gaming forum. The post claims it enhances gameplay, but Sam is skeptical. After uploading it to VirusTotal and seeing minimal detections, Sam decides to test it. Upon loading the DLL into the game, it unexpectedly launches Notepad. Confused, Sam notices that some parts in the DLL starts to wipe itself. There’s definitely a hidden agenda at play. 

- Category: Reverse
- **Flag format:** `bbctf{[a-zA-Z0-9]+\}`

<button onclick="downloadFile()">Download File</button>

<script>
function downloadFile() {
    const link = document.createElement('a');
    link.href = 'https://github.com/0x251e-challenge/challenges/raw/main/union-depository/reverse/reflective-hidden-agenda/Helper.dll';
    link.download = 'Helper.dll';
    link.click();
}
</script>

### Solution:

