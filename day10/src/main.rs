use std::fs;
use good_lp::{variables, variable, default_solver, SolverModel, Solution, Expression};

#[derive(Debug)]
struct Machine {
    lights: Vec<u8>,       // Part 1 Target (0 or 1)
    buttons: Vec<Vec<u8>>, // Columns of the matrix (Each button affects these rows)
    joltage: Vec<i64>,     // Part 2 Target
}

fn parse_line(line: &str) -> Machine {
    // Input format example: "[.##.] (3) (1,3) {3,5,4,7}"
    
    // 1. Extract Light Diagram: Inside [...]
    let lights_start = line.find('[').unwrap() + 1;
    let lights_end = line.find(']').unwrap();
    let lights: Vec<u8> = line[lights_start..lights_end]
        .chars()
        .map(|c| if c == '#' { 1 } else { 0 })
        .collect();
    
    let rows = lights.len();

    // 2. Extract Joltage: Inside {...}
    let jolt_start = line.find('{').unwrap() + 1;
    let jolt_end = line.find('}').unwrap();
    let joltage: Vec<i64> = line[jolt_start..jolt_end]
        .split(',')
        .map(|s| s.trim().parse().unwrap())
        .collect();

    // 3. Extract Buttons: Inside (...)
    // The buttons are between the lights and the joltage
    // Could have made this easier with regex, but this works
    let buttons_str = &line[lights_end + 1..jolt_start - 1];
    let buttons: Vec<Vec<u8>> = buttons_str
        .split('(')
        .skip(1) // First split is empty or whitespace before first '('
        .map(|s| {
            let content = s.split_once(')').unwrap().0;
            let mut col = vec![0u8; rows];
            if !content.is_empty() {
                for idx_str in content.split(',') {
                    if let Ok(idx) = idx_str.trim().parse::<usize>() {
                        if idx < rows {
                            col[idx] = 1;
                        }
                    }
                }
            }
            col
        })
        .collect();

    Machine { lights, buttons, joltage }
}

// Part 1: Brute Force (Fast for small N)
fn solve_p1(m: &Machine) -> Option<u32> {
    let n_buttons = m.buttons.len();
    let rows = m.lights.len();
    let mut min_presses = None;

    // Iterate all 2^N combinations
    for mask in 0..(1 << n_buttons) {
        // Check if this combination works
        let mut result = vec![0u8; rows];
        let mut press_count = 0;

        for (b_idx, btn) in m.buttons.iter().enumerate() {
            if (mask >> b_idx) & 1 == 1 {
                press_count += 1;
                // XOR add button vector, equivalent to my Python solution
                for r in 0..rows {
                    result[r] ^= btn[r];
                }
            }
        }

        if result == m.lights {
            if min_presses.map_or(true, |min| press_count < min) {
                min_presses = Some(press_count);
            }
        }
    }
    
    min_presses
}

// Part 2: Integer Linear Programming (ILP) using good_lp
fn solve_p2(m: &Machine) -> Option<Vec<i64>> {
    let mut vars_builder = variables!();

    // 1. Create variables: x_i >= 0, Integer
    let vars: Vec<_> = (0..m.buttons.len())
        .map(|_| vars_builder.add(variable().min(0).integer()))
        .collect();

    // 2. Define Objective: Minimize sum(x)
    let objective: Expression = vars.iter().sum();

    // 3. Initialize Problem
    let mut problem = vars_builder.minimise(objective).using(default_solver);

    // 4. Add Constraints: A * x = b
    for (r, &target_val) in m.joltage.iter().enumerate() {
        let mut row_expr = Expression::from(0);
        for (c, _btn) in m.buttons.iter().enumerate() {
            if m.buttons[c][r] == 1 {
                row_expr += vars[c];
            }
        }
        problem.add_constraint(row_expr.eq(target_val as f64));
    }

    // 5. Solve
    match problem.solve() {
        Ok(solution) => {
            let result: Vec<i64> = vars.iter()
                .map(|&v| solution.value(v).round() as i64)
                .collect();
            Some(result)
        },
        Err(_) => None,
    }
}

fn main() {
    println!("Advent of Code Day 10");
    let input = fs::read_to_string("day10/day10.txt").expect("Read error");

    let machines: Vec<Machine> = input
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(parse_line)
        .collect();

    // Part 1

    let total_p1: u32 = machines.iter()
        .filter_map(solve_p1)
        .sum();

    println!("Advent of Code Day 10 Answer Part 1: {}", total_p1);

    // Part 2
    
    let total_p2: i64 = machines.iter()
        .filter_map(solve_p2)
        .map(|sol| sol.iter().sum::<i64>())
        .sum();

    println!("Advent of Code Day 10 Answer Part 2: {}", total_p2);
}
