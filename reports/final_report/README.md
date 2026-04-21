# Final Report Workspace

This folder contains the final written report and its visual assets.

## Structure
- `final_report.md`: Main report source file (Markdown, A4-ready via Pandoc).
- `assets/`: Images, charts, and any media used in the report.

## A4 PDF Export (Pandoc)
Use this command from the project root:

```bash
pandoc reports/final_report/final_report.md \
  --from markdown+raw_tex \
  --pdf-engine=xelatex \
  -o reports/final_report/final_report.pdf
```

If `pandoc` is missing on macOS:

```bash
brew install pandoc
brew install --cask mactex-no-gui
```

## Image Usage
Store images in `reports/final_report/assets/` and reference them like:

```markdown
![Confusion matrix](assets/confusion_matrix.png)
```

## Title Page Behavior
The template in `final_report.md` uses a dedicated title page and then forces a page break so page 1 only contains the first content block.
