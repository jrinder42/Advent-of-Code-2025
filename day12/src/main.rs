use std::fs;
use std::collections::HashMap;


fn main() {
    let input = fs::read_to_string("day12/day12.txt").unwrap();
   
    let mut parts = input.rsplitn(2, "\n\n");
    let regions = parts.next().unwrap();
    let presents = parts.next().unwrap();

    let region_list: Vec<(usize, usize, Vec<usize>)> = regions
        .lines()
        .map(|line| {
            let (shape, present_list) = line.split_once(": ").unwrap();
            let (r_str, c_str) = shape.split_once('x').unwrap();

            let presents_vec: Vec<usize> = present_list
                .split_whitespace()
                .map(|num_str| num_str.parse().unwrap())
                .collect();

            (r_str.parse().unwrap(), c_str.parse().unwrap(), presents_vec)
        })
        .collect();

    let presents_map: HashMap<usize, (usize, usize)> = presents
        .split("\n\n")
        .map(|pres| {
            let (present_id, present_shape) = pres.split_once('\n').unwrap();
            // `trim_end_matches` is robust if our number > 9, it strips `:`
            let id = present_id.trim_end_matches(':').parse::<usize>().unwrap();

            let rows = present_shape.lines().count();
            // Just to be safe if we don't have a square grid
            let cols = present_shape.lines().map(|line| line.len()).max().unwrap();

            (id, (rows, cols))
        })
        .collect();

    let mut present_count = 0;
    for (rows, cols, pres) in region_list {
        let grid_area = rows * cols;
        let mut total_present_area = 0;
        for (id, &freq) in pres.iter().enumerate() {
            if freq > 0 {
                if let Some(&(r, c)) = presents_map.get(&id) {
                    total_present_area += freq * r * c;
                }
            }
        }
        if total_present_area <= grid_area {
            present_count += 1;
        }
    }

    println!("Advent of Code Day 12 Answer Part 1: {}", present_count);
}