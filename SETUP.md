# Install this profile in your GitHub account

This package is intended for your existing special profile repository:

**https://github.com/Christophermathai/Christophermathai**

1. Extract the ZIP archive.
2. Copy every item inside the extracted folder (including the hidden `.github` folder) into the root of your `Christophermathai/Christophermathai` repository.
3. Replace the existing `README.md` when prompted, then commit and push the files.
4. Open the repository's **Actions** tab. Enable Actions if GitHub prompts you, then run **Update profile statistics** using **Run workflow**.
5. The workflow refreshes the statistics SVG once per day after that.

You can also install it with Git:

```bash
git clone https://github.com/Christophermathai/Christophermathai.git
cd Christophermathai
# Extract/copy the package contents into this folder, then:
git add README.md assets scripts .github/workflows/update-profile.yml SETUP.md
git commit -m "Add personalized GitHub profile"
git push
```

## What updates automatically

The workflow reads your public GitHub profile and public repositories and updates repository count, total stars, followers, and forks. It does not calculate total lifetime commits or lines of code, because those require a more expensive and less reliable cross-repository history scan.

No personal access token or extra secret is required. The workflow uses the repository-scoped `GITHUB_TOKEN` for the scheduled commit. Make sure repository **Settings → Actions → General → Workflow permissions** allows read and write permissions if the workflow cannot push.
