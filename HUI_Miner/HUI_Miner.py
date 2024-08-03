from HUI_Miner_Algorithm import HUIMiner
if __name__ == "__main__":
    minUtility = 15
    inputPath = "Dataset/smallDb.txt"
    outputPath = "outputMiner.txt"
    hui_miner = HUIMiner()
    hui_miner.runAlgorithm(inputPath, outputPath, minUtility)
    hui_miner.printStats()

