import math




def main():
    search = input("Type a search here")
    if search == "star":
        print("[puts up a website about stars]")
        main()
    else:
        print("There are no available websites for your search!")
        main()

main()

