from Apriori import CApriori

def load_data_from_txt(file_path):
    with open(file_path, "r") as file:
        data = [line.strip().split(",") for line in file]
    return data


if __name__ == "__main__":
    apriori = CApriori()
    dataset = load_data_from_txt("Apriori\db.txt")
    min_support = 0.3
    frequent_itemsets = apriori.Apriori(dataset, min_support)
    print("\nFrequent itemsets with minimum support count of", min_support)
    for itemset, support in frequent_itemsets:
        print(f"{(itemset)}: {support}")
    print("")
    min_confidence = 1
    strong_rules = apriori.Generate_frequent_strong_rules(
        frequent_itemsets, min_confidence, dataset
    )
    print("")
    for antecedent, consequent in strong_rules:
        print(f"{antecedent} -> {consequent}")
