<img src="MineMetrics.svg" alt="MineMetrics" width="128">

# MineMetrics 

**MineMetrics** is a desktop application designed for Minecraft Java Edition. This tool helps you track the amount of time you've spent playing Minecraft, filling a gap left by the Java Edition (which lacks this feature, unlike Minecraft Bedrock).

## Features

- **Playtime Tracking:** Monitor how much time you've spent in Minecraft Java Edition.
- **Launcher Support:** Manually add various Minecraft launchers like Modrinth, Badlion, CurseForge, and more.

### Upcoming Features

- **Detailed Minecraft Stats:** Get in-depth insights into your gameplay, including your favorite blocks, weapons, and enemies.
- **Custom Achievements:** Showcase unique achievements for players to strive for.

## Adding Launchers Manually

To add launchers manually:

1. Navigate to the Home section.
2. Find and click on "ResourceManager."
3. Enter the launcher's name and path.
4. Specify the launcher's type (Instance or Container).

### Types of Launchers

Correctly defining the launcher type is crucial as it determines how the application reads the paths.

#### Instance

- **Description:** Launchers with a single logs folder, such as Minecraft, Badlion, Luna, etc.
- **Path Example:**  
  `/logs` or the folder directly containing `/logs`.

#### Container

- **Description:** Mod launchers or launchers with multiple instances (e.g., Modrinth, CurseForge). These have profiles or instances, each with its own logs folder.
- **Path Example:**  
  `/profiles`, with subdirectories like `/profiles/profile0`, `/profiles/profile1`, etc. You should add the `/profiles` directory.

## Important Notes on Paths

- **Instance:** You can directly add the path to the logs folder or the folder containing the logs.
  
  **Example:**  
  For Minecraft: `/logs`.

- **Container:** Add the path to the directory where instances or profiles are stored.
  
  **Example:**  
  For Modrinth: `/profiles`.