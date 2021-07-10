import csv

# read from csv to dict
def read_csv_to_dict(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def main():
    filename = 'data.csv'
    data = read_csv_to_dict(filename)
    print(data[2])

if __name__ == '__main__':
    main()