---
title: The Confused Donut
time: 2026-06-30
categories: [reverse]
tags: [medium]
image: /assets/posts/chall_category/rev.jpg
---

## Description:

A psychedelic ASCII donut rave suddenly explodes onto your screen, spinning majestically in glorious 3D text. It's hypnotic. It's chaotic. It's aggressively colorful. But the real question is… is it malicious? Underneath all that sugary chaos, this binary behaves like a confused piece of malware that's had one too many glazed donuts. It sniffs around the system, looking for something very specific before it does anything interesting.

- Category: Reverse
- Difficulty: Medium
- SHA256: `4718c0e31f6d16feab7d402c40ce5025e650f55b28cbeadf1678e3c81b0eaaa4`
- **Flag format:** `HNYX{flag-string}`

<button onclick="downloadFile()">Download File</button>

<script>
function downloadFile() {
    const link = document.createElement('a');
    link.href = 'https://github.com/0x251e-challenge/challenges/raw/main/union-depository/reverse/the-confused-donut/Confused_Donut.exe';
    link.download = 'Confused_Donut.exe';
    link.click();
}
</script>

### Solution:

The name is the hint. "Confused" is **ConfuserEx**, and "Donut" is [TheWover/donut](https://github.com/TheWover/donut), the shellcode generator that turns a .NET assembly into position-independent shellcode. The spinning torus is set dressing over a two-layer packing job.

Here is the whole execution chain before we walk it, so no function name below is a forward reference:

![Execution chain of Confused_Donut.exe, from the WinForms entry point through the username check, the reversed-base64 shellcode stage, the Donut instance decryption, and finally payload.dll writing the flag to the registry](/assets/posts/chall-writeup-img/the-confused-donut/chain.png)

##### 1. It is not a native binary

`file` gives the game away immediately:

```
Confused_Donut.exe: PE32 executable for MS Windows 6.00 (GUI), Intel i386 Mono/.Net assembly, 3 sections
```

Worth confirming rather than trusting the magic-byte guess, since the challenge is themed around confusing your tools. Parsing the PE optional header directly shows a populated CLR Runtime Header data directory and an import table of only 75 bytes:

```
Import:     RVA=0x737750 size=0x4b
CLRHeader:  RVA=0x2008   size=0x48
```

75 bytes is just the `mscoree.dll!_CorExeMain` stub every pure-IL executable carries. There is no native code here to decompile, so IDA/Ghidra are the wrong tools. This is a job for a .NET decompiler.

##### 2. ConfuserEx, and why the CLR refuses to load it

`ilspycmd -p -o out Confused_Donut.exe` produces classes named `FGXZHV-74-qG-PokWY8--UYb-`, a `ConfusedByAttribute`, and methods drowned in flattened control flow:

```csharp
while (true)
{
    uint num4;
    switch ((num4 = (uint)(num2 ^ -929122793)) % 25)
    {
    case 20u:
        num2 = -2090575577;
        continue;
    ...
```

String literals are gone too, replaced by calls into `<Module>`:

```csharp
((Control)this).Text = <Module>.SomeMangledName<string>(3540647568u);
```

The obvious move is to load the assembly by reflection and just call those decryptor methods. That does not work — CoreCLR rejects the file outright:

```
System.BadImageFormatException: Enclosing type(s) not found for type '<invisible unicode>'
```

ConfuserEx names its nested types with zero-width and bidi control characters, and CoreCLR's metadata validation is stricter about the `NestedClass` table than ILSpy's reader is. (Clearing the `32BITREQUIRED` CLR flag on a scratch copy gets past an earlier architecture-mismatch error, but not this one.) So the strings have to be recovered statically. We will come back to that in step 4 — it turns out not to be on the critical path to the flag.

##### 3. The gate

Stripping the flattening out of the main form by hand, the actual logic is small. The constructor grabs the username, and the Enter key runs the check:

```csharp
_username = Environment.UserName;
_target   = <Module>.Decrypt<string>(1820023326u);

// on KeyDown, KeyCode == 13
if (_username.Equals(_target, StringComparison.OrdinalIgnoreCase))
{
    // success label + "kawfi" image, then:
    RunPayload();
}
// else: failure label + "whoareu" image, and RunPayload() is never reached
```

And `RunPayload` is textbook shellcode staging:

```csharp
char[] array = Resources.d0nut_glaz3.ToCharArray();
Array.Reverse(array);
byte[] sc = Convert.FromBase64String(new string(array));
IntPtr mem = VirtualAlloc(IntPtr.Zero, (uint)sc.Length, 0x3000, 0x40);   // MEM_COMMIT|RESERVE, PAGE_EXECUTE_READWRITE
Marshal.Copy(sc, 0, mem, sc.Length);
WaitForSingleObject(CreateThread(IntPtr.Zero, 0, mem, IntPtr.Zero, 0, IntPtr.Zero), uint.MaxValue);
```

The timer that draws the donut never touches any of this. It is a decoy.

##### 4. Recovering the encrypted strings

`d0nut_glaz3` is one of four resources, and the `.resx` gives us the names in the clear — `whoareu`, `kawfi`, `_0x251e` (bitmaps and the icon) and `d0nut_glaz3`, a plain string. But the *username* is still encrypted.

ConfuserEx's constant protection stores everything in one blob that `<Module>`'s static constructor builds at load time: a 16-word xorshift32 keystream (seed `3694288513`) XORed against 80 hardcoded `uint`s, with the ciphertext fed back into the keystream between blocks, producing 320 bytes — which are then LZMA-decompressed. Reimplementing just that part in Python:

```python
n = 3694288513
a2 = []
for _ in range(16):
    n ^= (n >> 12); n &= 0xFFFFFFFF
    n ^= (n << 25); n &= 0xFFFFFFFF
    n ^= (n >> 27); n &= 0xFFFFFFFF
    a2.append(n)

out = bytearray()
for blk in range(0, 80, 16):
    a4 = [arr[blk + i] ^ a2[i] for i in range(16)]
    for i in range(16):
        out += struct.pack("<I", a4[i])
        a2[i] ^= a4[i]
```

The first 13 bytes come out as `5d 00 00 80 00 54 01 ...` — properties byte `0x5d`, an 8 MiB dictionary, 340 bytes uncompressed. That is a textbook LZMA-alone header, which is the confirmation that the keystream reconstruction is right. `lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)` gives the blob (the stream has no end marker, so the one-shot `lzma.decompress` refuses it).

Each accessor is then `p = (key * mul) ^ xor`, masked to `0x3FFFFFFF` and shifted left by 2, pointing at a 4-byte length followed by UTF-8:

```python
p = ((key * mul) & 0xFFFFFFFF) ^ xor
p = (p & 0x3FFFFFFF) << 2
cnt = int.from_bytes(blob[p:p+4], "little")
s = blob[p+4:p+4+cnt].decode()
```

Which yields the lot:

```
1820023326 -> 'c0ff33'
3284779498 -> 'Yummy,tastYY c0ff33, but where is the flag ???'
4174686491 -> 'H0ld upp, waittt ahh minuutee, u aint no c0ff33'
 710923470 -> '.,-~:;=!*#$@'
4184389502 -> 'd0nut_glaz3'
2688180735 -> 'whoareu'
3478833676 -> 'kawfi'
 904582475 -> 'The Confused Donut'
```

So the "something very specific" it sniffs for is a username of **`c0ff33`**. Note the success message: even on the correct username, the flag is not printed. It has to come from the shellcode.

##### 5. The shellcode is Donut

Reverse the resource string, base64-decode it, and you get 22,367 bytes starting with:

```
e8 c0 29 00 00  c0 29 00 00  66 cb a9 d7 ...
```

`strings` on it returns nothing but noise, so the payload is encrypted. But that prologue is the whole ballgame. `E8 C0 29 00 00` is `call +0x29c0`, and a `call` pushes the address of the *next* byte — offset 5 — onto the stack. That is Donut handing its loader a pointer to its own `DONUT_INSTANCE`. Reading a `uint32` at offset 5 gives `0x29C0`, the instance length, and `5 + 0x29C0 = 0x29C5` is exactly the call target. Layout confirmed:

```
[0x0000] E8 stub (5 bytes)
[0x0005] DONUT_INSTANCE, 0x29C0 bytes
[0x29C5] loader code
```

I first tried emulating the shellcode with Speakeasy to let it unpack itself. It spun forever in Donut's API-hashing loop, because the hashes never match against a synthetic export table. Not worth chasing — the offline route is deterministic, because **Donut stores the instance key in plaintext inside the instance**:

```c
typedef struct _DONUT_INSTANCE {
    uint32_t    len;    // +0
    DONUT_CRYPT key;    // +4   : mk[16] then ctr[16]  <- plaintext
    ...
    int         api_cnt;  // <- everything from here is encrypted
```

The cipher is Chaskey in CTR mode. Porting `chaskey()` and `donut_encrypt()` from `encrypt.c` is ~40 lines, and donut ships test vectors so the implementation can be proven before it is pointed at anything:

```python
assert chaskey(key_tv, plain_tv) == cipher_tv   # passes
```

##### 6. Finding the real encryption boundary

Decrypting from `offsetof(DONUT_INSTANCE, api_cnt)` produced garbage. Compiling donut's own header gave `api_cnt = 568`, but this sample was built with a different version of donut, so that offset is simply wrong for this binary.

Rather than guess, brute-force the boundary and score each candidate against strings a Donut instance *must* contain (`ntdll`, `amsi`, `wldp`, `AmsiScanBuffer`, `v4.0.30319`, …):

```python
for e in range(0, 1200, 4):
    dec = donut_encrypt(key_mk, key_ctr, inst[e:e+2048])
    score = sum(1 for m in MARKERS if m in dec)
```

One offset wins outright:

```
score=8 offset=572 preview=b'?\x00\x00\x00ole32;oleaut32;wininet;mscoree;shell32\x00'
```

`0x3F` = 63 API hashes, then the DLL list. Decrypting from **572** gives a clean instance, and the module header falls out of it:

```
module type     = 1 (NET_DLL)
module compress = 1 (NONE)
runtime         = 'v4.0.30319'
class           = 'Payload.Flag'
method          = 'Run'
len             = 4608
```

##### 7. The payload

The embedded module is a plain 4,608-byte .NET DLL (for embedded instances donut does not separately encrypt the module — `mod_key` is only used for HTTP staging), starting at the `MZ` immediately after the module header. Carve it out and decompile:

```csharp
namespace Payload;

public class Flag
{
    public static void Run()
    {
        RegistryKey registryKey = Registry.CurrentUser.OpenSubKey(
            "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", writable: true);
        if (registryKey != null)
        {
            registryKey.SetValue("Flag", "HNYX{c0nfu$1nG_tH3_d0nUt_4_c0ff33}");
            registryKey.Close();
        }
    }
}
```

The flag is written to the registry and never drawn on screen, which is what the success message is teasing about. The two halves also corroborate each other: the flag ends in `_4_c0ff33`, and `c0ff33` is the username recovered independently back in step 4.

### Takeaways

- A `call` as the very first instruction of a blob is a strong tell for Donut, and the pushed return address doubles as the instance pointer. If `instance_offset + len` lands exactly on the call target, the layout is confirmed before decrypting anything.
- Donut keeps the instance key in plaintext at `instance+4`, so unpacking never requires running the shellcode. Emulation is the slower, more fragile path here.
- Do not trust struct offsets compiled from upstream headers against a sample whose tool version you do not know. Brute-forcing the boundary against expected known-plaintext is faster than version archaeology and tells you when you are right.
- Format alone does not confirm a flag, but internal consistency does — recovering `c0ff33` from the obfuscated constants and from the payload string by two independent routes is what makes the answer trustworthy.

**Flag:** `HNYX{c0nfu$1nG_tH3_d0nUt_4_c0ff33}`
