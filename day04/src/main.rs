use std::fs;

fn count_neighbors(arr: &[Vec<char>], r: usize, c: usize) -> usize {
    /* Functional Approach - for learning
    (-1..=1)
        .flat_map(|dr| (-1..=1).map(move |dc| (dr, dc)))
            .filter(|&(dr, dc)| !(dr == 0 && dc == 0))
            .filter_map(|(dr, dc)| {
                let nr = r as isize + dr;
                let nc = c as isize + dc;
                arr.get(nr as usize).and_then(|row| row.get(nc as usize))
            })
            .filter(|&&val| val == '@')
            .count()
    */
    
    // Do a bunch of `isize` casting in order to handle negative indices
    let rows = arr.len() as isize;
    let cols = arr[0].len() as isize;
    let mut count = 0;

    for dr in -1..=1 {
        for dc in -1..=1 {
            if dr == 0 && dc == 0 {
                continue;
            }

            let nr = r as isize + dr;
            let nc = c as isize + dc;

            if nr >= 0 && nr < rows && nc >= 0 && nc < cols {
                if arr[nr as usize][nc as usize] == '@' {
                    count += 1;
                }
            }
        }
    }

    count
}

fn main() {
    let input = fs::read_to_string("day04/day04.txt").unwrap();

    let mut grid: Vec<Vec<char>> = input
        .lines()
        .map(|line| line.trim().chars().collect())
        .collect();

    // Part 1

    let row = grid.len();
    let col = grid[0].len();

    let mut rolls_of_paper = 0;
    for r in 0..row {
        for c in 0..col {
            if grid[r][c] == '@' {
                let neighbors = count_neighbors(&grid, r, c);
                if neighbors < 4 {
                    rolls_of_paper += 1;
                }
            }
        }
    }

    println!("Advent of Code Day 4 Answer Part 1: {}", rolls_of_paper);

    // Part 2

    let mut removal_steps = 0;
    // Equivalent to while true in Python
    loop {
        let mut to_change = Vec::new();

        // Cells to change
        for r in 0..row {
            for c in 0..col {
                if grid[r][c] == '@' {
                    let neighbors = count_neighbors(&grid, r, c);
                    if neighbors < 4 {
                        to_change.push((r, c));
                    }
                }
            }
        }

        if to_change.is_empty() {
           break;
        }

        for (r, c) in to_change {
            grid[r][c] = '.';
            removal_steps += 1;
        }
    }

    println!("Advent of Code Day 4 Answer Part 2: {}", removal_steps);
}