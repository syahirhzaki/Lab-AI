"""
Extra check for Part D: is the GA result reliable?
1. Brute force all 6! = 720 routes to find the true shortest distance.
2. Re-run the GA with seeds 1-20 for three population/generation settings
   and count how often it reaches that optimum.

Run:  python seed_experiment.py
"""
import itertools

import ga_delivery_route as ga

all_routes = list(itertools.permutations(ga.DELIVERY_STOPS))
optimum = min(ga.route_distance(r) for r in all_routes)
best_routes = [r for r in all_routes if ga.route_distance(r) == optimum]
print(f"Brute force over {len(all_routes)} routes: shortest distance = {optimum} km")
for r in best_routes:
    print("  ", " -> ".join(ga.full_route(r)))

print("\nGA with seeds 1-20 (distance found by each seed):")
for population, generations in [(30, 100), (10, 50), (6, 50)]:
    ga.POPULATION_SIZE, ga.GENERATIONS = population, generations
    results = [ga.route_distance(ga.run_ga(seed, verbose=False)[0]) for seed in range(1, 21)]
    hits = sum(d == optimum for d in results)
    print(f"population {population:2d}, {generations:3d} generations: {results} "
          f"-> optimum in {hits}/20 runs")
