# Half-Life 2 Deathmatch FastDL Server Setup Guide

This guide explains how to set up a local FastDL (Fast Download) server for your Half-Life 2 Deathmatch server. This allows players to quickly download custom maps and content when joining your server.

## Prerequisites

- Python 3.7 or higher
- Half-Life 2 Deathmatch server already installed and configuration files accesable

## Required Python Packages

```bash
pip install flask pyftpdlib
```

## FastDL Server Setup

1. Save the provided Python script as `fastdl_server.py`
2. Create the following directory structure in the same folder:
```
📁 fastdl/
├── 📁 maps/
├── 📁 materials/
├── 📁 models/
└── 📁 sound/
```

3. Place your custom content in the appropriate folders
4. Compress custom content files using bzip2 (resulting in .bz2 files)

## Server Configuration

Add these lines to your `server.cfg`:
```
sv_downloadurl "http://YOUR_LOCAL_IP:5000"
sv_allowdownload 1
sv_allowupload 1
```
Replace YOUR_LOCAL_IP with your actual local IP address (e.g., 192.168.1.164)

## Running the FastDL Server

1. Open Command Prompt or Terminal
2. Navigate to your FastDL directory
3. Run the script:
```bash
python fastdl_server.py
```

The server will start on port 5000 and display your local IP address. You don't need to forward port 5000 since the game server will access it locally.

## Testing the Setup

1. Start your HL2DM server
2. Connect to your server using your public IP
3. Check the server console for any FastDL-related errors
4. Try joining with a fresh client that doesn't have your custom content

## Troubleshooting

- If players can't connect to your server, verify the port forwarding settings
- If downloads fail, check that:
  - Files are in the correct directories
  - Files are properly compressed with bzip2
  - FastDL server is running
  - `sv_downloadurl` is set correctly
  - File permissions allow the FastDL server to read the files

## Notes

- The FastDL server must be running whenever your game server is running
- Keep your custom content organized in the appropriate directories
- Regularly check the FastDL server logs for any errors or issues

