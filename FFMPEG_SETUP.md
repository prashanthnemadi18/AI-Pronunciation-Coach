# FFmpeg Setup Instructions

FFmpeg is required for audio processing but is not included in this repository due to file size limitations.

## Windows Installation

1. **Download FFmpeg:**
   - Visit: https://www.gyan.dev/ffmpeg/builds/
   - Download: `ffmpeg-release-essentials.zip`

2. **Extract:**
   - Extract to a location like: `C:\ffmpeg\`
   - The bin folder should contain: `ffmpeg.exe`, `ffprobe.exe`, `ffplay.exe`

3. **Configure:**
   - Option A: Add to PATH environment variable
   - Option B: Set `FFMPEG_PATH` in your `.env` file:
     ```
     FFMPEG_PATH=C:\ffmpeg\bin\ffmpeg.exe
     ```

## macOS Installation

```bash
brew install ffmpeg
```

## Linux Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

## Verification

Test if FFmpeg is installed correctly:

```bash
ffmpeg -version
```

If you see version information, FFmpeg is installed correctly!
