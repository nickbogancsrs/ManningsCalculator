# Manning's Flow Calculator

A web-based application for hydraulic calculations of pipes, culverts, and open channels using Manning's equation.

## Features

- **Circular Pipe Analysis**: Calculate flow rate, velocity, and normal depth for circular pipes
- **Box Culvert Analysis**: Analyze rectangular culvert hydraulics with various dimensions
- **Trapezoidal Channel Analysis**: Evaluate open channel flow characteristics
- **Size Determination**: Find the minimum required pipe or culvert size for a given design flow
- **Visualization**: Generate rating curves and hydraulic profiles
- **Material Selection**: Choose from a variety of common materials with predefined roughness coefficients
- **Flow Regime Analysis**: Determine subcritical, critical, and supercritical flow conditions

## Installation

### Requirements

- Python 3.7+
- NumPy
- SciPy
- Matplotlib
- Streamlit

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/mannings-flow-calculator.git
   cd mannings-flow-calculator
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Usage

### Circular Pipe Analysis

1. Select the pipe material or enter a custom Manning's roughness coefficient
2. Enter the pipe diameter and slope
3. Choose calculation type:
   - Full pipe flow
   - Partial pipe flow (specify the depth)
   - Find normal depth for a given flow
4. View results and rating curve

### Box Culvert Analysis

1. Select the culvert material or enter a custom Manning's roughness coefficient
2. Enter the culvert width, height, and slope
3. Choose calculation type:
   - Full culvert flow
   - Partial culvert flow (specify the depth)
   - Find normal depth for a given flow
4. View results and rating curve

### Trapezoidal Channel Analysis

1. Select the channel material or enter a custom Manning's roughness coefficient
2. Enter the channel bottom width, side slope, and bed slope
3. Choose calculation type:
   - Calculate flow for a given depth
   - Find normal depth for a given flow
4. View results and rating curve

### Size Determination

1. Select culvert type (circular pipe or box culvert)
2. Enter design flow, slope, and material
3. Specify size constraints (minimum and maximum dimensions)
4. Calculate the minimum required size to handle the design flow

## Theory and Background

### Manning's Equation

The Manning's equation is used to calculate the velocity of open-channel flow:

$V = \frac{1.49}{n} R_h^{2/3} S^{1/2}$

Where:
- $V$ is the cross-sectional average velocity (ft/s)
- $n$ is Manning's roughness coefficient
- $R_h$ is the hydraulic radius (ft)
- $S$ is the slope of the hydraulic grade line (ft/ft)

Flow rate is calculated by multiplying velocity by cross-sectional area:

$Q = VA$

### Hydraulic Radius

The hydraulic radius is calculated as:

$R_h = \frac{A}{P}$

Where:
- $A$ is the cross-sectional area of flow
- $P$ is the wetted perimeter

### Flow Regime

The Froude number determines the flow regime:
- $Fr < 1$: Subcritical flow
- $Fr = 1$: Critical flow
- $Fr > 1$: Supercritical flow

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This calculator uses the Manning's equation for hydraulic calculations
- Visualization is powered by Matplotlib
- Web interface built with Streamlit
