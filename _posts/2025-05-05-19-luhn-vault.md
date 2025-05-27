---
title: Luhn's Vault
time: 2025-05-17
categories: [reverse]
tags: [easy]
image: /assets/posts/chall_category/rev.jpg
---

### Description:

The mysterious cryptographer Luhn created a safe vault that verifies numerical inputs using a technique he knows. For years, the vault has guaranteed its secrets, now is your time to crack the secret to unlock the vault. 

- Category: Reverse 
- **Flag format:** `bbctf{[a-zA-Z0-9]+\}`

<button onclick="downloadFile()">Download File</button>

<script>
function downloadFile() {
    const link = document.createElement('a');
    link.href = 'https://github.com/0x251e-challenge/challenges/raw/main/union-depository/reverse/luhn-vault/luhn-vault.exe';
    link.download = 'luhn-vault.exe';
    link.click();
}
</script>

### Solution:

##### 1. Disassemble and decompile, using graph mode to analyze the entry point

![luhn-vault-1.jpg](/assets/posts/chall-writeup-img/luhn-vault/luhn-vault-1.jpg) 

As this executable is a Windows GUI application which WinMain is the entry point. 

![luhn-vault-2.jpg](/assets/posts/chall-writeup-img/luhn-vault/luhn-vault-2.jpg) 

##### 2. Analyze WinMain function 

Here is the decompiled C code of WinMain function:

```c 
int __stdcall WinMain(HINSTANCE hInst, HINSTANCE hPreInst, LPSTR lpszCmdLine, int nCmdShow)
{
  MSG Msg; // [esp+38h] [ebp-50h] BYREF
  WNDCLASSA WndClass; // [esp+54h] [ebp-34h] BYREF
  HWND hWnd; // [esp+7Ch] [ebp-Ch]

  memset(&WndClass, 0, sizeof(WndClass));
  WndClass.lpfnWndProc = WindowProc;
  WndClass.hInstance = hInst;
  WndClass.lpszClassName = "FlagWindowClass";
  RegisterClassA(&WndClass);
  hWnd = CreateWindowExA(
           0,
           "FlagWindowClass",
           "Luhn's Vault",
           0xCF0000u,
           0x80000000,
           0x80000000,
           400,
           100,
           0,
           0,
           hInst,
           0);
  ShowWindow(hWnd, nCmdShow);
  while ( GetMessageA(&Msg, 0, 0, 0) )
  {
    TranslateMessage(&Msg);
    DispatchMessageA(&Msg);
  }
  return 0;
}
```
As Windows GUI application runs with event handling function, it will have **WindowProc** as a callback function that will process messages sent to the interface. 

##### 3. Analyze WindowProc function

Here is the decompiled C code for WindowProc function:

```c 
LRESULT __stdcall WindowProc(HWND hWndParent, UINT Msg, WPARAM wParam, LPARAM lParam)
{
  HWND DlgItem; // eax
  char __stream[4]; // [esp+3Fh] [ebp-69h] BYREF
  int v7; // [esp+43h] [ebp-65h]
  int v8; // [esp+47h] [ebp-61h]
  int v9; // [esp+4Bh] [ebp-5Dh]
  int v10; // [esp+4Fh] [ebp-59h]
  int v11; // [esp+53h] [ebp-55h]
  int v12; // [esp+57h] [ebp-51h]
  int v13; // [esp+5Bh] [ebp-4Dh]
  int v14; // [esp+5Fh] [ebp-49h]
  int v15; // [esp+63h] [ebp-45h]
  int v16; // [esp+67h] [ebp-41h]
  int v17; // [esp+6Bh] [ebp-3Dh]
  __int16 v18; // [esp+6Fh] [ebp-39h]
  char v19[10]; // [esp+71h] [ebp-37h] BYREF
  char v20[20]; // [esp+7Bh] [ebp-2Dh] BYREF
  CHAR String[25]; // [esp+8Fh] [ebp-19h] BYREF

  if ( Msg == 273 )
  {
    if ( (_WORD)wParam == 2 )
    {
      DlgItem = GetDlgItem(hWndParent, 1);
      GetWindowTextA(DlgItem, String, 17);
      if ( strlen(String) == 16 )
      {
        if ( luhnCheck(String) )
        {
          *(_DWORD *)__stream = 0;
          v7 = 0;
          v8 = 0;
          v9 = 0;
          v10 = 0;
          v11 = 0;
          v12 = 0;
          v13 = 0;
          v14 = 0;
          v15 = 0;
          v16 = 0;
          v17 = 0;
          v18 = 0;
          decryptFlagPart(&encryptedFirstPart, 9, v20);
          if ( checkSecondPart(String, v19) )
            snprintf(__stream, 0x32u, "bbctf{}\n... hey that is mine!!!", v20, v19);
          else
            snprintf(__stream, 0x32u, "bbctf{... but is it mine thou ???", v20);
          MessageBoxA(hWndParent, __stream, "Flag Found!", 0);
        }
        else
        {
          MessageBoxA(hWndParent, "Aint no Luhn's number that!", "Error", 0);
        }
      }
      else
      {
        MessageBoxA(hWndParent, "Sweet 16 darling", "Error", 0);
      }
    }
  }
  else
  {
    if ( Msg > 0x111 )
      return DefWindowProcA(hWndParent, Msg, wParam, lParam);
    if ( Msg == 1 )
    {
      CreateWindowExA(0, "EDIT", &WindowName, 0x50800080u, 10, 10, 250, 25, hWndParent, (HMENU)1, 0, 0);
      CreateWindowExA(0, "BUTTON", "CRACK IT", 0x50000001u, 270, 10, 80, 25, hWndParent, (HMENU)2, 0, 0);
    }
    else
    {
      if ( Msg != 2 )
        return DefWindowProcA(hWndParent, Msg, wParam, lParam);
      PostQuitMessage(0);
    }
  }
  return 0;
}
```

Now within this function of WindowProc, it shows logic handling and extra string processing function. 

At this part, we able to perform backtracing since we notice some unique strings such as `Flag Found` and `bbctf{ }`. 

![luhn-vault-3](/assets/posts/chall-writeup-img/luhn-vault/luhn-vault-3.jpg) 

##### 4. Analyze luhnCheck function 

In order to reverse and find out the input validation process, we first have to understand the logic handling of luhnCheck function, here is the decompiled C code of it:

```c 
BOOL __cdecl luhnCheck(char *Str)
{
  int v2; // [esp+20h] [ebp-18h]
  signed int i; // [esp+24h] [ebp-14h]
  BOOL v4; // [esp+28h] [ebp-10h]
  int v5; // [esp+2Ch] [ebp-Ch]

  v5 = 0;
  v4 = 0;
  for ( i = strlen(Str) - 1; i >= 0; --i )
  {
    v2 = Str[i] - 48;
    if ( v4 )
      v2 = 2 * v2 / 10 + 2 * v2 % 10;
    v5 += v2;
    v4 = !v4;
  }
  return v5 % 10 == 0;
}
```

The function checks whether the input passes the Luhn algorithm which is a common way to validate credit card numbers. Before it process the input, it needs the 16 digits of input. The function takes in parameters of the 16 digits number input but in the form of char and then converts the ascii to numerical by subtracting with 48. After that it performs a luhn algorithm check to determine a valid unique 16 digits number. 

**Conditions to get the first part of the flag**:
- 16 digits -> strlen(String)==16
- luhnCheck will return true/false after mod with 10, if return result is 0 true otherwise is false


