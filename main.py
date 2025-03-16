import re
import requests
import json


def extract_and_replace(text: str, replacements: dict[str, str]) -> str:
    # Regular expression to find content inside ${}
    pattern = r"\$\{([^}]+)\}"

    def replacer(match_items) -> str:
        key = match_items.group(1)
        return replacements.get(
            key, match_items.group(0)
        )  # Return the replacement if found, else return the original match

    # Substitute the placeholders with the replacements
    result = re.sub(pattern, replacer, text)
    return result


def turn_list_to_img(skills: list[str]) -> str:
    base_url = "https://go-skill-icons.vercel.app/api/icons?i="
    skills_str = ",".join(skills)
    img_url = f"{base_url}{skills_str}&perline=13"

    html_snippet = f"""
<p align="center">
    <a href="https://github.com/LelouchFR/skill-icons">
        <img src="{img_url}" />
    </a>
</p>
    """
    return html_snippet


def detials_template(summary: str, input: str) -> str:
    html_snipet = f"""
<details>
    <summary>{summary}✍️</summary>
    {input}
</details>
"""
    return html_snipet


def githubStats(url_point: str, params: list, alt: str) -> str:
    username = "eveeifyeve"
    base_url = "https://github-readme-stats.vercel.app/api"

    # Construct the parameters string
    params_str = "&".join(params)

    return f"""
    <img src="{base_url}{url_point}?username={username}{params_str}" height="150" alt="{alt} graph"/>
    """


def github_extra_repos(repo: str) -> str:
    base_url = "https://github-readme-stats.vercel.app/api/pin/"
    parts = repo.split("/")

    owner, name = parts

    return f"""
<a href="https://github.com/{repo}">
    <img height="150em" width="412em" align="center" src="{base_url}?username={owner}&repo={name}&langs_count=5&bg_color=30,34e8ff,9e26ff&hide_border=false&order=2&title_color=000&text_color=fff" alt="${name} repo pin" />
</a>"""


try:
    # Open the file and read its contents
    with open("README.md.rst", "r") as file:
        template = file.read()

    # Skills
    response = requests.get("https://eveeifyeve.pages.dev/api/skillIcon")
    skills = list(json.loads(response.text))

    skillsImg = turn_list_to_img(skills)

    # Details
    stats_base_url = "https://github-readme-stats.vercel.app/api"

    stats = f"""
<img src="{stats_base_url}?username=eveeifyeve&bg_color=30,34e8ff,9e26ff&title_color=000&text_color=fff" height="150" alt="stats graph"/>
<img src="{stats_base_url}/top-langs?username=eveeifyeve&locale=en&hide_title=false&layout=compact&card_width=320&langs_count=5&bg_color=30,34e8ff,9e26ff&hide_border=false&order=2&title_color=000&text_color=fff" height="150" alt="languages graph"  />
    """

    major = {"TeaClient": "CEO/Founder", "OpusClient": "Developer (2023-2024)"}
    nonmajor = {
        "DuvanMC": "Manager of Development (2024)",
        "Nodeforge": "Developer",
    }

    opensource = {
        "Evolutify": "CEO",
        "Cordevall": "CEO",
        "Minecraft-essentials": "Owner",
    }

    major_projects_lines = [f"- {project}: {role}" for project, role in major.items()]
    nonmajor_projects_lines = [
        f"- {project}: {role}" for project, role in nonmajor.items()
    ]
    opensource_projects_lines = [
        f"- {project}: {role}" for project, role in opensource.items()
    ]

    roles = f"""
### Major Projects/Company’s
{",\n".join(major_projects_lines)},

### Non-Major Projects/Company's
{",\n".join(nonmajor_projects_lines)},

### Opensource Projects: 
{",\n".join(opensource_projects_lines)}


    """

    details = detials_template("Github Stats ⚡️", stats) + detials_template(
        "Roles ✍️", roles
    )

    repos_list = [
        "eveeifyeve/Dotfiles",
        "Minecraft-Essentials/minecraft-essentials",
        "eveeifyeve/docker-rust-minecraft-server",
        "MCOpenAnti/MCOpenAnti",
        "eveeifyeve/DJApp",
        "eveeifyeve/BedrockGradleManifest",
    ]

    repos = f"""
### Check out all of my repos!
{"".join(github_extra_repos(repo) for repo in repos_list)}
    """

    replacements = {
        "List": skillsImg,
        "Details": details,
        "Repos": repos,
    }

    result = extract_and_replace(template, replacements)

    with open("README.md", "w") as readme:
        readme.write(result)

except FileNotFoundError:
    print("Error: The file 'test.txt' was not found.")
except IOError as e:
    print(f"Error reading the file: {e}")
