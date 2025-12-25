use std::fs;
use std::iter;

fn find_joltage(row: &[u32]) -> Option<u32> {
    /*
    // Functional approach
    // need to use the move keyword to take ownership of row to use `first_digit`
    row.iter()
        .enumerate()
        .flat_map(|(idx, &first_digit)| {
            // For every digit, look at every digit that comes after it
            row.iter()
                .skip(idx + 1)
                .map(move |&second_digit| first_digit * 10 + second_digit)
        })
        .max()
    */

    /*
    // Imperative approach
    let mut max_val = None;

    for (idx, &first) in row.iter().enumerate() {
        for &second in row.iter().skip(idx + 1) {
            let val = first * 10 + second;
            if max_val.map_or(true, |m| val > m) {
                max_val = Some(val);
            }
        }
    }

    max_val
    */

    row.iter()
        .enumerate()
        .flat_map(|(idx, &first_digit)| {
            // Create a stream of just `first_digit` repeated
            iter::repeat(first_digit)
                // Zip it with remaining digits, knows when to stop by skip length
                .zip(row.iter().skip(idx + 1))
        })
        .map(|(first, &second)| first * 10 + second)
        .max()
        
}

// Pointer approach, zero allocations
fn find_joltage_v2(row: &[u32]) -> Option<u64> {
    let cap = 12;
    let n = row.len();

    let mut result: u64 = 0;
    let mut current_idx = 0;

    // Loop cap times in reverse
    for i in (1..=cap).rev() {
        let search_end = n - i + 1;

        // Realistically, this will never happen
        if current_idx >= search_end {
            return None;
        }

        // Slice to look at the window
        let window = &row[current_idx..search_end];
        let max_val = window.iter().max()?; // same as top in Python

        // Accumulate as we go
        result = result * 10 + (*max_val as u64);

        let offset = window.iter().position(|x| x == max_val)?;

        current_idx += offset + 1;
    }

    Some(result)
}

fn main() {
    let input = fs::read_to_string("day03/day03.txt").unwrap();

    let joltage_rating: Vec<Vec<u32>> = input
        .lines()
        .map(|line| {
            line.trim()
                .chars()
                .filter_map(|c| c.to_digit(10))  // '2' -> 2
                .collect()
        })
        .collect();

    // Part 1

    let total_joltage: u32 = joltage_rating
        .iter()
        .filter_map(|row| find_joltage(row))
        .sum();
    
    println!("Advent of Code Day 3 Answer Part 1: {}", total_joltage);

    // Part 2

    let total_joltage_v2: u64 = joltage_rating
        .iter()
        .filter_map(|row| find_joltage_v2(row))
        .sum();

    println!("Advent of Code Day 3 Answer Part 2: {}", total_joltage_v2);
}