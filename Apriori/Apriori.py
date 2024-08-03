from itertools import chain, combinations


class CApriori:
    def __init__(self):
        self.frequent_itemsets = []

    def Create_candidates(self, prev_candidates, k):
        candidates = []
        n = len(prev_candidates)
        for i in range(n):
            for j in range(i + 1, n):
                # Kết hợp hai tập hợp nếu các phần tử đầu tiên (k-2) của chúng giống nhau
                if prev_candidates[i][: k - 2] == prev_candidates[j][: k - 2]:
                    candidate = list(set(prev_candidates[i]) | set(prev_candidates[j]))
                    candidate.sort()
                    candidates.append(candidate)
        return candidates

    def Support_count(self, dataset, candidate):
        count = 0
        for data in dataset:
            if set(candidate).issubset(set(data)):
                count += 1
        return count / len(dataset)

    def Find_frequent_items(self, dataset, candidates, min_support):
        frequent_candidates = []
        for candidate in candidates:
            support = self.Support_count(dataset, candidate)
            if support >= min_support:
                self.frequent_itemsets.append((candidate, round(support, 2)))
                frequent_candidates.append(candidate)
        return frequent_candidates

    def Apriori(self, dataset, min_support):
        k = 1
        candidates = [
            [item] for item in set(item for sublist in dataset for item in sublist)
        ]
        print(f"C{k} = {candidates}")
        frequent_candidates = self.Find_frequent_items(dataset, candidates, min_support)
        print(f"L{k} = {frequent_candidates}")
        print("*" * 30)
        k = 2
        while True:
            candidates = self.Create_candidates(candidates, k)
            print(f"C{k} = {candidates}")
            frequent_candidates = self.Find_frequent_items(
                dataset, candidates, min_support
            )
            if not frequent_candidates:
                break
            print(f"L{k} = {frequent_candidates}")
            print("*" * 30)
            candidates = frequent_candidates
            k += 1
        return self.frequent_itemsets

    def Powerset(self, s):
        return list(
            chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))
        )

    def Calculate_confidence(self, itemset, antecedent, dataset):
        # Assume some function to calculate support for itemset, antecedent, and consequent
        support_itemset = self.Support_count(dataset, itemset)
        support_antecedent = self.Support_count(dataset, antecedent)
        return support_itemset / support_antecedent

    def Generate_frequent_strong_rules(self, frequent_itemsets, min_confidence, dataset):
        strong_rules = []  # set()
        for itemset, support in frequent_itemsets:
            subsets = self.Powerset(itemset)
            print("subsets:", subsets)
            for antecedent in subsets:
                consequent = set(itemset) - set(antecedent)
                if not consequent:
                    continue
                confidence = self.Calculate_confidence(itemset, antecedent, dataset)
                if confidence >= min_confidence:
                    strong_rules.append(
                        (antecedent, consequent)
                    )  # ((frozenset(antecedent), frozenset(consequent)))
        return strong_rules
