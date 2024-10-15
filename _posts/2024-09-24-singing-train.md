---
title: Singing Train
time: 2024-09-24
categories: [osint]
tags: [reverse image search, easy]
image: /assets/posts/chall_category/osint.jpg
---

## Description:

While on a recent trip, I encountered an intriguing train. Unfortunately, video recording wasn’t allowed, so I captured its sound instead. Can you tell me the nickname of this locomotive. Maybe you can ask help from someone who is both a mechnical engineer and musician.

- Category: OSINT
- **Flag:** CTF{nickname-of-train}

<button onclick="downloadFile()">Download Audio File</button>

<script>
function downloadFile() {
    const link = document.createElement('a');
    link.href = 'https://github.com/0x251e/challenges/raw/main/union-depository/osint/singing-train/chall.mp3';
    link.download = '';
    link.click();
}
</script>



