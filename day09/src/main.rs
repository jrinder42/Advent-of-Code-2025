use std::cmp::{max, min};
use std::fs;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Point {
    r: i64,
    c: i64,
}

impl Point {
    // Shorthand to write `Point::new(r, c)`
    fn new(r: i64, c: i64) -> Self {
        Self { r, c }
    }
}

// Axis-Aligned Bounding Box
#[derive(Debug, Clone, Copy)]
struct Rect {
    min_r: i64,
    max_r: i64,
    min_c: i64,
    max_c: i64,
}

impl Rect {
    // Like a classmethod in Python
    fn from_points(p1: Point, p2: Point) -> Self {
        Rect {
            min_r: min(p1.r, p2.r),
            max_r: max(p1.r, p2.r),
            min_c: min(p1.c, p2.c),
            max_c: max(p1.c, p2.c),
        }
    }

    fn area(&self) -> i64 {
        let h = (self.max_r - self.min_r) + 1;
        let w = (self.max_c - self.min_c) + 1;
        h * w
    }
}

// Ray Casting Algorithm for Point-in-Polygon check
// Odd: You are inside. Even: You are outside.
fn is_point_in_polygon(p: Point, polygon: &[Point]) -> bool {
    let n = polygon.len();
    let mut inside = false;  // Assume outside by default
    let mut j = n - 1;

    for i in 0..n {
        let pi = polygon[i];
        let pj = polygon[j];  // Previous vertex, forming edge pj -> pi

        // Check if point is on the edge (boundary is considered inside)
        if on_segment(p, pi, pj) {
            return true;
        }

        // Ray casting (checks horizontal crossings)
        if ((pi.r > p.r) != (pj.r > p.r)) &&
            (p.c as f64) < (pj.c - pi.c) as f64 * (p.r - pi.r) as f64 / (pj.r - pi.r) as f64 + pi.c as f64 {
            inside = !inside;
        }
        j = i;  // Next edge
    }
    inside
}

// Boundary checking i.e. are these 3 points collinear
// Cross product of 2 vectors = area of parallelogram
fn on_segment(p: Point, a: Point, b: Point) -> bool {
    let cross_product = (b.c - a.c) * (p.r - a.r) - (b.r - a.r) * (p.c - a.c);
    if cross_product != 0 { 
        return false; 
    }
    p.r >= min(a.r, b.r) && p.r <= max(a.r, b.r) &&
    p.c >= min(a.c, b.c) && p.c <= max(a.c, b.c)
}

// Check if a rectangle is fully contained within the polygon, assume rectilinear
fn is_rect_inside_polygon(rect: &Rect, polygon: &[Point]) -> bool {
    // 1. All 4 corners must be in the polygon
    let corners = [
        Point::new(rect.min_r, rect.min_c),
        Point::new(rect.min_r, rect.max_c),
        Point::new(rect.max_r, rect.max_c),
        Point::new(rect.max_r, rect.min_c),
    ];

    for p in &corners {
        if !is_point_in_polygon(*p, polygon) {
            return false;
        }
    }

    // 2. No polygon vertex can be strictly inside the rectangle 
    for p in polygon {
        if p.r > rect.min_r && p.r < rect.max_r && p.c > rect.min_c && p.c < rect.max_c {
            return false;
        }
    }

    // 3. No polygon edge can pass strictly through the interior of the rectangle
    let n = polygon.len();
    for i in 0..n {
        let p1 = polygon[i];
        let p2 = polygon[(i + 1) % n];

        // Check if vertical edge passes through rect
        if p1.c == p2.c {
            let edge_c = p1.c;
            if edge_c > rect.min_c && edge_c < rect.max_c {
                let min_r = min(p1.r, p2.r);
                let max_r = max(p1.r, p2.r);
                // Check for overlapping intervals
                if min_r < rect.max_r && max_r > rect.min_r {
                    return false;
                }
            }
        }
        // Check if horizontal edge passes through rect
        else if p1.r == p2.r {
            let edge_r = p1.r;
            if edge_r > rect.min_r && edge_r < rect.max_r {
                let min_c = min(p1.c, p2.c);
                let max_c = max(p1.c, p2.c);
                // Check for overlapping intervals
                if min_c < rect.max_c && max_c > rect.min_c {
                    return false;
                }
            }
        }
    }

    true
}

fn main() {
    println!("Advent of Code Day 9");
    let input = fs::read_to_string("day09/day09.txt").unwrap();

    let points: Vec<Point> = input
        .lines()
        .filter(|l| !l.is_empty())
        .map(|line| {
            let (x_str, y_str) = line.split_once(',').unwrap();
            Point::new(
                y_str.trim().parse().unwrap(),
                x_str.trim().parse().unwrap()
            )
        })
        .collect();

    // Part 1: Max bounding box area of any two points

    let mut max_area_p1 = 0;
    for i in 0..points.len() {
        for j in i + 1..points.len() {
            let rect = Rect::from_points(points[i], points[j]);
            max_area_p1 = max(max_area_p1, rect.area());
        }
    }
    println!("Advent of Code Day 9 Answer Part 1: {}", max_area_p1);

    // Part 2
    /*
    1. Are the 4 corners of the rectangle inside the polygon?
    2. Are there any polygon vertices inside the rectangle?
    3. Do any polygon edges cross the rectangle interior?
     */

    let mut candidates = Vec::new();
    for i in 0..points.len() {
        for j in i + 1..points.len() {
            let p1 = points[i];
            let p2 = points[j];
            if p1.r != p2.r && p1.c != p2.c {
                candidates.push(Rect::from_points(p1, p2));
            }
        }
    }

    // Heuristic: Sort by area descending to find the largest one faster
    candidates.sort_by_key(|r| -r.area());

    let mut max_area_p2 = 0;
    for rect in candidates {
        if is_rect_inside_polygon(&rect, &points) {
            max_area_p2 = rect.area();
            break; 
        }
    }
    println!("Advent of Code Day 9 Answer Part 2: {}", max_area_p2);
}