# KMISynth User Patches

A community library of patches for [KMISynth](https://github.com/KellyMurphy/KMISynth), the open-source FM / wavetable
synthesizer (VST3, AU and standalone).

Anyone can use these patches. Anyone can add their own: fork this repo, add your `.kmip` files and open a pull request.

## Using the patches

KMISynth looks for user presets in `Documents/KMISynth/Presets` (subfolders are fine), and shows them under **User** in
the preset browser.

**Easiest:** click **Code > Download ZIP** above, then copy the category folders from `Patches/` into
`Documents/KMISynth/Presets/Community/`.

**Stay up to date with git:**

```sh
# Windows (PowerShell)
git clone https://github.com/KellyMurphy/KMISynth-UserPatches "$HOME\Documents\KMISynth\Presets\Community"

# macOS / Linux
git clone https://github.com/KellyMurphy/KMISynth-UserPatches ~/Documents/KMISynth/Presets/Community
```

Run `git pull` in that folder to get new patches. Reopen the preset browser to see them.

## Adding your patches

### 1. Make and save the patch

Build your sound in KMISynth and click **Save...**. In the preset browser, right-click the patch and choose
**Edit tags...** to add a few tags, comma-separated (for example `bass, fm, dark`). Tags are stored in the file and
make the patch easy to find.

Before you save, please:

- **Match the factory loudness.** Set **Patch Level** (Filters / VCA > VCA) so the patch sits around **-18 to -24 dB
  RMS**, like the factory bank. Nobody likes a preset that blasts their speakers.
- **Set up a macro or two.** Map Macro 1 and Macro 2 to something useful (Brightness, Attack, Space...) so the patch
  can be tweaked from the Home page.
- **Check it for clipping, stuck notes and endless tails.**
- **Embedded files travel with the patch.** User wavetables and Scala tunings are saved inside the `.kmip` file. Only
  include audio and tunings you made yourself or are free to share.

### 2. Fork the repo

Click **Fork** at the top right of this page. That gives you your own copy at
`github.com/<your-username>/KMISynth-UserPatches`.

### 3. Add your files

**In the browser (no git needed):**

1. In your fork, open the right category folder under `Patches/` (for example `Patches/Bass`).
2. Click **Add file > Upload files** and drag in your `.kmip` file(s).
3. Choose **Create a new branch for this commit**, give it a name like `add-wide-reese-pad`, and click **Propose
   changes**.

**With git:**

```sh
git clone https://github.com/<your-username>/KMISynth-UserPatches
cd KMISynth-UserPatches
git checkout -b add-my-patches
cp ~/Documents/KMISynth/Presets/"My Patch.kmip" Patches/Pad/
git add Patches
git commit -m "Add My Patch (Pad)"
git push -u origin add-my-patches
```

### 4. Open a pull request

GitHub shows a **Compare & pull request** button on your fork after you push. Click it, make sure the base repository
is `KellyMurphy/KMISynth-UserPatches` and the base branch is `main`, fill in the checklist and submit.

An automatic check validates every patch file. If it fails, open the **Details** link to see what to fix, then push
another commit to the same branch. The pull request updates on its own.

### Rules

| | |
|---|---|
| **File type** | `.kmip` files saved by KMISynth only. No ZIPs, no WAVs. |
| **Location** | `Patches/<Category>/`, using one of the existing category folders. Want a new category? Ask in the PR. |
| **File name** | The patch name: letters, numbers, spaces, `-`, `_` and `'`. Max 48 characters. Must not clash with an existing patch in the same folder. |
| **Tags** | At least one tag. |
| **Original work** | Patches must be your own (variations of factory presets are fine if they're clearly your own sound). No patches copied from other synths or commercial banks. |
| **One sound per file** | Up to 10 patches per pull request makes review easier. |

Categories: Arp, Bass, Bells, Brass, Drone, FX, Keys, Lead, Organ, Pad, Pluck, Sequence.

### Credit

Your GitHub username is recorded in the commit history for each patch you add. If you'd like your name in the patch's
tags too, add a tag like `by:yourname`.

## Checking patches locally

```sh
python3 scripts/validate_patches.py
```

This runs the same checks as the pull request check: valid KMISynth XML, an allowed category folder, a valid file name,
at least one tag, and no duplicates.

## License

By submitting a patch you agree to license it under
[Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). See [LICENSE](LICENSE).
KMISynth itself is AGPL-3.0, but patches are data, not code, so they use a separate license.
