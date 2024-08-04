from HUI_Miner import HUIMiner
if __name__ == "__main__":
    minUtility = 10
    inputPath = "Dataset/mushroom.txt"
    outputPath = "outputMiner.txt"
    hui_miner = HUIMiner()
    hui_miner.runAlgorithm(inputPath, outputPath, minUtility)
    hui_miner.printStats()

