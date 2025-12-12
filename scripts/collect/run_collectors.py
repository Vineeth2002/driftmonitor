from collectors.google_trends import save_google_trends
from collectors.hackernews import save_hackernews

def main():
    gt = save_google_trends()
    hn = save_hackernews()
    print("Collected:")
    print(gt)
    print(hn)

if __name__ == "__main__":
    main()
