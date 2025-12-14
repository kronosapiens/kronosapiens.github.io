import csv

# ---- CONFIG ----
CSV_PATH = "./gg-rankings.csv"  # path to your downloaded CSV
THRESHOLDS = [5, 10, 25, 50]


def load_ranks(path):
    """
    Load project -> rank mappings for GG20 and GG22 from a single CSV
    with columns: GG20, Rank20, GG22, Rank22.
    Empty cells are ignored.
    """
    gg20_ranks = {}
    gg22_ranks = {}

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Adjust these keys if your header names differ
            gg20_name = row.get("GG20", "").strip()
            gg22_name = row.get("GG22", "").strip()

            rank20 = row.get("Rank20", "").strip()
            rank22 = row.get("Rank22", "").strip()

            if gg20_name and rank20:
                gg20_ranks[gg20_name] = int(rank20)

            if gg22_name and rank22:
                gg22_ranks[gg22_name] = int(rank22)

    return gg20_ranks, gg22_ranks


def analyze_overlap(gg20_ranks, gg22_ranks, thresholds):
    """
    For each threshold N, compute:
    - projects in top N in GG20
    - projects in top N in GG22
    - intersection
    """
    results = []

    for N in thresholds:
        gg20_topN = {p for p, r in gg20_ranks.items() if r <= N}
        gg22_topN = {p for p, r in gg22_ranks.items() if r <= N}
        overlap = gg20_topN & gg22_topN

        results.append({
            "threshold": N,
            "overlap_count": len(overlap),
            "overlap_percentage": len(overlap) / N,
            "overlap_projects": sorted(
                overlap,
                key=lambda p: (gg20_ranks[p], gg22_ranks[p])
            )
        })

    return results


def main():
    gg20_ranks, gg22_ranks = load_ranks(CSV_PATH)

    results = analyze_overlap(gg20_ranks, gg22_ranks, THRESHOLDS)

    print("Overlap summary (projects that are in the top N in BOTH rounds):")
    print("-" * 72)

    for res in results:
        N = res["threshold"]
        print(f"Top {N}:")
        print(f"  Overlap count     : {res['overlap_count']}")
        print(f"  Overlap percentage: {res['overlap_percentage']}")
        print("  Overlap projects  :")
        for p in res["overlap_projects"]:
            print(f"    - {p} (GG20 rank {gg20_ranks[p]}, GG22 rank {gg22_ranks[p]})")
        print("-" * 72)


if __name__ == "__main__":
    main()
