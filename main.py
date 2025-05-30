import os
import sqlite3

inputFile = "standards.txt"

def dumpCompaniesToDB(companies):
    conn = sqlite3.connect("output.db")
    cursor = conn.cursor()

    for company in companies:
        if len(company) < 3: continue

        cursor.execute("INSERT INTO oui_lookup (oui, name, address) VALUES (?, ?, ?)", (company[0], company[1], company[2]))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Setup db
    conn = sqlite3.connect("output.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS oui_lookup (id INTEGER PRIMARY KEY, oui TEXT, name TEXT, address TEXT)")

    conn.commit()
    conn.close()

    # Parse the standards file
    with open(inputFile, "r", encoding="utf-8") as file:
        companies = []
        current = 0

        currentCompanyLines = []
        while True:
            line = file.readline()

            # Ensures that the program will not exit if currentCompanyLines is full
            if (not line) and (len(currentCompanyLines) == 0):
                break

            currentCompanyLines.append(line)
            
            # The reason for or not line is because the very last line in the file will not get added to the db because there is no final \n 
            if (line == "\n") or (not line):
                if len(currentCompanyLines) == 6:
                    companies.append({})

                    # Extract oui and company name from first line (line 0)
                    oui, companyName = currentCompanyLines[0].split("(hex)")

                    oui = oui.strip().replace("-", ":")
                    companyName = companyName.strip()

                    companies[current][0] = oui
                    companies[current][1] = companyName

                    # Extract address (lines 2, 3, and 4)
                    tempAddressLines = []
                    for i, v in enumerate(currentCompanyLines[2:4], start=2):
                        tempAddressLines.append(" ".join(v.replace("\t", "").strip().split()))

                    companies[current][2] = ", ".join(tempAddressLines)
                
                    current += 1
                
                currentCompanyLines = []

                # Makes sure to dump companies to the db if there is no line
                if (len(companies) >= 25) or (not line):
                    dumpCompaniesToDB(companies)
                    
                    current = 0
                    companies = []
