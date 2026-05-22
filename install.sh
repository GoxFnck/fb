#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Colors for stylish output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${MAGENTA}==========================================${NC}"
echo -e "${MAGENTA}🚀  Encoded Python Bot - Auto Setup     ${NC}"
echo -e "${MAGENTA}==========================================${NC}"
echo ""

# Step 1: Update and Upgrade Termux Packages
echo -e "${YELLOW}[1/5] Updating system packages...${NC}"
pkg update -y
pkg upgrade -y
echo -e "${GREEN}✅ System packages updated.${NC}"
echo ""

# Step 2: Install Python3 and Pip
echo -e "${YELLOW}[2/5] Installing Python3 and Pip...${NC}"
pkg install -y python3 python3-pip
echo -e "${GREEN}✅ Python3 and Pip installed.${NC}"
echo ""

# Step 3: Setup Storage Access (Optional for Termux)
echo -e "${YELLOW}[3/5] Setting up storage access...${NC}"
if command -v termux-setup-storage &> /dev/null; then
    termux-setup-storage 2>/dev/null || true
    sleep 1
fi
echo -e "${GREEN}✅ Storage setup completed.${NC}"
echo ""

# Step 4: Create Project Directories
echo -e "${YELLOW}[4/5] Creating project directories...${NC}"
mkdir -p logs outputs cache
echo -e "${GREEN}✅ Directories created (logs/, outputs/, cache/).${NC}"
echo ""

# Step 5: Verify Installation
echo -e "${YELLOW}[5/5] Verifying installation...${NC}"
python3 --version
pip --version
echo -e "${GREEN}✅ Python and Pip verified.${NC}"
echo ""

echo -e "${MAGENTA}==========================================${NC}"
echo -e "${GREEN}🎉  Setup Completed Successfully!        ${NC}"
echo -e "${MAGENTA}==========================================${NC}"
echo ""
echo -e "${BLUE}📝 To Run:${NC}"
echo -e "  ${YELLOW}python3 bot.py${NC}"
echo ""
echo -e "${MAGENTA}==========================================${NC}"
