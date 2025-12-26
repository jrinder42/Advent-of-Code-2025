use std::fs;
use std::collections::HashSet;

fn main() {
    let input = fs::read_to_string("day07/day07.txt").unwrap();

    let grid: Vec<Vec<char>> = input
        .lines()
        .map(|line| line.trim().chars().collect())
        .collect();

    let height = grid.len();
    let width = grid[0].len();

    // Part 1 and Part 2

    let start_col = grid[0]
        .iter()
        .position(|&c| c == 'S')
        .unwrap();

    // `current_beams[col]` = # of beams at column `col` in the current row
    let mut current_beams = vec![0u64; width];
    current_beams[start_col] = 1; // Fill in one beam at 'S'

    let mut visited_splitters = HashSet::new();

    for y in 0..height - 1 {
        let mut next_beams = vec![0u64; width];

        for x in 0..width {
            let count = current_beams[x];
            if count == 0 {
                continue;
            }

            let target_char = grid[y + 1][x];

            match target_char {
                '^' => {
                    visited_splitters.insert((y + 1, x));

                    if x > 0 {
                        next_beams[x - 1] += count;
                    }
                    if x + 1 < width {
                        next_beams[x + 1] += count;
                    }
                }
                _ => {
                    next_beams[x] += count;
                }
            }
        }
        current_beams = next_beams;
    }

    let total_beams: u64 = current_beams.iter().sum();

    println!("Advent of Code Day 7 Answer Part 1: {}", visited_splitters.len());
    println!("Advent of Code Day 7 Answer Part 2: {}", total_beams);
}