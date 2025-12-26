use std::fs;

#[derive(Debug)]
struct Box {
    x: i64,
    y: i64,
    z: i64,
}

// Union-Find Problem
fn main() {
    let input = fs::read_to_string("day08/day08.txt").unwrap();

    let boxes: Vec<Box> = input
        .lines()
        .filter(|line| !line.is_empty())
        .map(|line| {
            let dims: Vec<i64> = line
                .split(',')
                .map(|dim| dim.parse().unwrap())
                .collect();
            Box {
                x: dims[0],
                y: dims[1],
                z: dims[2],
            }
        })
        .collect();

    // Part 1

    let mut edges = Vec::new();
    for i in 0..boxes.len() {
        for j in i + 1..boxes.len() {
            let p1 = &boxes[i];
            let p2 = &boxes[j];
            let dsq = (p1.x - p2.x).pow(2) + (p1.y - p2.y).pow(2) + (p1.z - p2.z).pow(2);
            edges.push((i, j, dsq));
        }
    }
    // Sort edges by distance
    edges.sort_by_key(|edge| edge.2);

    // To work with the test input and real input
    let limit = if boxes.len() < 50 { 10 } else { 1000 };

    // Adjacency vector
    let mut adj = vec![vec![]; boxes.len()];
    for &(u, v, _) in edges.iter().take(limit) {
        adj[u].push(v);
        adj[v].push(u);
    }

    let mut visited = vec![false; boxes.len()];
    let mut sizes = Vec::new();

    for i in 0..boxes.len() {
        if !visited[i] {
            // BFS like Python implementation
            let mut count = 0;
            let mut stack = vec![i];
            visited[i] = true;
            while let Some(node) = stack.pop() {
                count += 1;
                for &neighbor in &adj[node] {
                    if !visited[neighbor] {
                        visited[neighbor] = true;
                        stack.push(neighbor);
                    }
                }
            }
            sizes.push(count);
        }
    }

    sizes.sort_unstable_by(|a, b| b.cmp(a));
    
    println!("Advent of Code Day 8 Answer Part 1: {}", sizes.iter().take(3).product::<usize>());

    // Part 2

    let mut group: Vec<usize> = (0..boxes.len()).collect();
    let mut num_groups = boxes.len();

    for &(u, v, _) in &edges {
        let mut root_u = u;
        while group[root_u] != root_u {
            root_u = group[root_u];
        }

        let mut root_v = v;
        while group[root_v] != root_v {
            root_v = group[root_v]; 
        }

        // Merge groups
        if root_u != root_v {
            group[root_v] = root_u;
            num_groups -= 1;

            if num_groups == 1 {
                println!("Advent of Code Day 8 Answer Part 2: {}", boxes[u].x * boxes[v].x);
                return;
            }
        }
    }
}