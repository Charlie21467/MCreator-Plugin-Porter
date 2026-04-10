import requests

GITHUB_RELEASES_API = "https://api.github.com/repos/MCreator/MCreator/releases"


def fetch_release_tags(limit=40):
    response = requests.get(GITHUB_RELEASES_API, params={"per_page": limit})
    response.raise_for_status()

    releases = response.json()
    return [release["tag_name"] for release in releases if "tag_name" in release]


if __name__ == "__main__":
    for tag in fetch_release_tags():
        print(tag)
