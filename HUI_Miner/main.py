from HUI_Miner import HUIMiner
if __name__ == "__main__":
    minUtility = 40
    inputPath = "Dataset/test.txt"
    outputPath = "outputMiner.txt"
    hui_miner = HUIMiner()
    hui_miner.runAlgorithm(inputPath, outputPath, minUtility)
    hui_miner.printStats()

