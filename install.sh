#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Colors for stylish output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}🚀  Facebook Number Checker - Auto Setup  ${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Step 1: Update and Upgrade Termux Packages
echo -e "${YELLOW}[1/6] Updating and upgrading system packages...${NC}"
pkg update -y && pkg upgrade -y
echo -e "${GREEN}✅ System packages updated successfully.${NC}"
echo ""

# Step 2: Setup Storage Access
echo -e "${YELLOW}[2/6] Setting up storage access...${NC}"
echo -e "${BLUE}📢 Please allow storage permission if a popup appears!${NC}"
termux-setup-storage
sleep 2
echo -e "${GREEN}✅ Storage setup completed.${NC}"
echo ""

# Step 3: Install Core Packages (Python, Git)
echo -e "${YELLOW}[3/6] Installing Python and Git...${NC}"
pkg install -y python git
echo -e "${GREEN}✅ Python and Git installed.${NC}"
echo ""

# Step 4: Install Python Dependencies
echo -e "${YELLOW}[4/6] Installing Selenium...${NC}"
pip install selenium
echo -e "${GREEN}✅ Selenium installed successfully.${NC}"
echo ""

# Step 5: Add Extra Repositories (TUR, X11)
echo -e "${YELLOW}[5/6] Adding tur-repo and x11-repo...${NC}"
pkg install -y tur-repo x11-repo
echo -e "${GREEN}✅ Repositories added.${NC}"
echo ""

# Step 6: Install Chromium Browser
echo -e "${YELLOW}[6/6] Installing Chromium Browser...${NC}"
pkg install -y chromium
echo -e "${GREEN}✅ Chromium installed successfully.${NC}"
echo ""

# Final Verification & Directory Setup
echo -e "${YELLOW}📁 Creating logs and outputs directories...${NC}"
mkdir -p logs outputs
echo -e "${GREEN}✅ Directories created.${NC}"
echo ""

echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}🎉  Installation & Setup Completed!       ${NC}"
echo -e "${BLUE}=========================================${NC}"
echo -e "Run your script using: ${YELLOW}python bot.py${NC}"
echo -e "${BLUE}=========================================${NC}"
