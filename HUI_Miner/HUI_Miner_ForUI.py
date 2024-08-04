import time
import csv
import psutil
from collections import defaultdict

class Element:
    def __init__(self, tid, iutils, rutils):
        self.tid = tid
        self.iutils = iutils
        self.rutils = rutils

class UtilityList:
    def __init__(self, item):
        self.item = item
        self.sumIutils = 0
        self.sumRutils = 0
        self.elements = []

    def addElement(self, element):
        self.sumIutils += element.iutils
        self.sumRutils += element.rutils
        self.elements.append(element)

class HUIMiner:
    def __init__(self):
        self.startTimestamp = 0
        self.endTimestamp = 0
        self.huiCount = 0
        self.mapItemToTWU = {}
        self.joinCount = 0
        self.BUFFERS_SIZE = 200
        self.itemsetBuffer = [0] * self.BUFFERS_SIZE

    def runAlgorithm(self, inputPath, outputPath, minUtility):
        self.startTimestamp = time.time()
        self.startMemory = psutil.Process().memory_info().rss / (1024 * 1024)  # Memory in MB
        self.itemsetBuffer = [0] * self.BUFFERS_SIZE

        with open(outputPath, 'w') as writer:
            self.writer = writer

            self.mapItemToTWU = defaultdict(int)

            # Đọc dữ liệu từ tệp đầu vào
            transactions = self.readTransactions(inputPath)

            # Tính toán TWU cho mỗi mục
            self.calculateTWU(transactions, minUtility)

            # Tạo danh sách các UtilityList
            listOfUtilityLists, mapItemToUtilityList = self.createUtilityLists(minUtility)

            # Duyệt qua từng giao dịch và xây dựng UtilityList
            self.buildUtilityLists(transactions, mapItemToUtilityList, minUtility)

            # Khởi chạy HUI-Miner
            self.huiMiner([], 0, None, listOfUtilityLists, minUtility)
            self.endTimestamp = time.time()
            self.endMemory = psutil.Process().memory_info().rss / (1024 * 1024)  # Memory in MB
            executionTime = self.endTimestamp - self.startTimestamp
            memoryUsage = self.endMemory - self.startMemory
            self.writer.write(f"\nExecution Time: {executionTime:.2f} seconds\n")
            self.writer.write(f"Memory Usage: {memoryUsage:.2f} MB\n")

    def readTransactions(self, inputPath):
        transactions = []
        with open(inputPath, 'r') as file:
            reader = csv.reader(file, delimiter=':')
            for row in reader:
                items = list(map(int, row[0].split()))
                transactionUtility = int(row[1])
                utilities = list(map(int, row[2].split()))
                transactions.append((items, transactionUtility, utilities))
        return transactions

    def calculateTWU(self, transactions, minUtility):
        for items, transactionUtility, _ in transactions:
            for item in items:
                self.mapItemToTWU[item] += transactionUtility

    def createUtilityLists(self, minUtility):
        listOfUtilityLists = []
        mapItemToUtilityList = {}

        for item in self.mapItemToTWU:
            if self.mapItemToTWU[item] >= minUtility:
                uList = UtilityList(item)
                mapItemToUtilityList[item] = uList
                listOfUtilityLists.append(uList)

        listOfUtilityLists.sort(key=lambda x: self.mapItemToTWU[x.item])
        return listOfUtilityLists, mapItemToUtilityList

    def buildUtilityLists(self, transactions, mapItemToUtilityList, minUtility):
        for tid, (items, transactionUtility, utilities) in enumerate(transactions):
            revisedTransaction = []
            remainingUtility = 0

            for item, utility in zip(items, utilities):
                if self.mapItemToTWU[item] >= minUtility:
                    revisedTransaction.append((item, utility))
                    remainingUtility += utility

            revisedTransaction.sort(key=lambda x: self.mapItemToTWU[x[0]])

            for item, utility in revisedTransaction:
                remainingUtility -= utility
                element = Element(tid, utility, remainingUtility)
                mapItemToUtilityList[item].addElement(element)

    def huiMiner(self, prefix, prefixLength, pUL, ULs, minUtility):
        for i in range(len(ULs)):
            X = ULs[i]

            if X.sumIutils >= minUtility:
                self.writeHUI(prefix + [X.item], X.sumIutils)
                self.huiCount += 1

            self.joinCount += 1

            nextULs = [u for u in ULs[i+1:] if u.item > X.item]
            self.huiMiner(prefix + [X.item], prefixLength + 1, X, nextULs, minUtility)

    def writeHUI(self, itemset, utility):
        self.writer.write(f"{' '.join(map(str, itemset))} #UTL: {utility}\n")
