from Apriori import CApriori

def load_data_from_txt(file_path):
    with open(file_path, "r") as file:
        data = [line.strip().split(",") for line in file]
    return data

if __name__ == "__main__":
    apriori = CApriori()
    dataset = load_data_from_txt("Apriori/db.txt")
    min_support = 0.3
    frequent_itemsets = apriori.Apriori(dataset, min_support)
    print("\nFrequent itemsets with minimum support count of", min_support)
    for idx, (itemset, support) in enumerate(frequent_itemsets, start=1):
        print(f"{idx}. {itemset}: {support}")
    
    
    min_confidence = 0.5
    strong_rules = apriori.Generate_frequent_strong_rules(frequent_itemsets, min_confidence, dataset)
    
    print(f"\nTotal number of strong rules: {len(strong_rules)}\n")    
    for idx, (antecedent, consequent, confidence) in enumerate(strong_rules, start=1):
        print(f"{idx}. {antecedent} -> {consequent} with {confidence:.2f}")
