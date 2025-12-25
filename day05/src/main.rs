use std::fs;
use std::ops::RangeInclusive;

fn main() {
    let input = fs::read_to_string("day05/day05.txt").unwrap();

    // Split the input
    let (ranges_part, numbers_part) = input.split_once("\n\n").unwrap();

    // Parse ranges
    let ranges: Vec<RangeInclusive<u64>> = ranges_part
        .lines()
        .map(|line| {
            let (start, end) = line.split_once("-").unwrap();
            let start = start.parse().unwrap();
            let end = end.parse().unwrap();
            start..=end
        })
        .collect();

    // Parse numbers
    let numbers: Vec<u64> = numbers_part
        .lines()
        .map(|line| line.parse().unwrap())
        .collect();

    // Part 1

    /*
    // Functional approach
    let count: usize = numbers
        .iter()
        .map(|&num| {
            // `as usize` converts bool to 0 or 1
            ranges.iter().any(|range| range.contains(&num)) as usize
        })
        .sum();

    // or

    let count: usize = numbers
        .iter()
        .filter(|&&num| ranges.iter().any(|range| range.contains(&num)))
        .count();
    */

    let mut count = 0;

    for &num in &numbers {
        if ranges.iter().any(|range| range.contains(&num)) {
            count += 1;
        }
    }

    println!("Advent of Code Day 5 Answer Part 1: {}", count);

    // Part 2

    let mut sorted_ranges = ranges.clone();
    sorted_ranges.sort_by_key(|range| *range.start());

    /*
    Can also use something like this to verify a non-empty vector

    if let Some(first) = sorted_ranges.first() {
        let mut current_start = *first.start();
        let mut current_end = *first.end();
        // proceed with merging
    } else {
        // handle empty case
    }
    */
    if sorted_ranges.is_empty() {
        println!("Advent of Code Day 5 Answer Part 2: Empty Vector");
        return;
    }
    
    let mut merged_ranges: Vec<RangeInclusive<u64>> = Vec::new();

    // Merge overlapping ranges, safe way to handle empty vectors
    
    // First range
    let first = sorted_ranges.first().unwrap();
    let mut current_start = *first.start();
    let mut current_end = *first.end();

    for range in sorted_ranges.iter().skip(1) {
        let next_start = *range.start();
        let next_end = *range.end();

        if next_start <= current_end + 1 {
            // Extend the current end as we have sorted ranges by start
            current_end = current_end.max(next_end);
        } else {
            // No overlap
            merged_ranges.push(current_start..=current_end);
            current_start = next_start;
            current_end = next_end;
        }
    }
    merged_ranges.push(current_start..=current_end);

    // Ingredient IDs --> Functional approach :)
    let total_count: u64 = merged_ranges
        .iter()
        .map(|range| range.end() - range.start() + 1)
        .sum();

    println!("Advent of Code Day 5 Answer Part 2: {}", total_count);
}