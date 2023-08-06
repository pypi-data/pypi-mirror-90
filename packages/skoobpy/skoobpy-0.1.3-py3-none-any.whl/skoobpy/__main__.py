from skoobpy import *

def main():
    from sys import argv
    user_id = argv[1]

    books_json = get_all_books(user_id)
    books_desired = filter_desired_books(books_json)
    export_csv(books_desired, user_id)

if __name__ == "__main__":
    main()