from src.workflow import Workflow

def main():
    query = input("Enter your art research query: ")
    workflow = Workflow()
    result = workflow.run(query)
    print("\n--- Results ---")
    if result.get("artists"):
        for artist in result["artists"]:
            print(f"\n{artist.name}")
            print(f"  Styles: {', '.join(artist.styles)}")
            print(f"  Bio: {artist.bio}")
    if result.get("analysis"):
        print(f"\nRecommendation:\n{result['analysis']}")


if __name__ == "__main__":
    main()
