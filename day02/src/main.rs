use std::fs;

#[derive(Debug)]
struct Ids {
    first: u64,
    last: u64,
}

fn generate_combinations(num_str: &str) -> bool {
    let n_full = num_str.len();
    let mut n_half = n_full / 2;

    while n_half > 0 {
        let base = &num_str[0..n_half];
        /*
        // Python solution logic translated to Rust
        let mut count = 0;

        for i in (n_half..n_full).step_by(n_half) {
            // handles case where length of num_str is not multiple of n_half
            let end = std::cmp::min(i + n_half, n_full);
            let elem = &num_str[i..end];

            if elem != base {
                count += 1;
            }
        }

        if count == 0 {
            return true;
        }
        */
        if n_full % n_half == 0 {
            // need to convert to byte array as that is what chunks needs
            let all_match = num_str.as_bytes()
                .chunks(n_half)
                .all(|chunk| chunk == base.as_bytes());

            if all_match {
                return true;
            }
        }
        n_half -= 1;
    }

    false
}

fn main() {
    let input = fs::read_to_string("day02/day02.txt").unwrap();

    let elf_ids: Vec<Ids> = input
        .lines()
        .flat_map(|line| line.split(","))
        .filter_map(|line| {
            let (left, right) = line.trim().split_once("-")?;
            Some(Ids {
                first: left.parse().ok()?,
                last: right.parse().ok()?,
            })
        })
        .collect();
    /* 
    // just want this here as a learning mechanism
    let elf_ids: Vec<Ids> = input
        .lines()
        .flat_map(|line| line.split(","))
        .filter(|id_range| !id_range.is_empty())
        .map(|id_range| {
            let (left, right) = id_range.trim().split_once("-").unwrap();
            Ids {
                first: left.parse().unwrap(),
                last: right.parse().unwrap(),
            }
        })
        .collect();
    */

    // Part 1

    // just use elf_ids.iter() when chaining methods
    let mut invalid_ids: Vec<u64> = Vec::new();
    for pair in &elf_ids {
        for num in pair.first..=pair.last {
            let str_num = num.to_string();
            let n = str_num.len();

            if n % 2 == 0 && str_num[..n / 2] == str_num[n / 2..] {  
                invalid_ids.push(num);  
            }
        }
    }

    let total_invalid_ids: u64 = invalid_ids.iter().sum();
    println!("Advent of Code Day 2 Answer Part 1: {}", total_invalid_ids);

    // Part 2

    invalid_ids.clear();
    for pair in &elf_ids {
        for num in pair.first..=pair.last {
            let str_num = num.to_string();
            if generate_combinations(&str_num) {
                invalid_ids.push(num);
            }
        }
    }

    let total_invalid_ids: u64 = invalid_ids.iter().sum();
    println!("Advent of Code Day 2 Answer Part 2: {}", total_invalid_ids);

}