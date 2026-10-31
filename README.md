# Xueyi Zhang · Academic Homepage

Bilingual academic homepage for [xueyizhang1998.github.io](https://xueyizhang1998.github.io), built with Jekyll and published through GitHub Pages.

The October 2026 update uses the supplied CV for the portrait, biography, current appointments, HELIX launch and translation-glasses demo, robot project, academic service, and honors. The publication section follows [Zhiyuan Yan’s homepage](https://yzy-stack.github.io/): a method figure on the left and an italic title, authors, venue, and highlighted text links on the right. Each of the eight papers appears once. Four of these selected papers are marked Oral, as stated in the CV.

## Edit content

| Content | Source |
| --- | --- |
| Name, affiliation, portrait, contact links | `_data/profile.yml` |
| Biography, research interests, achievement counts | `_data/about.yml` |
| News and event photographs | `_data/news.yml` |
| Eight first-author research highlights | `_data/publications.yml` |
| Research and education | `_data/experience.yml` |
| Projects | `_data/projects.yml` |
| Academic service | `_data/service.yml` |
| Academic honors and competition awards | `_data/honors.yml`, `_data/competitions.yml` |
| English and Chinese labels | `_data/ui.yml` |

Publication order uses the unique `order` field, highest first. Figures retain their original proportions and open at full resolution when clicked. Figure sources are recorded in `assets/img/pub/SOURCES.md`. Add code links only after verifying the official repository.

## Preview

The lightweight preview uses the actual Liquid templates, including shared publication and sidebar components. It requires Ruby, Liquid 4, and Kramdown:

```sh
gem install liquid -v 4.0.4
gem install kramdown -v 2.5.2
python3 build_preview.py
```

Open `preview.html` directly, or serve the repository locally. The generated preview file is ignored by Git. To run the complete Jekyll build instead:

```sh
bundle install
bundle exec jekyll serve
```

## Publish

Commit the reviewed changes and push to the existing `main` branch. GitHub Pages builds the site from the repository root. The live address stays [xueyizhang1998.github.io](https://xueyizhang1998.github.io).

## Layout and behavior

- English/Chinese toggle with a saved language preference.
- A portrait extracted from the supplied CV, preserving its crop.
- Responsive publication rows with complete, uncropped method diagrams.
- Figure viewer with keyboard focus handling and Escape to close.
- Native expandable competition-award details.
- White background, restrained blue type, and pale yellow link highlighting in the publication list.

The implementation is independent; the reference site is used for visual direction. Paper figures belong to their respective authors and publishers.
