#!/bin/bash
# Setup script for Gmail MCP Server

echo "Setting up Gmail MCP Server with Python 3.12..."

# Navigate to the directory
cd ~/Desktop/coding-projects/claude-gmail-manager

# Create a virtual environment
echo "Creating virtual environment..."
python3.12 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure gmail_token.pickle is in this directory"
echo "2. Update your Claude Desktop config at:"
echo "   ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
echo "Add this configuration:"
echo '{'
echo '  "mcpServers": {'
echo '    "gmail": {'
echo '      "command": "/Users/paulbrown/Desktop/coding-projects/claude-gmail-manager/venv/bin/python",'
echo '      "args": ["/Users/paulbrown/Desktop/coding-projects/claude-gmail-manager/gmail_mcp.py"]'
echo '    }'
echo '  }'
echo '}'
echo ""
echo "3. Restart Claude Desktop completely"
