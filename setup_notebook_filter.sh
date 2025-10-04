#!/bin/bash
# Helper script to clean notebook outputs before committing

echo "🧹 Cleaning Jupyter notebook outputs..."
echo ""

# Find all .ipynb files and clean them
for notebook in *.ipynb; do
    if [ -f "$notebook" ]; then
        echo "  Cleaning: $notebook"
        uv run jupyter nbconvert --clear-output --inplace "$notebook"
    fi
done

echo ""
echo "✅ All notebooks cleaned!"
echo ""
echo "💡 Remember to run this script before committing notebooks:"
echo "   ./setup_notebook_filter.sh"
echo "   git add *.ipynb"
echo "   git commit -m 'Your message'"
