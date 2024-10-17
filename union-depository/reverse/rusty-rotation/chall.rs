use std::io::{self, Write};

fn main() {
    println!("\n=== rruussttyy R0tAT10nN ===\n");
    println!("Give me the flag I'll give you points ;)\n");
    print!("flag: ");
    io::stdout().flush().unwrap();

    let mut flag = String::new();
    io::stdin()
        .read_line(&mut flag)
        .expect("Failed to read input");
    let flag = flag.trim();
    let mut out = String::new();

    for (i, c) in flag.chars().enumerate() {
        let new_char = (c as u8).wrapping_sub((i as u8) + 3);
        out.push(new_char as char);
    }

    if out == "@PAukjliihlD@D0b6[Yg" {
        println!("correct! +999 points");
    } else {
        println!("wrong! try again --_--)");
    }
}

