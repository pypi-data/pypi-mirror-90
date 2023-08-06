import typofinder

if __name__ == "__main__":
    typos = typofinder.get(
        repo="gh:minho42/healthroster", min_len=14, extensions=["html", "py"]
    )
    print(typos)