# Dragon Warrior Monsters 2 App

## Overview

This Flask app is designed to use data from Dragon Warrior Monsters 2 to create an intuitive web UI. The app allows users to lookup monster information, and eventually breeding pairs and skills. Inspired by the [dwm2-tools](https://github.com/MetroWind/dwm2-tools) project.

## Features

- Efficiently parse and display Dragon Warrior Monsters 2 game data.
- Simple and accessible codebase for developers with basic web skills.
- Fast development with Flask, allowing real-time changes while running.
- Seamless integration with SQLite database for scalability.
- Designer friendly Tailwind Styling

## Setup Instructions

### Prerequisites

- [Python](https://www.python.org/downloads/) 
- [Tailwind CSS](https://github.com/tailwindlabs/tailwindcss/releases/latest)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/0ceanslim/dwm2-app.git
   cd dwm2-app
   ```
2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Run the Flask app:

    ```bash
    python app.py
    ```

4. Open your browser and navigate to http://127.0.0.1:5000/.


### Tailwind CSS
To rebuild the styles when making changes, use:

```bash
tailwindcss -i static/style/input.css -o static/style/output.css --watch
```

## Development
Contributions and pull requests are welcome!

Fork the repository.
Create a new branch for your feature or bug fix.
Submit a pull request.

## To-Do List
- Add sprites for monsters.
- Enhance styling for a more polished appearance.
- Integrate a skills database with detailed descriptions.

### Future Enhancements
Discuss any planned features or enhancements for future development.

## License

This repository is provided under the MIT License. Feel free to use, modify, and distribute these scripts as needed. Contributions and improvements are welcome. ❤️    
See the [LICENSE](LICENSE) file for details.

Acknowledgments
Special thanks to dwm2-tools for inspiration.