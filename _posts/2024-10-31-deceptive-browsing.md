---
title: Deceptive Browsing
time: 2024-10-31
categories: [malware analysis]
tags: [easy, trojan, AutoIt]
image: /assets/posts/chall_category/malware-analysis.png
---

## Description:

A 32-bit executable, seemingly harmless, opens a Google search page upon launch to blend in. However, something isn’t right—it’s quietly orchestrating actions in the background. Examine the suspicious activity and bring its hidden motives to light.

- Category: Malware Analysis
- **Flag:** CTF{Flag}
- Password for the challenge file: `infected`

<button onclick="downloadFile()">Download File</button>

<script>
function downloadFile() {
    const link = document.createElement('a');
    link.href = 'https://github.com/0x251e-challenge/challenges/raw/refs/heads/main/union-depository/malware-analysis/deceptive-browsing/mal.7z';
    link.download = 'mal.7z';
    link.click();
}
</script>

