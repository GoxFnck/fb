echo "========================================"
echo "🚀 Facebook Number Checker - Auto Setup"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check command
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Update packages
echo -e "${YELLOW}[1/5] Updating packages...${NC}"
pkg update -y && pkg upgrade -y
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to update packages${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Packages updated${NC}"

# Step 2: Install Python
echo -e "${YELLOW}[2/5] Installing Python...${NC}"
if ! command_exists python3; then
    pkg install -y python
else
    echo -e "${GREEN}✅ Python already installed${NC}"
fi

# Step 3: Install Chromium
echo -e "${YELLOW}[3/5] Installing Chromium...${NC}"
if ! command_exists chromium; then
    pkg install -y chromium
else
    echo -e "${GREEN}✅ Chromium already installed${NC}"
fi

# Step 4: Install required tools
echo -e "${YELLOW}[4/5] Installing required tools...${NC}"
pkg install -y which nano git curl wget
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install tools${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Tools installed${NC}"

# Step 5: Install Python dependencies
echo -e "${YELLOW}[5/5] Installing Python dependencies...${NC}"
pip install selenium -q
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install Selenium${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Selenium installed${NC}"

# Create necessary directories
mkdir -p logs
mkdir -p outputs

echo ""
echo "========================================"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo "========================================"
echo ""
echo "📝 To run the script:"
echo "   python3 bot.py"
echo ""
echo "📁 Output files will be saved in:"
echo "   - outputs/ (results in JSON/CSV)"
echo "   - logs/ (detailed logs)"
echo ""
