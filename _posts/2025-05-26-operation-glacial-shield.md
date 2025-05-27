---
title: Operation Glacial Shield
time: 2025-05-26
categories: [osint]
tags: [hard, reverse image search]
image: /assets/posts/chall_category/osint.jpg
---

As part of an OSINT investigation analyst, you have received an email containing two images linked to a suspected environment crime. Your task is to examine the visual evidence, identify the precise location of interest, and report the exact coordinates. Accuracy and urgency are critical, lives are depending on it. 

- Category: OSINT
- **Flag format:** `bbctf{latitude_longitude}` rounded to three decimal places.

<button onclick="downloadFile()">Download File</button>

<script>
function downloadFile() {
    const link = document.createElement('a');
    link.href = 'https://github.com/0x251e-challenge/challenges/raw/main/union-depository/osint/operation-glacial-sheild/operation_glacial_shield.eml';
    link.download = 'operation_glacial_shield.eml';
    link.click();
}
</script>

### Solution:

