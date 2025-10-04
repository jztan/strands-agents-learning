#!/bin/bash
# Setup git filter to automatically clean notebook outputs before committing

echo "Setting up Jupyter notebook output filter..."

# Configure git filter for notebooks
git config filter.nbstripout.clean 'uv run jupyter nbconvert --stdin --stdout --clear-output --to notebook'
git config filter.nbstripout.smudge cat
git config filter.nbstripout.required true

# Configure diff tool for notebooks
git config diff.ipynb.textconv 'uv run jupyter nbconvert --stdin --stdout --to markdown'

echo "✅ Git filter configured successfully!"
echo ""
echo "From now on, notebook outputs will be automatically stripped when committing."
echo "This keeps your repository clean and avoids large diffs."
