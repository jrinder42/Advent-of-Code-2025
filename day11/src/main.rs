use std::fs;
use std::collections::HashMap;

fn count_paths(u: &str, target: &str, graph: &HashMap<String, Vec<String>>, cache: &mut HashMap<String, u64>) -> u64 {
    if u == target {
        return 1;
    }

    // Check cache
    if let Some(&count) = cache.get(u) {
        return count;
    }

    let mut total_paths = 0;
    // Use .get() because leaf nodes might not be keys in the map like defaultdict in Python does automatically
    if let Some(neighbors) = graph.get(u) {
        for neighbor in neighbors {
            total_paths += count_paths(neighbor, target, graph, cache);
        }
    }

    cache.insert(u.to_string(), total_paths);

    total_paths
}

fn main() {
    let input = fs::read_to_string("day11/day11.txt").unwrap();

    // Can turn strings into ints for big speedup (both compute + space)
    let devices: HashMap<String, Vec<String>> = input
        .lines()
        .map(|line| {
            let (source, destination) = line.split_once(": ").unwrap();
            let neighbors = destination
                .split_whitespace()
                .map(|s| s.to_string())
                .collect();

            (source.to_string(), neighbors)
        })
        .collect();

    // Part 1

    let part1_paths = count_paths("you", "out", &devices, &mut HashMap::new());
    
    println!("Advent of Code Day 11 Answer Part 1: {}", part1_paths);

    // Part 2

    let start_node = "svr";
    let end_node = "out";

    let p1 = count_paths(start_node, "fft", &devices, &mut HashMap::new());
    let p2 = count_paths("fft", "dac", &devices, &mut HashMap::new());
    let p3 = count_paths("dac", end_node, &devices, &mut HashMap::new());

    println!("Advent of Code Day 11 Answer Part 2: {}", p1 * p2 * p3);
}