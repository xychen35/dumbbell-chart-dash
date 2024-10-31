# Life Expectancy Dumbbell Chart in Europe

This project is a **Dash Plotly application** that displays a **dumbbell chart** visualizing life expectancy across European countries in the years **1952, 1977 (interpolated), and 2002**. The chart enables a clear comparison of life expectancy over time, helping identify trends and progress across decades.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)

## Overview

This app uses Plotly's `gapminder` dataset, filtering data to only include European countries for selected years. An interpolation function calculates life expectancy for the year **1977**, enabling a continuous view of life expectancy trends over 50 years.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/xychen35/dumbbell-chart-dash.git
    cd dumbbell-chart-dash
    ```

2. **Install dependencies**:
    Make sure you have Python and `pip` installed, then run:
    ```bash
    pip install dash pandas plotly
    ```

## Usage

To run the application locally:
```bash
python app.py
```

After running, open your browser and go to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to see the chart.
