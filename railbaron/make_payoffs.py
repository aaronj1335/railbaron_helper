from random import random
import csv


cities = sorted({l.strip() for l in open('railbaron/cities.csv')})
payoffs = {c: {} for c in cities}

for from_city in cities:
    for to_city in cities:
        if from_city in payoffs[to_city]:
            payoffs[from_city][to_city] = payoffs[to_city][from_city]
        else:
            if from_city == to_city:
                payoffs[from_city][to_city] = 0
            else:
                payoffs[from_city][to_city] = int(random() * 100 + 1)

with open('railbaron/payoffs.csv', 'w') as output_file:
    output = csv.writer(output_file)
    output.writerow([''] + [c for c in cities])
    for from_city in cities:
        output.writerow([from_city] + [payoffs[from_city][to] for to in cities])