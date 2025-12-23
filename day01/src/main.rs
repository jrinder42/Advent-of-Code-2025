use std::fs;

#[derive(Debug)]
struct Movement {
    dir: char,
    num: i32,
}

fn main() {
    // Read the entire file into a String in one line
    let input = fs::read_to_string("day01/day01.txt").unwrap();

    // Manipulate the data i.e. iterate over lines and parse numbers
    let numbers: Vec<Movement> = input
        .lines()
        .filter(|line| !line.is_empty())
        .map(|line| {
            let (dir_str, num_str) = line.split_at(1);
            Movement {
                dir: dir_str.chars().next().unwrap(),
                num: num_str.parse().unwrap(),
            }
        })
        .collect();

    // Part 1

    let mut count = 0;
    let mut start = 50;
    for movement in &numbers {
        if movement.dir == 'L' {
            let rem = (100 - movement.num) % 100;
            start += rem;
            start %= 100;
        } else {  // movement.dir == 'R'
            let rem = movement.num % 100;
            start += rem;
            start %= 100;
        }

        count += i32::from(start == 0);
    }

    println!("Advent of Code Day 1 Answer Part 1: {}", count);

    // Part 2

    count = 0;
    start = 50;
    for movement in &numbers {
        if movement.dir == 'L' {
            // can use % here because we guarantee 100 - start is non-negative
            let rem = (100 - start) % 100;
            count += (rem + movement.num) / 100;
            // rem_euclid handles negative values correctly i.e. it wraps around 100
            start = (start - movement.num).rem_euclid(100);
        } else {  // movement.dir == 'R'
            let rem = movement.num % 100;
            count += (start + movement.num) / 100;
            start += rem;
            start %= 100;
        }

    }

    println!("Advent of Code Day 1 Answer Part 2: {}", count);

}

