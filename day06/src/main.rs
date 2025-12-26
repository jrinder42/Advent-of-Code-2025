use std::fs;

fn main() {
    let input = fs::read_to_string("day06/day06.txt").unwrap();
    
    let lines: Vec<&str> = input.lines().collect();

    // `split_last` gives us the last element and the rest as a slice
    let (operator_line, number_lines) = lines.split_last().unwrap();

    // Part 1

    // Split by whitespace
    let part1_operations: Vec<char> = operator_line
        .split_whitespace()
        .map(|s| s.chars().next().unwrap()) // Take the first char of each token
        .collect();

    // buckets to hold numbers for each column index
    let mut part1_cols: Vec<Vec<u64>> = vec![Vec::new(); part1_operations.len()];

    for line in number_lines {
        // split_whitespace() ignores multiple spaces and aligns by token order
        // We don't dereference `num_str` because it is a string
        for (i, num_str) in line.split_whitespace().enumerate() {
            if i < part1_cols.len() {
                // This is just to be safe, don't necessarily need it
                if let Ok(num) = num_str.parse::<u64>() {
                    part1_cols[i].push(num);
                }
            }
        }
    }

    let mut part1_total = 0;
    for (i, col) in part1_cols.iter().enumerate() {
        match part1_operations[i] {
            '+' => part1_total += col.iter().sum::<u64>(),
            '*' => part1_total += col.iter().product::<u64>(),
            _ => eprintln!("Unknown operator in Part 1: {}", part1_operations[i]),
        }
    }

    println!("Advent of Code Day 6 Answer Part 1: {}", part1_total);

    // Part 2

    // `match_indices` returns an iterator of (index, matched_str)
    // This gives us the exact byte offset of every non-whitespace character in the last line.
    let part2_operations: Vec<(usize, char)> = operator_line
        .match_indices(|c: char| !c.is_whitespace())
        .map(|(i, s)| (i, s.chars().next().unwrap()))
        .collect();

    let mut part2_total = 0;

    // Iterate through each "Column" defined by the operators
    for (i, &(start_idx, op)) in part2_operations.iter().enumerate() {
        // Determine the end index for this column (horizontal boundary)
        let end_idx = part2_operations.get(i + 1).map(|(next_idx, _)| *next_idx).unwrap_or(usize::MAX);

        // Calculate the maximum width of this column block across all lines
        let mut max_width = 0;
        for line in number_lines {
            if start_idx < line.len() {
                let limit = end_idx.min(line.len());
                max_width = max_width.max(limit - start_idx);
            }
        }

        let mut col_values = Vec::new();

        // Iterate horizontally across the width of this block
        for relative_x in 0..max_width {
            let mut num_str = String::new();
            let mut num_hit = false;

            // Iterate vertically down the lines
            for line in number_lines {
                let char_idx = start_idx + relative_x;
                
                // Get the character at this position, or treat as space if out of bounds
                let c = if char_idx < line.len() {
                    line.as_bytes()[char_idx] as char
                } else {
                    ' '
                };

                if c.is_digit(10) {
                    num_str.push(c);
                    num_hit = true;
                } else if num_hit && c.is_whitespace() {
                    // Stop reading this specific vertical number if we hit a space after finding digits
                    break;
                }
            }

            if !num_str.is_empty() {
                if let Ok(num) = num_str.parse::<u64>() {
                    col_values.push(num);
                }
            }
        }

        match op {
            '+' => part2_total += col_values.iter().sum::<u64>(),
            '*' => part2_total += col_values.iter().product::<u64>(),
            _ => eprintln!("Unknown operator: {}", op),
        }
    }

    println!("Advent of Code Day 6 Answer Part 2: {}", part2_total);
}
